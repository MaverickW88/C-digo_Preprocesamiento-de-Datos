"""
Leccion 4 - Evaluacion y seleccion de caracteristicas
Guia: "Metodos de seleccion basados en correlacion"

Que hace este script:
  1. Reproduce el ejemplo del PDF con las columnas X,Y (alta correlacion
     lineal) y Z,W (correlacion casi nula), usando los mismos valores que
     aparecen en el documento, para poder comparar resultados.
  2. Calcula el coeficiente de correlacion de Pearson entre pares de
     variables (serie.corr(serie)) y la matriz de correlacion completa
     (frame.corr()).
  3. Muestra el criterio para declarar "variables redundantes" (correlacion
     alta entre dos variables de entrada) y "variable poco relacionada con
     la salida" (correlacion baja con la variable de salida).
  4. Reproduce el ejemplo de seleccion automatica con SelectKBest de
     scikit-learn sobre el dataset de digitos (load_digits).
"""

import pandas as pd
from sklearn.datasets import load_digits
from sklearn.feature_selection import SelectKBest, f_classif

# ---------------------------------------------------------------------------
# 1. Recrear el frame 'datos' con las 4 columnas del ejemplo del PDF
# ---------------------------------------------------------------------------
datos = pd.DataFrame({
    "X": [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 1.0],
    "Y": [0.5712, 0.9758, 1.1613, 1.1948, 1.4789, 1.7980, 1.9983, 2.1510, 2.3037, 2.4097],
    "Z": [0.0761, 0.0116, 0.5570, 0.5693, 0.6364, 0.9790, 0.4309, 0.0831, 0.2618, 0.2555],
    "W": [0.7452, 0.1669, 0.6938, 0.1939, 0.3526, 0.6706, 0.4059, 0.5279, 0.2650, 0.2770],
})
print("Frame de ejemplo:")
print(datos)

# ---------------------------------------------------------------------------
# 2. Correlacion de Pearson entre dos series especificas (serie.corr(serie))
# ---------------------------------------------------------------------------
corr_xy = datos["X"].corr(datos["Y"])
corr_zw = datos["Z"].corr(datos["W"])
print(f"\nCorrelacion X-Y (deberia ser ~0.9904, alta): {corr_xy:.4f}")
print(f"Correlacion Z-W (deberia ser ~0.2289, baja):  {corr_zw:.4f}")

# El orden de las variables no importa: corr es simetrica
assert round(datos["X"].corr(datos["Y"]), 6) == round(datos["Y"].corr(datos["X"]), 6)

# ---------------------------------------------------------------------------
# 3. Matriz de correlacion completa del frame (frame.corr())
# ---------------------------------------------------------------------------
matriz_corr = datos.corr()
print("\nMatriz de correlacion completa (simetrica, diagonal = 1.0):")
print(matriz_corr)

# ---------------------------------------------------------------------------
# 4. Criterio de "variables redundantes": correlacion absoluta alta (>= 0.7
#    es un umbral comun, pero depende del problema) entre dos variables de
#    ENTRADA. Si X y Y tienen 0.99 de correlacion, son redundantes: se
#    puede eliminar una de las dos sin perder casi informacion.
# ---------------------------------------------------------------------------
UMBRAL_REDUNDANCIA = 0.7
print(f"\n¿X y Y son redundantes (|corr| >= {UMBRAL_REDUNDANCIA})?", abs(corr_xy) >= UMBRAL_REDUNDANCIA)
print(f"¿Z y W son redundantes (|corr| >= {UMBRAL_REDUNDANCIA})?", abs(corr_zw) >= UMBRAL_REDUNDANCIA)

# ---------------------------------------------------------------------------
# 5. Criterio de "poca relacion con la salida": si existiera una variable de
#    salida, se calcula su correlacion con cada variable de entrada y se
#    elimina la que quede por debajo de un umbral (el PDF menciona valores
#    tipicos entre 0.2 y 0.5, segun el problema).
# ---------------------------------------------------------------------------
UMBRAL_RELACION_SALIDA = 0.2


def variables_a_mantener(frame, columna_salida, umbral=UMBRAL_RELACION_SALIDA):
    """Regresa la lista de columnas de entrada cuya correlacion absoluta con
    la columna de salida es >= umbral (las demas se eliminarian)."""
    correlaciones = frame.corr()[columna_salida].drop(columna_salida)
    return correlaciones[correlaciones.abs() >= umbral].index.tolist()


# Usamos 'Y' como si fuera la salida, solo para ilustrar el criterio:
mantener = variables_a_mantener(datos, "Y")
print(f"\nSi 'Y' fuera la salida, se mantendrian (|corr| >= {UMBRAL_RELACION_SALIDA}): {mantener}")

# ---------------------------------------------------------------------------
# 6. Seleccion automatica con SelectKBest (scikit-learn), sobre el dataset
#    de digitos escritos a mano (1797 imagenes de 8x8 pixeles).
# ---------------------------------------------------------------------------
X, y = load_digits(return_X_y=True, as_frame=True)
print(f"\nDataset de digitos: X tiene forma {X.shape}, y se llama '{y.name}'")
print("Primeras 5 columnas:", list(X.columns[0:5]))
print("Primeros 2 valores de salida:", list(y)[0:2])

# SelectKBest(k=20) con la funcion de evaluacion por default (f_classif, para
# variable de salida discreta / clasificacion), nos quedamos con los 20
# pixeles mas relevantes para predecir el digito.
X_new = SelectKBest(f_classif, k=20).fit_transform(X, y)
print(f"\nSelectKBest(f_classif, k=20): de {X.shape[1]} columnas originales, "
      f"nos quedamos con {X_new.shape[1]}")

print("\nListo: correlacion de Pearson, matriz de correlacion, criterios de "
      "redundancia/relacion con la salida y SelectKBest probados.")
