"""
Capstone del modulo "01_Preprocesamiento de Datos"
Guia: "Creacion de un adecuado conjunto de datos" (ejercicio de 4 misiones)

Que hace este script:
Es el ejercicio practico ("4 misiones") que integra TODAS las tecnicas de
preprocesamiento vistas en el modulo (seleccion/eliminacion de columnas,
manejo de valores perdidos y atipicos, creacion de columnas, One-Hot
Encoding y seleccion por correlacion), aplicadas sobre datos REALES de
1999 jugadores de FIFA 2017 (archivo datos/FIFA2017.csv).

Este script implementa, en orden, las RESPUESTAS CORRECTAS que el propio
PDF da al final (seccion "Respuestas y retroalimentacion") para cada una
de las 4 misiones -- no son datos inventados ni un ejercicio sin resolver:
son exactamente las instrucciones que el documento marca como correctas,
con comentarios explicando el porque de cada paso (incluyendo por que las
otras opciones del PDF eran incorrectas, cuando es util saberlo).

Mision 1: Cargar el CSV a un frame llamado jugadores2017.
Mision 2: Eliminar columnas irrelevantes, imputar valores perdidos y
          eliminar valores atipicos de Rating.
Mision 3: Crear columnas nuevas (edad, limpiar Height/Weight) y generar
          Club_Position_OH via One-Hot Encoding.
Mision 4: Quedarse solo con columnas numericas relevantes, revisar
          correlacion de las columnas dudosas contra Rating, eliminar las
          de correlacion baja, y guardar jugadores2017Final.csv.
"""

import pandas as pd

# ---------------------------------------------------------------------------
# MISION 1: Cargar el archivo FIFA2017.csv al frame 'jugadores2017'
# ---------------------------------------------------------------------------
# Respuesta correcta del PDF (opcion b):
#   import pandas as pd
#   jugadores2017 = pd.read_csv("FIFA2017.csv")
# (la opcion 'a' no asignaba el resultado a ninguna variable, y la 'c' no
# importaba pandas antes de usarlo)
import os
RUTA_CSV = os.path.join(os.path.dirname(__file__), "datos", "FIFA2017.csv")
jugadores2017 = pd.read_csv(RUTA_CSV)

print(f"Mision 1 lista: frame 'jugadores2017' cargado con shape {jugadores2017.shape} "
      "(1999 jugadores, 30 caracteristicas).")

# ---------------------------------------------------------------------------
# MISION 2: Eliminar columnas irrelevantes, imputar valores perdidos y
#           eliminar valores atipicos
# ---------------------------------------------------------------------------
# --- Ejercicio 1: eliminar columnas irrelevantes (respuesta 'a' del PDF) ---
# Columnas incompletas (la mayoria de jugadores no tiene seleccion nacional):
jugadores2017 = jugadores2017.drop(["National_Position", "National_Kit"], axis=1)
# Columnas muy particulares de cada jugador, que no ayudan a predecir Rating:
jugadores2017.drop(
    ["Player_ID", "Club_Kit", "Club_Joining", "Contract_Expiry"],
    axis=1, inplace=True,
)
print(f"\nMision 2 (ejercicio 1) lista: columnas irrelevantes eliminadas. "
      f"Quedan {jugadores2017.shape[1]} columnas.")

# --- Ejercicio 2: imputar valores perdidos y quitar valores atipicos ---
# (respuesta 'a' del PDF)
print("\nValores perdidos por columna (antes de imputar):")
print(pd.isna(jugadores2017).sum()[pd.isna(jugadores2017).sum() > 0])

# 'Height' llega como texto con una 'm' al final (ej. "1.78 m"); hay que
# quitar los ultimos 2 caracteres (" m") y convertir a float ANTES de poder
# imputarla con la media (si se intenta sacar la media de un string, falla).
jugadores2017["Height"] = jugadores2017["Height"].str[0:-2].astype(float)

