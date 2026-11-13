"""
Leccion 2 - Manejo de matrices y tablas
Guia: "Cambiar nombre a columnas"

Que hace este script:
Muestra, con el mismo frame 'hoteles' usado en el primer tutorial de esta
leccion, como cambiar el nombre de una o varias columnas con el metodo
rename(), que es mucho mas simple y eficiente que la alternativa de
"crear columna nueva + borrar la vieja".
"""

import pandas as pd

# ---------------------------------------------------------------------------
# 1. Recrear el frame "hoteles" (igual que en 01_seleccionar_eliminar_columnas.py)
# ---------------------------------------------------------------------------
hoteles = pd.DataFrame({
    "nombre": ["Gran X", "Colonial", "The Bridge"],
    "ciudad": ["Cancun", "Barranquilla", "Portland"],
    "estado": ["Quintana Roo", "Atlantico", "Oregon"],
    "pais": ["Mexico", "Colombia", "USA"],
    "habitacion": ["doble", "sencilla", "sencilla"],
    "precio": [3250, 1500, 2500],
    "estrellas": [5, 4, 3],
    "playa": ["si", "no", "no"],
})
print("Frame original 'hoteles':")
print(hoteles)

# ---------------------------------------------------------------------------
# 2. La forma "larga" que el PDF menciona pero NO recomienda (solo como
#    referencia, para entender por que rename() es mejor):
#    1) crear una columna nueva copiando la vieja
#    2) borrar la columna vieja
# ---------------------------------------------------------------------------
hoteles_forma_larga = hoteles.copy()
hoteles_forma_larga["No. de estrellas"] = hoteles_forma_larga["estrellas"]
hoteles_forma_larga = hoteles_forma_larga.drop("estrellas", axis=1)
print("\nMismo resultado, pero por el camino largo (copiar + borrar):")
print(hoteles_forma_larga)

# ---------------------------------------------------------------------------
# 3. La forma recomendada: rename(columns={...})
#    rename() recibe un diccionario {nombre_actual: nombre_nuevo}.
#    Por default NO modifica el frame original, regresa uno nuevo.
# ---------------------------------------------------------------------------
hoteles_renombrado = hoteles.rename(columns={"estrellas": "No. de estrellas"})
print("\nFrame con 'estrellas' renombrada a 'No. de estrellas' (rename):")
print(hoteles_renombrado)
print("El frame original 'hoteles' sigue con el nombre viejo:", "estrellas" in hoteles.columns)

# ---------------------------------------------------------------------------
# 4. Para que el cambio se quede en el propio frame hay dos formas:
#    a) Reasignar el resultado al mismo frame
#    b) Usar el parametro inplace=True
# ---------------------------------------------------------------------------
hoteles_a = hoteles.copy()
hoteles_a = hoteles_a.rename(columns={"estrellas": "No. de estrellas"})  # (a) reasignando

hoteles_b = hoteles.copy()
hoteles_b.rename(columns={"estrellas": "No. de estrellas"}, inplace=True)  # (b) inplace=True

print("\n(a) Reasignando:")
print(hoteles_a.columns.tolist())
print("(b) Con inplace=True:")
print(hoteles_b.columns.tolist())

# ---------------------------------------------------------------------------
# 5. Renombrar VARIAS columnas a la vez: solo se agregan mas pares al
#    diccionario.
# ---------------------------------------------------------------------------
hoteles_varios = hoteles.rename(
    columns={"pais": "Pais", "ciudad": "Ciudad"}, inplace=False
)
print("\nVarias columnas renombradas a la vez ('pais'->'Pais', 'ciudad'->'Ciudad'):")
print(hoteles_varios)

print("\nListo: cambio de nombre de columnas, individual y en lote, probado.")
