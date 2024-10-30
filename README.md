# Prueba técnica Lulo Bank - Data engineers
Presentado por: 
Yudi Liseth Alvarez Alvarez
lizethalvarez678@gmail.com

---

## ⚠️ Advertencia
Antes de ejecutar cualquier script en este proyecto, asegúrate de **crear y activar un entorno virtual** y de **instalar las librerías necesarias** indicadas en `requirements.txt`

##### Pasos para Configuración y Activación del Entorno Virtual
1. **Crear el entorno virtual**:  
   Desde la carpeta raíz del proyecto, ejecuta el siguiente comando:
   ```bash
   python -m venv venv
2. **Activa el entorno virtual**: 
    Desde la carpeta raíz del proyecto, ejecuta el siguiente comando:
   ```bash
   .\venv\Scripts\activate
3. **Instalar dependencias**: 
    ```bash
   pip install -r requirements.txt
# Índice
1. [Obtención de datos y almacenamiento](#1-obtencion-de-datos-y-almacenamiento)
2. [Procesamiento de los Datos JSON a DataFrames y Almacenamiento en Parquet](#2-procesamiento-de-los-datos-json-a-dataframes-y-almacenamiento-en-parquet)
3. [Generación de Profiling de Datos y Análisis](#3-generacion-de-profiling-de-datos-y-analisis)
4. [Análisis del Profiling y Operaciones de Limpieza de Datos](#4-analisis-del-profiling-y-operaciones-de-limpieza-de-datos)
5. [Almacenamiento en Base de Datos y Operaciones de Agregación](#5-almacenamiento-en-base-de-datos-y-operaciones-de-agregacion)
6. [Generación de Diagrama ER del Modelo de Datos](#6-generacion-de-diagrama-er-del-modelo-de-datos)

# 1. Obtención de datos y almacenamiento

El primer paso del proyecto consiste en obtener datos de series emitidas en enero de 2024 desde el API de TVMaze.

URL del API para consulta:
`http://api.tvmaze.com/schedule/web?date=YYYY-MM-DD`

Se creó el script `fetch_data.py` para automatizar la extracción de información diaria durante el mes de enero de 2024. Los datos obtenidos se almacenan en formato JSON en la carpeta `json`.

**Ruta de Almacenamiento de Datos**:
Los datos obtenidos se guardan en la siguiente ruta:
   ```bash
   ./json/shows_january_2024.json
``` 

**Ejecuta el script de obtención de datos**:
   ```bash
   python fetch_data.py
``` 
El archivo JSON con los datos de enero de 2024 se generará en la carpeta json.

# 2. Procesamiento de los Datos JSON a DataFrames y Almacenamiento en Parquet

### Descripción
El archivo `process_data.py` realiza el procesamiento de los datos obtenidos en formato JSON desde el API de TVMaze y los convierte a un formato más eficiente (Parquet) que respeta la integridad de los datos y facilita su manipulación en etapas posteriores. Este paso permite estructurar los datos en un formato tabular usando la librería `pandas`, donde se separan y normalizan los campos clave.

### Archivos Involucrados
- **Archivo JSON**: `./json/shows_january_2024.json` - Archivo JSON con todos los datos de las series emitidas en enero de 2024.
- **Archivo Parquet**: `./data/shows_january_2024.parquet` - Archivo de salida que almacena los datos en formato Parquet.

### Funcionalidades Principales

1. **Carga de Datos desde JSON**  
   La función `load_json_to_dataframe()` utiliza `pd.json_normalize` para convertir los datos anidados del JSON en un DataFrame de `pandas`. Los datos son extraídos y organizados de manera que cada columna represente un atributo importante de los episodios y series, preservando la integridad de los datos originales.

2. **Estructura del DataFrame**  
   Se desglosan y normalizan los siguientes campos:
   - **Campos del Episodio**: Información básica de cada episodio, como `id`, `url`, `name`, `season`, `number`, `type`, `airdate`, `airstamp`, y `runtime`.
   - **Campos del Show**: Detalles específicos del show, incluyendo `average` (rating promedio), `name` (nombre del show), `type`, `language`, `genres`, `status`, `averageRuntime`, `premiered`, `ended`, `officialSite`, y el `webChannel_name`.
   
   Esto permite disponer de un formato estructurado, lo que facilita el análisis de cada show y sus episodios.

3. **Almacenamiento en Formato Parquet**  
   La función `save_to_parquet()` guarda el DataFrame en un archivo Parquet con compresión `snappy`, lo cual optimiza el tamaño y la velocidad de acceso en operaciones futuras.

### Ejecución del Script