# Imputacion con la medida de tendencia central adecuada segun el tipo de
# cada variable: moda para categoricas, mediana para enteras, media para
# flotantes (igual que se vio en Leccion 3).
#
# Nota tecnica: el PDF escribe esto como
#   jugadores2017['columna'].fillna(valor, inplace=True)
# Eso funcionaba en versiones anteriores de Pandas, pero en las versiones
# recientes (con "Copy-on-Write" activado, que es el comportamiento por
# default desde Pandas 2.x/3.x) ese patron opera sobre una COPIA temporal
# de la columna y el cambio NUNCA llega al frame original (Pandas incluso
# avisa esto con un ChainedAssignmentError). Por eso aqui se usa la forma
# recomendada y equivalente: reasignar la columna completa con
# jugadores2017['columna'] = jugadores2017['columna'].fillna(valor)
jugadores2017["Club_Position"] = jugadores2017["Club_Position"].fillna(
    jugadores2017["Club_Position"].value_counts().idxmax()
)  # categorica -> moda (aqui usando value_counts().idxmax(), equivalente a mode().iat[0])
jugadores2017["Preffered_Foot"] = jugadores2017["Preffered_Foot"].fillna(
    jugadores2017["Preffered_Foot"].mode().iat[0]
)  # categorica -> moda
jugadores2017["Height"] = jugadores2017["Height"].fillna(jugadores2017["Height"].mean())  # flotante -> media
jugadores2017["Interceptions"] = jugadores2017["Interceptions"].fillna(jugadores2017["Interceptions"].median())  # entera -> mediana
jugadores2017["Strength"] = jugadores2017["Strength"].fillna(jugadores2017["Strength"].median())  # entera -> mediana

print("\nValores perdidos por columna (despues de imputar):")
print(pd.isna(jugadores2017).sum()[pd.isna(jugadores2017).sum() > 0].rename("deberia salir vacio"))

# Deteccion/eliminacion de valores atipicos en 'Rating' por el metodo de
# "media +/- N desviaciones estandar" (visto en Leccion 3), con factor=3.
print("\ndescribe() de las columnas numericas (para revisar valores atipicos):")
print(jugadores2017.describe())

factor = 3
upper_lim = jugadores2017["Rating"].mean() + jugadores2017["Rating"].std() * factor
lower_lim = jugadores2017["Rating"].mean() - jugadores2017["Rating"].std() * factor
# Nota: el PDF usa & (Y lógico) para quedarse con los datos DENTRO del
# rango. Usar | (O lógico) por error, como muestran las opciones
# incorrectas del PDF, selecciona lo de AFUERA del rango (justo lo
# contrario de lo que se busca).
filas_antes = len(jugadores2017)
jugadores2017 = jugadores2017[
    (jugadores2017["Rating"] < upper_lim) & (jugadores2017["Rating"] > lower_lim)
]
print(f"\nMision 2 (ejercicio 2) lista: se eliminaron {filas_antes - len(jugadores2017)} "
      f"jugadores con Rating atipico (fuera de [{lower_lim:.2f}, {upper_lim:.2f}]). "
      f"Quedan {len(jugadores2017)} jugadores.")

# ---------------------------------------------------------------------------
# MISION 3: Agregar columnas nuevas (edad, limpiar Height/Weight, One-Hot)
# ---------------------------------------------------------------------------
# (respuesta 'b' del PDF)
# 'Birth_Date' es un STRING, no se puede restar directamente de 2017 (un
# entero); primero hay que extraer el anio de nacimiento con DatetimeIndex.
jugadores2017["año_nacimiento"] = pd.DatetimeIndex(jugadores2017["Birth_Date"]).year
jugadores2017["edad"] = 2017 - jugadores2017["año_nacimiento"]

# 'Weight' llega como texto con "kg" al final (ej. "65 kg"); los primeros 2
# caracteres son el numero, por lo que basta tomar str[:2] y convertir a int
# (Height ya se limpio en la Mision 2, pero aqui se repite la logica por
# si este script se corriera de forma independiente desde este punto).
jugadores2017["Weight"] = jugadores2017["Weight"].str[:2].astype(int)

