# Análisis de Historial de Streaming en Spotify

Este proyecto analiza datos de historial de reproducción de Spotify extraídos en formato JSON. Incluye transformaciones de datos, estadísticas avanzadas, y visualizaciones interactivas para comprender patrones de reproducción, canciones más escuchadas, motivos de inicio y fin, y otros insights clave.

## Contenido del Código

### 1. **Configuración Inicial**
- Se configuran los estilos y temas para las gráficas utilizando `seaborn` y `matplotlib`.
- Carga un archivo JSON con datos de historial de reproducción de Spotify.

### 2. **Transformación de Datos**
- Conversión de datos JSON a un `DataFrame` de pandas.
- Renombrado de columnas para mayor claridad.
- Conversión de marcas de tiempo a formato datetime.
- Conversión de duración de reproducciones de milisegundos a segundos.

### 3. **Limpieza de Datos**
- Eliminación de columnas irrelevantes (`direccion_ip`, `marca_tiempo_offline`).
- Creación de columnas adicionales como:
  - `anio`: Año de la reproducción.
  - `mes_anio`: Mes y año combinados para análisis mensual.
  - `duracion_segundos`: Duración de la reproducción en segundos.

### 4. **Estadísticas y Métricas Avanzadas**
#### a) **Por Canción**
- Top 30 canciones más reproducidas.
- Análisis de la duración total por canción.

#### b) **Por Artista**
- Top 10 artistas más reproducidos.
- Duración total de reproducciones por artista.

#### c) **Por Álbum**
- Top 10 álbumes más reproducidos.

#### d) **Distribución de Duración**
- Histograma para analizar la duración de las reproducciones.

#### e) **Reproducciones por Mes y Año**
- Análisis temporal de reproducciones.

#### f) **Canciones Más Saltadas**
- Identificación de las canciones que los usuarios más han saltado.

#### g) **Motivos de Inicio y Fin**
- Análisis de los motivos para iniciar y finalizar reproducciones.

#### h) **Por Plataforma**
- Distribución de reproducciones por plataformas (ej., móvil, escritorio).

#### i) **Estados de Reproducción**
- Reproducciones en modo aleatorio, offline, e incógnito.

#### j) **Reproducciones por País**
- Top 10 países con más reproducciones.

#### k) **Reproducciones por Hora del Día y Día de la Semana**
- Análisis de patrones horarios y semanales.

### 5. **Visualizaciones**
El proyecto incluye visualizaciones para una mejor comprensión de los datos:
- Gráficos de dona para canciones y álbumes más reproducidos.
- Diagramas de barras para artistas, plataformas y motivos de inicio/fin.
- Gráficos de línea para patrones temporales.
- Histogramas para distribuciones de duración.

## Requisitos
- **Python 3.7+**
- Librerías utilizadas:
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `json`