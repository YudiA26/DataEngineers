# Análisis y Estrategia de Limpieza del Dataset

Este README documenta el análisis, las observaciones clave y la estrategia de limpieza para un dataset de shows emitidos en enero de 2024. La estrategia se basa en un análisis inicial de perfilado de datos y está diseñada para mejorar la calidad y usabilidad del conjunto de datos para futuros análisis.

---

## Índice

1. [Resumen del Dataset](#resumen-del-dataset)
2. [Análisis de Variables Numéricas Clave](#análisis-de-variables-numéricas-clave)
   - `ID`
   - `rating_average`
   - `runtime`
3. [Variables Categóricas y de Texto](#variables-categóricas-y-de-texto)
   - `_embedded_show_language`
   - `_embedded_show_genres`
4. [Alertas de Correlación y Redundancia](#alertas-de-correlación-y-redundancia)
5. [Datos Faltantes y Valores Cero](#datos-faltantes-y-valores-cero)
6. [Resumen y Estrategia de Limpieza](#resumen-y-estrategia-de-limpieza)

---

### Resumen del Dataset

**Número de Variables y Observaciones**  
- **66 variables** con **4,733 observaciones**. El dataset es amplio y contiene variables detalladas sobre las características de cada show.

**Porcentaje de Datos Faltantes**  
- **39.1%** de celdas faltantes indica una cantidad considerable de datos incompletos. La estrategia de limpieza dependerá de la relevancia de estas variables para el análisis.

**Tamaño y Eficiencia en Memoria**  
- **Tamaño total**: 16.4 MiB, con un **tamaño promedio de 3.6 KiB** por registro. Aunque es manejable, reducir el número de variables redundantes podría optimizar aún más el uso de memoria.

**Tipos de Variables**  
- **Numéricas**: 15
- **URLs**: 13
- **Texto**: 12
- **Categóricas**: 14
- **Fecha y Hora**: 4
Las variables URL, Texto y No Soportadas requieren inspección adicional para decidir si deben incluirse o excluirse del análisis.

---

### Análisis de Variables Numéricas Clave

#### `ID`
- **Valores Únicos (100%)**: Sin datos faltantes ni valores extremos. Esta columna es ideal como clave primaria.

#### `rating_average`
- **Datos faltantes**: **92.8%**. Esto implica que la mayoría de los registros no tienen calificación.
- **Distribución**:
  - **Media**: 7.49
  - **Desviación estándar**: 1.22
  - **Sesgo**: Negativo (Curtosis: 2.0)
  - **Rango**: 3 a 10, con una **IQR** de 1.6, lo que indica baja variabilidad.
- **Recomendación**: Imputar valores faltantes con la media o mediana, o considerar agrupar datos por géneros y completar los valores basados en tendencias observadas.

#### `runtime`
- **Datos faltantes**: **9.4%**
- **Distribución y valores extremos**:
  - **Rango**: 1 a 300 minutos, con una media de 44.4 y una desviación estándar de 43.7.
  - **Sesgo**: Alto (3.06) con curtosis elevada (11.71), indicando outliers.
- **Recomendación**: Imputar valores faltantes con la mediana o métodos avanzados (p. ej., kNN). Considerar el recorte de valores extremos si resultan ruidosos.

---

### Variables Categóricas y de Texto

#### `_embedded_show_language`
- **Distribución y Valores Dominantes**:
  - **Idiomas más comunes**: Inglés (1,635), Chino (1,506)
  - **Datos faltantes**: 6.5%
- **Recomendación**: Imputar valores faltantes con "Unknown" o la moda. Esta variable puede ser útil para agrupar el análisis de calificaciones y géneros.

---

### Alertas de Correlación y Redundancia

**Variables Altamente Correlacionadas**  
Algunas variables, como `_embedded_show_averageRuntime`, `_embedded_show_network_country_code` y `_embedded_show_externals_tvrage`, presentan correlaciones altas con otras variables, lo cual sugiere redundancia o dependencia. Algunas correlaciones clave incluyen:

- **`rating_average`** y `runtime` correlacionadas con variables de país y plataforma, lo cual puede informar segmentaciones.
  
**Recomendación**  
Considerar eliminar o consolidar variables altamente correlacionadas que no aporten información adicional. Para análisis predictivos, aplicar una técnica de reducción de dimensionalidad como PCA.

---

### Datos Faltantes y Valores Cero

**Variables con Alta Cantidad de Datos Faltantes**  
Algunas variables, como `image`, `summary`, `_embedded_show_network`, `_embedded_show_dvdCountry`, y `rating_average`, presentan más del 60% de datos faltantes.

**Variables Desbalanceadas**  
- Variables como `_embedded_show_schedule_time` y `type` presentan desbalance extremo, lo que podría sesgar el análisis si no se corrige.

**Valores Cero**  
- **`_embedded_show_weight`**: 2.9% de valores cero. Revisar si estos valores son válidos o si representan errores en los datos.

**Recomendación**  
- **Eliminar** variables con más del 80% de datos faltantes.
- **Imputar** las variables faltantes importantes con valores calculados o constantes.
- **Revisar** la variable `_embedded_show_weight` para verificar si los valores cero son significativos.

---

### Resumen y Estrategia de Limpieza

1. **Eliminar Variables con Alta Correlación y Datos Faltantes**  
   - Considera eliminar `_embedded_show_network` y otras variables de alta correlación y baja cobertura.

2. **Convertir Variables No Soportadas**  
   - **`_embedded_show_genres`** y **`_embedded_show_image`** deben convertirse a texto o analizarse para decidir su relevancia.

3. **Detección y Tratamiento de Outliers**  
   - En `runtime`, donde existen outliers, aplicar métodos de suavizado o eliminar outliers con base en cuartiles.
