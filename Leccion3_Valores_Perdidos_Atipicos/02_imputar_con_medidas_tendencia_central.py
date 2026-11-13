"""
Leccion 3 - Manejo de valores perdidos y atipicos
Guia: "Manejo de valores perdidos" (seccion "La ayuda de las medidas de
tendencia central")

Que hace este script:
Usa el archivo real datosCentrales.csv (carpeta datos/) para mostrar CUANDO
usar cada medida de tendencia central al imputar valores perdidos:
  - Datos continuos (reales)              -> imputar con la MEDIA
  - Datos discretos contables (enteros)   -> imputar con la MEDIANA
  - Datos discretos categoricos           -> imputar con la MODA

En este dataset:
  - 'sueldo'                 es continuo  -> media
  - 'calificacion_servicio'  es categorico -> moda
  - 'antiguedad'             es entero (anios en la empresa) -> mediana
  - 'comentarios_adicionales' tambien es categorico -> se imputa con moda
    como criterio adicional (el PDF solo la menciona, no la resuelve; aqui
    se completa el mismo criterio para dejar el frame sin huecos)
"""

import os
import pandas as pd

CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_CSV = os.path.join(CARPETA_ACTUAL, "datos", "datosCentrales.csv")

# ---------------------------------------------------------------------------
# 1. Leer el archivo y colocarlo en el frame 'datos1' (igual que el PDF)
# ---------------------------------------------------------------------------
datos1 = pd.read_csv(RUTA_CSV)
print("Frame 'datos1' (datosCentrales.csv):")
print(datos1)

# ---------------------------------------------------------------------------
# 2. Revisar cuantos valores perdidos hay por columna
# ---------------------------------------------------------------------------
print("\nValores perdidos por columna:")
print(pd.isna(datos1).sum())

# ---------------------------------------------------------------------------
# 3. 'sueldo' es una variable CONTINUA (numeros reales) -> imputar con la
#    MEDIA. fillna(datos1.mean()) aplicado asi imputaria la media de TODAS
#    las columnas numericas; aqui se hace columna por columna para que
#    quede explicito y no se mezclen criterios por accidente.
# ---------------------------------------------------------------------------
media_sueldo = datos1["sueldo"].mean()
datos1["sueldo"] = datos1["sueldo"].fillna(media_sueldo)
print(f"\nMedia de 'sueldo' usada para imputar: {media_sueldo:.4f}")
print(datos1[["id_vendedor", "sueldo"]])

# ---------------------------------------------------------------------------
# 4. 'calificacion_servicio' es CATEGORICA -> imputar con la MODA.
#    .mode() puede regresar mas de un valor si hay empate; .iat[0] toma el
#    primero, tal como indica el PDF.
# ---------------------------------------------------------------------------
moda_calificacion = datos1["calificacion_servicio"].mode().iat[0]
datos1["calificacion_servicio"] = datos1["calificacion_servicio"].fillna(moda_calificacion)
print(f"\nModa de 'calificacion_servicio' usada para imputar: '{moda_calificacion}'")
print(datos1[["id_vendedor", "calificacion_servicio"]])

# ---------------------------------------------------------------------------
# 5. 'antiguedad' es DISCRETA CONTABLE (anios, numeros enteros) -> imputar
#    con la MEDIANA, para garantizar que el valor imputado siga siendo un
#    entero razonable (la media podria dar un valor con decimales).
# ---------------------------------------------------------------------------
mediana_antiguedad = datos1["antiguedad"].median()
datos1["antiguedad"] = datos1["antiguedad"].fillna(mediana_antiguedad)
print(f"\nMediana de 'antiguedad' usada para imputar: {mediana_antiguedad}")
print(datos1[["id_vendedor", "antiguedad"]])

# ---------------------------------------------------------------------------
# 6. 'comentarios_adicionales' tambien es categorica -> mismo criterio de
#    moda, para dejar el frame completo sin valores perdidos.
# ---------------------------------------------------------------------------
moda_comentarios = datos1["comentarios_adicionales"].mode().iat[0]
datos1["comentarios_adicionales"] = datos1["comentarios_adicionales"].fillna(moda_comentarios)
print(f"\nModa de 'comentarios_adicionales' usada para imputar: '{moda_comentarios}'")

# ---------------------------------------------------------------------------
# 7. Verificacion final
# ---------------------------------------------------------------------------
print("\nFrame final, sin valores perdidos:")
print(datos1)
huecos_finales = pd.isna(datos1).sum().sum()
print(f"\nValores perdidos restantes: {huecos_finales}")
assert huecos_finales == 0, "Todavia quedan valores perdidos sin imputar"
print("Listo: datosCentrales.csv imputado usando media / mediana / moda segun el tipo de dato.")