# One-Hot Encoding de 'Club_Position' (categorica -> varias columnas
# binarias), quitando la primera columna automaticamente con
# drop_first=True porque es redundante (si todas las demas columnas son 0,
# ya se sabe que esa categoria es la que faltaba, sin necesidad de guardarla).
Club_Position_OH = pd.get_dummies(jugadores2017["Club_Position"], drop_first=True)
# Para poder usar estas columnas numericas mas adelante en la Mision 4, se
# agrega al frame principal una version resumida en forma de codigo entero
# (0, 1, 2...) por categoria, llamada 'Club_Pos_Num' (el PDF la menciona en
# la Mision 4 como ya existente; aqui se genera a partir de la version
# categorica, usando el mismo truco de Leccion 6: .cat.codes).
jugadores2017["Club_Pos_Num"] = jugadores2017["Club_Position"].astype("category").cat.codes

print(f"\nMision 3 lista: columnas 'edad', 'Height'/'Weight' limpias, y "
      f"'Club_Pos_Num' creadas. Club_Position_OH tiene shape {Club_Position_OH.shape} "
      "(One-Hot con la primera categoria eliminada).")

# ---------------------------------------------------------------------------
# MISION 4: Quedarse solo con columnas numericas relevantes, revisar
#           correlacion y guardar el archivo final
# ---------------------------------------------------------------------------
# (respuesta 'a' del PDF)
# Se arma el frame final con todas las variables de habilidad (que se
# asume que SI importan para el Rating) + las 4 columnas creadas por
# nosotros, de las que SI tenemos dudas: 'edad', 'Club_Pos_Num', 'Height'
# y 'Weight'.
jugadores2017Final = jugadores2017[[
    "Height", "Weight", "Weak_foot", "Ball_Control", "Dribbling", "Marking",
    "Attacking_Position", "Interceptions", "Short_Pass", "Long_Pass",
    "Acceleration", "Speed", "Strength", "Agility", "Jumping", "Heading",
    "Shot_Power", "Curve", "Rating", "edad", "Club_Pos_Num",
]]

# Se revisa la correlacion lineal de cada una de las 4 columnas dudosas
# contra 'Rating' (la variable de salida que se quiere predecir).
corr_edad = jugadores2017Final["Rating"].corr(jugadores2017Final["edad"])
corr_club_pos = jugadores2017Final["Rating"].corr(jugadores2017Final["Club_Pos_Num"])
corr_height = jugadores2017Final["Rating"].corr(jugadores2017Final["Height"])
corr_weight = jugadores2017Final["Rating"].corr(jugadores2017Final["Weight"])

print("\nCorrelacion de cada variable dudosa con 'Rating':")
print(f"  edad:         {corr_edad:.4f}")
print(f"  Club_Pos_Num: {corr_club_pos:.4f}")
print(f"  Height:       {corr_height:.4f}")
print(f"  Weight:       {corr_weight:.4f}")

# Umbral del PDF: se elimina toda variable (de las 4 dudosas) cuya
# |correlacion| con Rating sea menor a 0.07. Segun el PDF, solo 'Height'
# cae por debajo de ese umbral (correlacion ~0.04) y debe eliminarse;
# 'edad', 'Club_Pos_Num' y 'Weight' se quedan.
UMBRAL_CORRELACION = 0.07
columnas_dudosas = {
    "Height": corr_height, "Weight": corr_weight,
    "edad": corr_edad, "Club_Pos_Num": corr_club_pos,
}
columnas_a_eliminar = [
    col for col, corr in columnas_dudosas.items() if abs(corr) < UMBRAL_CORRELACION
]
print(f"\nColumnas con |correlacion| < {UMBRAL_CORRELACION} (se eliminan): {columnas_a_eliminar}")

jugadores2017Final = jugadores2017Final.drop(columnas_a_eliminar, axis=1)

# Se guarda el resultado final, listo para usarse en un modelo de Machine
# Learning que prediga el Rating de un jugador.
RUTA_SALIDA = os.path.join(os.path.dirname(__file__), "jugadores2017Final.csv")
jugadores2017Final.to_csv(RUTA_SALIDA, index=False)

print(f"\nMision 4 lista: frame final con shape {jugadores2017Final.shape} "
      f"guardado en: {RUTA_SALIDA}")
print(f"Columnas finales: {list(jugadores2017Final.columns)}")

print("\nListo: las 4 misiones del capstone 'Creacion de un adecuado conjunto "
      "de datos' fueron resueltas sobre datos reales de FIFA2017.csv.")
