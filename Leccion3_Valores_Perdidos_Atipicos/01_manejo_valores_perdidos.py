"""
Leccion 3 - Manejo de valores perdidos y atipicos
Guia: "Manejo de valores perdidos" + "Como imputar un valor perdido"

Que hace este script:
Usa el archivo real datosFaltantes.csv (carpeta datos/, junto a este script,
copiado del material del curso) para:
  1. Detectar cuantos valores perdidos (NaN) hay y en que columnas
  2. Ver que tan caro es simplemente borrar renglones o columnas con NaN
  3. Imputar los valores perdidos POR INDUCCION (deduciendo el valor correcto
     a partir del patron de los datos), que es la opcion que el PDF prefiere
     antes que usar una medida de tendencia central a ciegas
  4. Usar groupby + transform para recalcular una columna derivada
     (ventas_totales_en_mes) y rellenar el hueco con el valor correcto

Ejecutar desde esta carpeta (o ajustar la ruta de RUTA_CSV) para que
encuentre datos/datosFaltantes.csv.
"""

import os
import pandas as pd

CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_CSV = os.path.join(CARPETA_ACTUAL, "datos", "datosFaltantes.csv")

# ---------------------------------------------------------------------------
# 1. Leer el archivo y colocarlo en el frame 'datos' (igual que el PDF)
# ---------------------------------------------------------------------------
datos = pd.read_csv(RUTA_CSV)
print("Frame 'datos' (datosFaltantes.csv):")
print(datos)

# ---------------------------------------------------------------------------
# 2. Detectar valores perdidos: isna() marca True donde el valor es NaN;
#    sumando por columna obtenemos el total de huecos en cada una.
# ---------------------------------------------------------------------------
huecos_por_columna = pd.isna(datos).sum()
print("\nValores perdidos por columna:")
print(huecos_por_columna)
print(f"\nTotal de valores perdidos en toda la tabla: {huecos_por_columna.sum()}")

# ---------------------------------------------------------------------------
# 3. Ver que tan caro seria simplemente ELIMINAR renglones o columnas con NaN
#    (el PDF lo hace solo para mostrar que no conviene en este caso: se
#    perderia 30% de los renglones o 50% de las columnas).
# ---------------------------------------------------------------------------
na_por_renglon = datos.dropna(axis=0)   # axis=0: quita renglones con algun NaN
na_por_columna = datos.dropna(axis=1)   # axis=1: quita columnas con algun NaN

pct_renglones_perdidos = 100 * (1 - len(na_por_renglon) / len(datos))
pct_columnas_perdidas = 100 * (1 - na_por_columna.shape[1] / datos.shape[1])
print(f"\nSi borramos renglones con NaN, perderiamos {pct_renglones_perdidos:.1f}% de los renglones")
print(f"Si borramos columnas con NaN, perderiamos {pct_columnas_perdidas:.1f}% de las columnas")
print("-> Ambas opciones pierden demasiada informacion; mejor imputar por induccion.")

# ---------------------------------------------------------------------------
# 4. Imputacion POR INDUCCION (deduciendo el dato correcto, no una medida
#    de tendencia central) para las columnas 'mes' y 'mes_id':
#
#    - 'mes' falta en los ejemplos 2 y 11 (indices 1 y 10): por el orden de
#      los meses (enero, ?, marzo...) se deduce que es 'febrero'.
#    - 'mes_id' falta en el ejemplo 5 (indice 4): como el mes es 'mayo',
#      el mes_id correspondiente es 5.
# ---------------------------------------------------------------------------
datos["mes"] = datos["mes"].fillna("febrero")
datos["mes_id"] = datos["mes_id"].fillna(5)

print("\nDespues de imputar 'mes' y 'mes_id' por induccion:")
print(datos)

# ---------------------------------------------------------------------------
# 5. La columna 'ventas_totales_en_mes' es la suma de 'ventas' agrupada por
#    'mes' (cada tienda vendio una cantidad distinta, pero el total del mes
#    es el mismo para todos los renglones de ese mes). Por eso, en vez de
#    imputar con una medida de tendencia central, se recalcula con groupby +
#    transform, y eso ya rellena el hueco con el valor correcto.
# ---------------------------------------------------------------------------
datos["ventas_totales_en_mes"] = datos.groupby("mes")["ventas"].transform("sum")

print("\nDespues de recalcular 'ventas_totales_en_mes' con groupby + transform:")
print(datos)

# ---------------------------------------------------------------------------
# 6. Verificacion final: ya no debe quedar ningun valor perdido
# ---------------------------------------------------------------------------
huecos_finales = pd.isna(datos).sum().sum()
print(f"\nValores perdidos restantes en todo el frame: {huecos_finales}")
assert huecos_finales == 0, "Todavia quedan valores perdidos sin imputar"
print("Listo: todos los valores perdidos de datosFaltantes.csv fueron imputados.")
