# Código - Módulo 01_Preprocesamiento de Datos

Esta carpeta contiene el código Python **completo y funcional** correspondiente a cada uno de los PDFs/tutoriales del módulo de Preprocesamiento de Datos. Los PDFs solo muestran algunas funciones o líneas sueltas de código; aquí está el programa completo, probado y comentado, para que puedas entender de dónde sale cada parte y cómo funciona.

Cada script:
- Tiene un docstring al inicio que indica de qué PDF/guía viene y qué hace.
- Recrea los datos de ejemplo del PDF (tablas chiquitas) o usa los CSV reales del módulo cuando el PDF los menciona.
- Tiene comentarios en cada paso explicando el porqué, no solo el qué.
- Fue ejecutado y verificado (todos corren sin errores, `python3 archivo.py`).

## Estructura

```
Codigo/
├── Leccion2_Manejo_Matrices_Tablas/
│   ├── 01_seleccionar_eliminar_columnas.py   -> Selección/eliminación de columnas y renglones
│   ├── 02_adicion_columnas.py                -> Agregar columnas, concat de filas/columnas
│   └── 03_cambiar_nombre_columnas.py         -> rename() de columnas
│
├── Leccion3_Valores_Perdidos_Atipicos/
│   ├── datos/                                -> Copias de los CSV reales usados por estos scripts
│   ├── 01_manejo_valores_perdidos.py         -> Detección e imputación por inducción (datosFaltantes.csv)
│   ├── 02_imputar_con_medidas_tendencia_central.py -> Imputación con media/mediana/moda (datosCentrales.csv)
│   └── 03_manejo_valores_atipicos.py         -> Detección/corrección/transformación de atípicos (valoresAtipicos.csv), genera gráficas en figuras/
│
├── Leccion4_Evaluacion_Seleccion_Caracteristicas/
│   ├── 01_seleccion_basada_en_correlacion.py -> Correlación, redundancia, relación con la salida, SelectKBest
│   ├── 02_seleccion_metodo_propio_fcbf.py    -> Algoritmo FCBF implementado desde cero (verificado contra el PDF)
│   └── 03_seleccion_automatica_regularizacion.py -> Selección automática con Ridge (regularización)
│
├── Leccion5_Agrupamiento_Separacion/
│   ├── 01_agrupamiento_de_datos.py           -> groupby() en todas sus variantes
│   └── 02_separacion_de_datos.py             -> Separar fechas en año/mes/día (3 métodos)
│
├── Leccion6_Transformacion/
│   ├── 01_escalamiento_caracteristicas.py    -> Max-abs, min-max y estandarización (a mano + scikit-learn)
│   ├── 02_pca_reduccion_dimensiones.py       -> PCA básico (reduce 2D a 1D), genera gráfica en figuras/
│   └── 03_uso_de_funciones_y_encoding.py     -> Potencias, logaritmos, One-Hot Encoding (3 formas), Categorical Encoding
│
└── Leccion7_Conjunto_Datos_Final/
    ├── datos/FIFA2017.csv                    -> Datos reales de 1999 jugadores de FIFA 2017
    ├── 01_creacion_conjunto_datos_FIFA.py     -> Las 4 "misiones" del capstone, con las respuestas correctas del PDF
    └── jugadores2017Final.csv                -> Resultado del script (se genera al correrlo)
```

## Cómo correr un script

Cada script es independiente: solo necesitas Python 3 con pandas, numpy, scikit-learn y matplotlib instalados.

```bash
cd Leccion3_Valores_Perdidos_Atipicos
python3 01_manejo_valores_perdidos.py
```

## Nota importante sobre el Reto (carpeta "Reto")

La carpeta **Reto** (con la rúbrica, las instrucciones y `EmpleadosRETO.csv`) **todavía no se ha resuelto**. Es la evaluación/práctica final del módulo, a la que se llega después de terminar por completo esta carpeta de Código. Se deja pendiente a propósito hasta que decidas empezarla.