Para ejecutar el script y generar el archivo Parquet:
1. Asegúrate de que el archivo JSON se encuentra en la carpeta `json`.
2. Desde el directorio `src`, ejecuta el script:
   ```bash
   python process_data.py

# 3. Generación de Profiling de Datos y Análisis

#### Descripción
Este paso utiliza `pandas-profiling` para generar un reporte exploratorio completo de los datos en formato HTML. El profiling permite realizar un análisis exhaustivo del dataset de shows emitidos en enero de 2024, proporcionando estadísticas y visualizaciones que destacan patrones, correlaciones y posibles problemas de calidad de datos.

### Archivos Involucrados
- **Archivo Parquet**: `./data/shows_january_2024.parquet` - Archivo Parquet generado en el paso anterior, que sirve como fuente de datos para el profiling.
- **Reporte de Profiling**: `./profiling/shows_january_2024_profile.html` - Archivo HTML que contiene el análisis exploratorio detallado del dataset.

### Funcionalidades Principales

1. **Carga de Datos desde Parquet**  
   Los datos se cargan desde el archivo Parquet en un DataFrame de `pandas` para que `pandas-profiling` pueda procesarlos y generar el reporte.

2. **Generación del Reporte de Profiling**  
   La librería `pandas-profiling` se utiliza para crear un informe completo que incluye:
   - **Estadísticas Resumidas**: Número de observaciones, variables, tipos de datos, memoria utilizada, etc.
   - **Distribución de Variables**: Histogramas y distribuciones de cada variable.
   - **Correlación**: Análisis de correlación entre variables numéricas.
   - **Valores Faltantes y Duplicados**: Identificación de datos ausentes y filas duplicadas, para evaluar la calidad del dataset.
   - **Alertas**: Anomalías o patrones inusuales en los datos que podrían necesitar atención.

3. **Almacenamiento del Reporte en HTML**  
   El reporte se guarda en la carpeta `profiling` en formato HTML, lo que permite una fácil navegación y análisis de los resultados en un navegador.

### Ejecución del Script

Para generar el reporte de profiling en HTML:
1. Asegúrate de que el archivo Parquet se encuentra en la carpeta `data`.
2. Desde el directorio `src`, ejecuta el script:
   ```bash
   python profiling_data.py

# 4. Análisis del Profiling y Operaciones de Limpieza de Datos

### Descripción
Con base en el análisis del profiling detallado en `profiling/profiling_analysis.md`, se realizaron las operaciones de limpieza necesarias para asegurar la calidad y consistencia del dataset antes de los análisis. El objetivo es transformar los datos para reducir redundancias, manejar valores faltantes, y corregir outliers, mejorando así su calidad y eficiencia para análisis posteriores.

### Archivo Involucrado
- **Script de Limpieza**: `src/data_cleaning_pipeline.py` - Este script automatiza la limpieza y el procesamiento de los datos de shows para que cumplan con los estándares de calidad definidos en el análisis de profiling.

### Funcionalidades Principales

1. **Eliminación de Variables con Alta Correlación y Baja Cobertura**  
   Basándonos en el análisis de correlación y cobertura de datos, eliminamos columnas redundantes o que presentaban una alta cantidad de datos faltantes, las cuales no aportan valor significativo al análisis.

2. **Conversión de Variables No Soportadas**  
   Se transformaron las variables de tipo lista o JSON (`_embedded_show_genres` y `_embedded_show_image`) a texto para asegurar que el DataFrame sea compatible y manejable en su estructura.

3. **Imputación de Datos Faltantes**  
   Los valores faltantes en variables numéricas y categóricas importantes fueron imputados:
   - `runtime`: Valores faltantes fueron completados con la mediana.
   - `_embedded_show_language`: Valores faltantes fueron completados con la moda.

4. **Tratamiento de Outliers**  
   Para la variable `runtime`, se aplicó una técnica de recorte basada en el rango intercuartílico (IQR) para limitar los valores dentro de un umbral razonable, minimizando el impacto de outliers que podrían sesgar el análisis.

5. **Almacenamiento del Dataset Limpio**  
   El dataset procesado se guarda en formato Parquet con compresión `snappy` en la carpeta `data`, lo que permite una mayor eficiencia de almacenamiento y rapidez en las consultas futuras.

### Ejecución del Script de Limpieza

