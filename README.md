# DataEngineers

  # Análisis y Limpieza del Dataset de Series de TV
 
  ## Índice
 
  1. Resumen del Dataset
  2. Variables Numéricas Clave
  - id
  - rating_average
  - runtime
  3. Variables Categóricas y de Texto
  4. Alertas de Correlación y Redundancia
  5. Datos Faltantes y Valores Cero
  6. Resumen de Estrategia de Limpieza
 
  ---
 
  ### Resumen del Dataset
 
  Descripción general del conjunto de datos:
  - Número de variables: 66
  - Número de observaciones: 4733
  - Porcentaje de celdas faltantes: 39.1%
  - Tamaño total en memoria: 16.4 MiB
  - Tamaño promedio de cada registro: 3.6 KiB
 
  Tipos de datos principales:
  - Numéricas: 15
  - URLs: 13
  - Texto: 12
  - Categóricas: 14
  - Fecha y Hora: 4
  - No soportadas: 8
 
  Nota: Las variables de tipo URL, Texto y "No soportadas" se revisarán más adelante para decidir si deben convertirse o eliminarse.
 
  ---
 
  ### Variables Numéricas Clave