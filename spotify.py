#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datetime import datetime

# Configuración de estilos y tema
sns.set_theme(style="whitegrid", font_scale=1.1)
plt.rcParams["figure.figsize"] = (12, 8)
plt.rcParams.update({'font.size': 12})

def main():
    # Ruta al archivo JSON del historial de streaming
    streaming_history_json_path = './spotifydata/Streaming_History_Audio_2023-2024_0.json'

    # Cargar el historial de streaming desde JSON
    try:
        with open(streaming_history_json_path, 'r', encoding='utf-8') as f:
            streaming_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: El archivo {streaming_history_json_path} no se encontró.")
        return
    except json.JSONDecodeError:
        print(f"Error: El archivo {streaming_history_json_path} no es un JSON válido.")
        return

    # Convertir el historial de streaming a DataFrame
    df = pd.json_normalize(streaming_data)

    # Renombrar columnas a español y mayor claridad
    df.rename(columns={
        'ts': 'marca_tiempo',
        'master_metadata_track_name': 'nombre_cancion',
        'master_metadata_album_artist_name': 'artista',
        'master_metadata_album_album_name': 'album',
        'spotify_track_uri': 'uri_cancion',
        'ms_played': 'duracion_ms',
        'platform': 'plataforma',
        'conn_country': 'pais_conexion',
        'ip_addr': 'direccion_ip',
        'reason_start': 'motivo_inicio',
        'reason_end': 'motivo_fin',
        'shuffle': 'modo_aleatorio',
        'skipped': 'saltada',
        'offline': 'modo_offline',
        'offline_timestamp': 'marca_tiempo_offline',
        'incognito_mode': 'modo_incognito'
    }, inplace=True)

    # Seleccionar y reorganizar columnas relevantes
    df = df[[
        'marca_tiempo', 'plataforma', 'duracion_ms', 'pais_conexion',
        'nombre_cancion', 'artista', 'album', 'uri_cancion',
        'motivo_inicio', 'motivo_fin', 'modo_aleatorio', 'saltada',
        'modo_offline', 'marca_tiempo_offline', 'modo_incognito'
    ]]

    # Convertir 'marca_tiempo' a datetime
    df['marca_tiempo'] = pd.to_datetime(df['marca_tiempo'], errors='coerce')

    # Convertir 'duracion_ms' a segundos
    df['duracion_segundos'] = df['duracion_ms'].apply(lambda x: round(x / 1000) if pd.notnull(x) else np.nan)
    df.drop('duracion_ms', axis=1, inplace=True)

    # Mostrar información del DataFrame
    print("Primeras filas del DataFrame de streaming:")
    print(df.head())

    print("\nInformación del DataFrame de streaming:")
    df.info()

    # Valores nulos
    print("\nValores nulos en el DataFrame de streaming:")
    print(df.isnull().sum())

    # Eliminar columnas no utilizadas
    columnas_eliminar = ['direccion_ip', 'marca_tiempo_offline']
    df.drop(columns=columnas_eliminar, inplace=True, errors='ignore')

    # --- Análisis Exploratorio de Datos Avanzado ---
    print("\nDescripción estadística del DataFrame de streaming:")
    print(df.describe(include='all').transpose())

    # 1. Métricas por Canción
    stats_canciones = df.groupby(['nombre_cancion', 'artista'], as_index=False).agg(
        reproducciones=('uri_cancion', 'count'),
        duracion_total_seg=('duracion_segundos', 'sum')
    )
    stats_canciones['duracion_total_min'] = round(stats_canciones['duracion_total_seg'] / 60, 2)
    stats_canciones.sort_values('reproducciones', ascending=False, inplace=True)

    print("\nTop 10 canciones más reproducidas:")
    print(stats_canciones.head(10).to_string(index=False))

    # 2. Métricas por Artista
    stats_artistas = df.groupby('artista', as_index=False).agg(
        reproducciones=('uri_cancion', 'count'),
        duracion_total_seg=('duracion_segundos', 'sum')
    )
    stats_artistas['duracion_total_min'] = round(stats_artistas['duracion_total_seg'] / 60, 2)
    stats_artistas.sort_values('reproducciones', ascending=False, inplace=True)

    print("\nTop 10 artistas más reproducidos:")
    print(stats_artistas.head(10).to_string(index=False))

    # 3. Métricas por Álbum
    stats_albums = df.groupby(['album', 'artista'], as_index=False).agg(
        reproducciones=('uri_cancion', 'count'),
        duracion_total_seg=('duracion_segundos', 'sum')
    )
    stats_albums['duracion_total_min'] = round(stats_albums['duracion_total_seg'] / 60, 2)
    stats_albums.sort_values('reproducciones', ascending=False, inplace=True)

    print("\nTop 10 álbumes más reproducidos:")
    print(stats_albums.head(10).to_string(index=False))

    # 4. Distribución de la duración de las reproducciones
    plt.figure(figsize=(12, 8))
    sns.histplot(df['duracion_segundos'].dropna(), bins=50, kde=True, color='steelblue')
    plt.title('Distribución de la Duración de las Reproducciones (en segundos)', fontsize=16)
    plt.xlabel('Duración (segundos)', fontsize=14)
    plt.ylabel('Frecuencia', fontsize=14)
    plt.tight_layout()
    plt.show()

    # 5. Reproducciones por Mes (sin espacio entre meses)
    # Extraer mes y año y crear una etiqueta "mes-año"
    df['mes_num'] = df['marca_tiempo'].dt.month
    df['anio'] = df['marca_tiempo'].dt.year
    # Crear columna mes-año con formato "mes-año"
    df['mes_anio'] = df.apply(lambda x: f"{x['mes_num']}-{x['anio']}", axis=1)

    reproducciones_mensuales = df.groupby('mes_anio').size().reset_index(name='reproducciones')
    # Ordenar por año y mes numéricamente
    # Extraemos números para poder ordenar correctamente
    reproducciones_mensuales['anio'] = reproducciones_mensuales['mes_anio'].apply(lambda x: int(x.split('-')[1]))
    reproducciones_mensuales['mes_num'] = reproducciones_mensuales['mes_anio'].apply(lambda x: int(x.split('-')[0]))
    reproducciones_mensuales = reproducciones_mensuales.sort_values(['anio', 'mes_num'])

    print("\nReproducciones por mes (mes-año):")
    print(reproducciones_mensuales.head())

    plt.figure(figsize=(14, 8))
    # Plot estético sin espacios entre puntos del eje X
    sns.lineplot(data=reproducciones_mensuales, x='mes_anio', y='reproducciones', marker='o', color='green')
    plt.title('Número de Reproducciones por Mes', fontsize=16)
    plt.xlabel('Mes-Año', fontsize=14)
    plt.ylabel('Número de Reproducciones', fontsize=14)
    plt.xticks(rotation=45, ha='right')

    # Añadir etiquetas encima de cada punto
    for idx, row in reproducciones_mensuales.iterrows():
        plt.text(idx, row['reproducciones'] + 5, str(row['reproducciones']), color='blue', ha="center", va="bottom", fontsize=10)

    plt.tight_layout()
    plt.show()

    # 6. Canciones Más Saltadas
    df_saltadas = df[df['saltada'] == True]
    stats_saltadas = df_saltadas.groupby(['nombre_cancion', 'artista'], as_index=False).agg(
        saltos=('uri_cancion', 'count')
    ).sort_values('saltos', ascending=False).head(10)

    print("\nTop 10 canciones más saltadas:")
    print(stats_saltadas.to_string(index=False))

    # 7. Motivos de Inicio
    motivos_inicio = df['motivo_inicio'].value_counts().reset_index()
    motivos_inicio.columns = ['motivo_inicio', 'cantidad']
    plt.figure(figsize=(14, 8))
    sns.barplot(data=motivos_inicio, x='cantidad', y='motivo_inicio', color='purple')
    plt.title('Motivos de Inicio de Reproducción', fontsize=16)
    plt.xlabel('Cantidad', fontsize=14)
    plt.ylabel('Motivo de Inicio', fontsize=14)
    plt.tight_layout()
    plt.show()

    # 8. Motivos de Fin
    motivos_fin = df['motivo_fin'].value_counts().reset_index()
    motivos_fin.columns = ['motivo_fin', 'cantidad']
    plt.figure(figsize=(14, 8))
    sns.barplot(data=motivos_fin, x='cantidad', y='motivo_fin', color='darkred')
    plt.title('Motivos de Fin de Reproducción', fontsize=16)
    plt.xlabel('Cantidad', fontsize=14)
    plt.ylabel('Motivo de Fin', fontsize=14)
    plt.tight_layout()
    plt.show()

    # 9. Reproducciones por Plataforma
    plataformas = df['plataforma'].value_counts().reset_index()
    plataformas.columns = ['plataforma', 'cantidad']
    plt.figure(figsize=(14, 8))
    sns.barplot(data=plataformas, x='cantidad', y='plataforma', color='teal')
    plt.title('Reproducciones por Plataforma', fontsize=16)
    plt.xlabel('Cantidad', fontsize=14)
    plt.ylabel('Plataforma', fontsize=14)
    plt.tight_layout()
    plt.show()

    # 10. Estados de Reproducción
    estados = {
        'modo_aleatorio': 'Reproducciones en modo aleatorio',
        'modo_offline': 'Reproducciones en modo offline',
        'modo_incognito': 'Reproducciones en modo incógnito'
    }
    df_estados = pd.DataFrame({
        'estado': list(estados.values()),
        'cantidad': [df[col].sum() for col in estados.keys()]
    })

    plt.figure(figsize=(14, 8))
    sns.barplot(data=df_estados, x='cantidad', y='estado', color='orange')
    plt.title('Estado de Reproducción', fontsize=16)
    plt.xlabel('Cantidad', fontsize=14)
    plt.ylabel('Estado', fontsize=14)
    plt.tight_layout()
    plt.show()

    # 11. Países con más reproducciones
    paises = df['pais_conexion'].value_counts().reset_index()
    paises.columns = ['pais', 'cantidad']
    plt.figure(figsize=(14, 8))
    sns.barplot(data=paises.head(10), x='cantidad', y='pais', color='chocolate')
    plt.title('Top 10 Países por Número de Reproducciones', fontsize=16)
    plt.xlabel('Cantidad', fontsize=14)
    plt.ylabel('País', fontsize=14)
    plt.tight_layout()
    plt.show()

    # --- Nuevas Estadísticas Avanzadas ---
    # 12. Reproducciones por Hora del Día
    df['hora'] = df['marca_tiempo'].dt.hour
    reproducciones_por_hora = df.groupby('hora').size().reset_index(name='reproducciones')
    plt.figure(figsize=(14, 8))
    sns.lineplot(data=reproducciones_por_hora, x='hora', y='reproducciones', marker='o', color='purple')
    plt.title('Reproducciones por Hora del Día', fontsize=16)
    plt.xlabel('Hora del Día (0-23)', fontsize=14)
    plt.ylabel('Reproducciones', fontsize=14)
    for idx, row in reproducciones_por_hora.iterrows():
        plt.text(row['hora'], row['reproducciones'] + 5, str(row['reproducciones']), ha='center', va='bottom')
    plt.tight_layout()
    plt.show()

    # 13. Reproducciones por Día de la Semana
    # Mapeamos el número de día a nombre en español (sin usar locale)
    # 0: Lunes, 6: Domingo
    dias_map = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}
    df['dia_semana'] = df['marca_tiempo'].dt.weekday.map(dias_map)
    # Ordenar días
    orden_dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    reproducciones_por_dia = df.groupby('dia_semana').size().reset_index(name='reproducciones')
    # Convertimos dia_semana a categoría para asegurar el orden correcto
    reproducciones_por_dia['dia_semana'] = pd.Categorical(reproducciones_por_dia['dia_semana'], categories=orden_dias, ordered=True)
    reproducciones_por_dia.sort_values('dia_semana', inplace=True)

    plt.figure(figsize=(14, 8))
    sns.barplot(data=reproducciones_por_dia, x='dia_semana', y='reproducciones', color='skyblue')
    plt.title('Reproducciones por Día de la Semana', fontsize=16)
    plt.xlabel('Día de la Semana', fontsize=14)
    plt.ylabel('Reproducciones', fontsize=14)
    for idx, row in reproducciones_por_dia.iterrows():
        plt.text(idx, row['reproducciones'] + 10, str(row['reproducciones']), ha='center', va='bottom')
    plt.tight_layout()
    plt.show()

    # 14. Proporción de Reproducciones Saltadas vs No Saltadas
    total_reproducciones = len(df)
    total_saltadas = df['saltada'].sum()
    total_no_saltadas = total_reproducciones - total_saltadas

    plt.figure(figsize=(8, 8))
    plt.pie([total_saltadas, total_no_saltadas],
            labels=['Saltadas', 'No Saltadas'],
            autopct='%1.1f%%', startangle=90, colors=['#ff9999', '#66b3ff'])
    plt.title('Proporción de Reproducciones Saltadas', fontsize=16)
    plt.tight_layout()
    plt.show()

    # 15. Ratio de Saltos por Artista
    artistas_saltos = df.groupby('artista').agg(
        reproducciones=('uri_cancion', 'count'),
        saltos=('saltada', 'sum')
    )
    artistas_saltos['ratio_saltos'] = artistas_saltos['saltos'] / artistas_saltos['reproducciones']
    artistas_saltos_top = artistas_saltos.sort_values('ratio_saltos', ascending=False).head(5).reset_index()

    plt.figure(figsize=(14, 8))
    sns.barplot(data=artistas_saltos_top, x='ratio_saltos', y='artista', color='red')
    plt.title('Top 5 Artistas con Mayor Ratio de Saltos', fontsize=16)
    plt.xlabel('Ratio de Saltos', fontsize=14)
    plt.ylabel('Artista', fontsize=14)
    for idx, row in artistas_saltos_top.iterrows():
        plt.text(row['ratio_saltos'] + 0.001, idx, f"{row['ratio_saltos']:.2f}", va='center')
    plt.tight_layout()
    plt.show()

    # 16. Matriz de Correlación (Variables Numéricas)
    numericas = df[['duracion_segundos', 'hora']]
    corr = numericas.corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Matriz de Correlaciones entre Variables Numéricas', fontsize=16)
    plt.tight_layout()
    plt.show()

    # Guardar DataFrame procesado
    processed_streaming_csv = './spotifydata/processed_streaming_history_mejorado.csv'
    df.to_csv(processed_streaming_csv, index=False)
    print(f"\nDataFrame procesado y mejorado guardado en: {processed_streaming_csv}")

if __name__ == "__main__":
    main()