Para ejecutar el proceso de limpieza y almacenar el DataFrame limpio:
1. Asegúrate de que el archivo `shows_january_2024.parquet` generado en el paso 3 esté disponible en la carpeta `data`.
2. Desde el directorio `src`, ejecuta el siguiente comando:
   ```bash
   python data_cleaning_pipeline.py
### Salida Generada: 
Al ejecutar el script, se generará un nuevo archivo Parquet con los datos limpios en: `./data/shows_january_2024_cleaned.parquet`

# 5. Almacenamiento en Base de Datos y Operaciones de Agregación

### Descripción
En esta sección, los datos limpios fueron almacenados en una base de datos SQLite para realizar operaciones de consulta y agregación de manera eficiente. El modelo de datos fue diseñado para mantener la integridad y relaciones de la información de los shows. Además, se realizaron consultas específicas para obtener información valiosa sobre los shows emitidos en enero de 2024.

### Archivo Involucrado
- **Script de Almacenamiento y Análisis**: `src/data_storage_and_analysis.py` - Este script lee los datos del archivo Parquet limpio, los almacena en una base de datos SQLite, y ejecuta consultas de agregación sobre los datos.

### Pasos Principales

1. **Lectura del Archivo Parquet Limpio**  
   Los datos procesados y guardados en `./data/shows_january_2024_cleaned.parquet` se cargan en un DataFrame de pandas para su posterior almacenamiento en SQLite.

2. **Creación del Modelo de Datos en SQLite**  
   Se define la estructura de la tabla `shows`, que incluye las columnas más importantes del dataset. Esta estructura asegura la integridad de los datos y permite realizar consultas de manera organizada y eficiente. La tabla se crea si no existe en la base de datos `./db/shows_data.db`.

3. **Almacenamiento de los Datos en SQLite**  
   El DataFrame se transfiere a la base de datos SQLite utilizando la función `to_sql`, reemplazando cualquier tabla existente con el mismo nombre. Esto asegura que los datos de cada ejecución se almacenen sin duplicación.

4. **Operaciones de Agregación**  
   Se realizaron varias operaciones de agregación para extraer información relevante de la base de datos:
- **a. Calcular Runtime Promedio (averageRuntime):**  
     Runtime promedio: 44.484547710354164      
    
   
   - **b. Conteo de Shows de TV por Género:**  
        | embedded_show_genres                          | count |
        |-----------------------------------------------|-------|
        | ['Action', 'Adventure', 'Anime', 'Fantasy']   | 51    |
        | ['Action', 'Adventure', 'Anime']              | 35    |
        | ['Action', 'Adventure', 'Children']           | 20    |
        | ['Action', 'Adventure', 'Fantasy']            | 76    |
        | ['Action', 'Adventure', 'Science-Fiction']    | 21    |
        | ['Travel']                                    | 19    |
        | ['War', 'History']                            | 10    |
        | ['War', 'Travel']                             | 2     |
        | ['War']                                       | 2     |
        | []                                            | 1468  |

- **c. Listado de Dominios Únicos del Sitio Oficial de los Shows:**  
   
| Dominios Únicos                           |                       |                       |                        |
|-------------------------------------------|-----------------------|-----------------------|------------------------|
| www.ivi.ru                                 | okko.tv               | wink.ru               | kion.ru                |
| premier.one                                | iview.abc.net.au      | v.qq.com              | v.youku.com            |
| w.mgtv.com                                 | asiapoisk.com         | www.bbc.co.uk         | www.hotstar.com        |
| smotrim.ru                                 | youtube.com           | program.imbc.com      | elisaviihde.fi         |
| play.tv2.no                                | tvn.cjenm.com         | www.amazon.co.uk      | www.viceland.com       |
| www.wowpresentsplus.com                    | www.netflix.com       | www.iq.com            | v.youku.tv             |
| www.paramountplus.com                      | www.youtube.com       | www.primevideo.com    | shahid.mbc.net         |
| discoveryplus.in                           | www.univision.com     | www.cbc.ca            | abcnews.go.com         |
| www.youku.tv                               | www.knowledgekids.ca  | www.peacocktv.com     | roosterteeth.com       |
| watch.wwe.com                              | www.nbcnews.com       | www.cbsnews.com       | tv.nrk.no              |
| rtl.hu                                     | www.tv4play.se        | www.wwe.com           | magnolia.com           |
| m.youku.com                                | vk.com                | viaplay.dk            | www.disneyplus.com     |
| www.amazon.com                             | start.ru              | odekake-kozame.com    | www.iqiyi.com          |
| www.cnn.com                                | www.sbs.com.au        | www.today.com         | www.dropout.tv         |
| www.discoveryplus.com                      | abc.com               | voyo.nova.cz          | www.cwtv.com           |
| twit.tv                                    | www.foxnews.com       | weibo.com             | www.bilibili.com       |
| www.kuaishou.com                           | tv3.ru                | www.srf.ch            | disneynow.com          |
| bleacherreport.com                         | www.pokergo.com       | www.svtplay.se        | www.outtvgo.com        |
| www.ddtpro.com                             | so.youku.com          | www.itv.com           | www.sonyliv.com        |
| www.jiocinema.com                          | www.njpw1972.com      | www.mtv.fi            | ver.movistarplus.es    |
| www.hbomax.com                             | more.tv               | www.britbox.com       | voyo.si                |
| stories.showmax.com                        | www.motortrend.com    | www.dndbeyond.com     | www.alaraby.com        |
| www.blutv.com                              | network.wwe.com       | www.bet.plus          | allblk.tv              |
| www.sundancenow.com                        | www.hulu.com          | www.zdf.de            | www.channel4.com       |
| www.dr.dk                                  | www.tvnow.de          | www.crave.ca          | rosenbergreport.tv     |
| list.youku.com                             | www.tving.com         | www.exxen.com         | v2.videoland.com       |
| www.goplay.be                              | www.facebook.com      | tv.apple.com          | sic.pt                 |
| vidol.tv                                   | www.swearnet.com      | www.sho.com           | app.pureflix.com       |
| www.dailywire.com                          | www.asiasuperyoung.xyz| talesofweddingrings-anime.jp | www.raiplay.it   |
| www.pbs.org                                | amasupercross.com     | vod.tvp.pl            | play.max.com           |
| ukrainer.net                               | www.adweek.com        | www.thezeusnetwork.com | www.gain.tv           |
| www.goldenglobes.com                       | www.5-tv.ru           | discoveryplus.com     | pro-tv.info            |
| www.nta.ua                                 | kusuriyanohitorigoto.jp| kanaten-anime.com     | www.foxbusiness.com    |
| www.bravotv.com                            | www.tv3.dk            | www.atopthefourthwall.com | www.nbc.com        |
| nation.foxnews.com                         | goplay.be             | www.insideofyoupodcast.com | www.shudder.com |
| tubitv.com                                 | wetv.vip              | frieren-anime.jp      | www.nfl.com            |
| sengoku-youko.com                          | www.cc.com            | www.bac.org.il        | www.gagaoolala.com     |
| elcinema.com                               | critrole.com          | www.aetv.com          | infoman.radio-canada.ca|
| www.angel.com                              | www.trueid.net        | vix.com               | simonscat.com          |
| m.youtube.com                              | www.cbs.com           | www.harlemglobetrotters.com | vyzit-v-dubae.tnt-online.ru |
| tnt-online.ru                              | premium.atresplayer.com | www.ufc.com         | sumo.tv2.no            |
| www.mpt.org                                | auvio.rtbf.be         | stopgame.ru           | www.talkvillepodcast.com |
| www.nationalgeographic.com                 | www.stan.com.au       | www.ruutu.fi          | galgos.movistarplus.es |
| skamitalia.timvision.it                    | ici.tou.tv            | www.amazon.in         | www.ardmediathek.de     |
| therokuchannel.roku.com                    | www.max.com           | sympacool.com         | povysaia-gradus.tnt-online.ru |
| viaplay.no                                 | heyqween.tv           | www.sky.com           | plus.rtl.de            |
| seasonvar.ru                               | www.kinopoisk.ru      | vtmgo.be              | www.france.tv          |
| flameserial.ru                             | tv.nova.cz            | vmesteproject.ru      | www.miguvideo.com      |
| independentwrestling.tv                    | www.laisves.tv        | megogo.net            | kurzgesagt.org         |
| tv.line.me                                 | watcha.com            | tv.tv2.dk             | gem.cbc.ca             |
| disneyplus.com                             | www.espn.com          |                       |                        |

### Ejecución del Script de Almacenamiento y Análisis

Para ejecutar el almacenamiento y las consultas de agregación:
1. Asegúrate de que el archivo Parquet limpio (`shows_january_2024_cleaned.parquet`) esté disponible en la carpeta `data`.
2. Desde el directorio `src`, ejecuta el siguiente comando:
   ```bash
   python data_storage_and_analysis.py

# 6. Generación de Diagrama ER del Modelo de Datos

Para visualizar el modelo de datos utilizado en el proyecto, se generó un diagrama ER (Entidad-Relación) a partir de la estructura de la base de datos almacenada en SQLite. Este diagrama ayuda a comprender mejor las relaciones y la integridad de los datos entre las tablas creadas.

El diagrama fue generado usando la librería **ERAlchemy**, que permite crear visualizaciones del esquema de bases de datos en distintos formatos.

#### Script utilizado: `model.py`

**Descripción:**
- El script `model.py` conecta con la base de datos SQLite `shows_data.db` y extrae su esquema para generar una imagen del modelo.
- La imagen generada, `shows_data_schema.png`, se guarda en la carpeta `model/`.

**Ruta de la base de datos y salida de la imagen:**
- Base de datos: `./db/shows_data.db`
- Imagen de salida: `./model/shows_data_schema.png`
> Note:  Instalar la librería ERAlchemy y los requisitos necesarios para la generación del diagrama: 
`pip install eralchemy`.

El archivo de la imagen del diagrama ER puede encontrarse en `model/shows_data_schema.png` para facilitar su visualización.
