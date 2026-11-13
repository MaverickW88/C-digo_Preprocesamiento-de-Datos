"""
Leccion 2 - Manejo de matrices y tablas
Guia: "Adicion de columnas a una tabla"

Que hace este script:
Reproduce, con el mismo frame de ejemplo del PDF (un grupo de 4 alumnos,
`grupoDS`), las distintas formas de agregar columnas a un frame de Pandas:
  1. Crear una columna con una expresion (ej. calificacion final)
  2. Crear una columna con un valor predefinido (el mismo valor para todos)
  3. Crear una columna con valores especificos (una lista)
  4. assign() e insert() como alternativas a la asignacion directa
  5. Concatenar renglones de un frame a otro (pd.concat, axis=0)
  6. Concatenar columnas de un frame a otro / "joining" (pd.concat, axis=1)
  7. Los dos tipos de join: outer (union) e inner (interseccion)

No usa ningun CSV del curso; el PDF arma el ejemplo a mano, asi que aqui se
recrea la misma tabla para poder correr el archivo de forma independiente.
"""

import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# 1. Recrear el frame "grupoDS" del PDF (4 alumnos: Examen y Proyecto)
# ---------------------------------------------------------------------------
grupoDS = pd.DataFrame({
    "Nombre": ["Paulina", "Norberto", "Julia", "Mario"],
    "Examen": [97, 85, 86, 91],
    "Proyecto": [95, 95, 90, 90],
})
print("Frame original 'grupoDS':")
print(grupoDS)

# ---------------------------------------------------------------------------
# 2. Nueva columna con una EXPRESION (50% examen + 50% proyecto)
# ---------------------------------------------------------------------------
grupoDS["Final"] = 0.5 * grupoDS["Examen"] + 0.5 * grupoDS["Proyecto"]
print("\nFrame con la columna 'Final' (expresion aritmetica):")
print(grupoDS)

# ---------------------------------------------------------------------------
# 3. Nueva columna con un VALOR PREDEFINIDO (mismo valor para todos)
# ---------------------------------------------------------------------------
grupoDS["Grupo"] = 1
print("\nFrame con la columna 'Grupo' (valor fijo para todos):")
print(grupoDS)

# ---------------------------------------------------------------------------
# 4. Nueva columna con VALORES ESPECIFICOS (una lista, uno por renglon)
# ---------------------------------------------------------------------------
grupoDS["Apellido"] = ["Perez", "Lopez", "Hernandez", "Garcia"]
print("\nFrame con la columna 'Apellido' (lista de valores):")
print(grupoDS)

# ---------------------------------------------------------------------------
# 5. Metodo assign(): igual que la asignacion directa, agrega al final y
#    regresa un frame NUEVO (no modifica el original).
# ---------------------------------------------------------------------------
grupoDS_base = pd.DataFrame({
    "Nombre": ["Paulina", "Norberto", "Julia", "Mario"],
    "Examen": [97, 85, 86, 91],
    "Proyecto": [95, 95, 90, 90],
})
nuevo_frame_assign = grupoDS_base.assign(
    Apellido=["Perez", "Lopez", "Hernandez", "Garcia"]
)
print("\nassign() agrega la columna al final, sin tocar el frame original:")
print(nuevo_frame_assign)

# ---------------------------------------------------------------------------
# 6. Metodo insert(): permite elegir EN QUE POSICION va la nueva columna.
#    OJO: insert() SI modifica el frame que lo llama (no regresa uno nuevo).
# ---------------------------------------------------------------------------
grupoDS_insert = grupoDS_base.copy()
# Posicion 1 = justo despues de 'Nombre' (que esta en la posicion 0)
grupoDS_insert.insert(1, "Apellido", ["Perez", "Lopez", "Hernandez", "Garcia"])
print("\ninsert() coloca 'Apellido' justo despues de 'Nombre':")
print(grupoDS_insert)

# ---------------------------------------------------------------------------
# 7. Concatenar RENGLONES de un frame a otro: pd.concat([...]) (axis=0 default)
# ---------------------------------------------------------------------------
otroGrupoDS = pd.DataFrame({
    "Nombre": ["Ricardo", "Fernanda"],
    "Examen": [88, 84],
    "Proyecto": [93, 98],
})

# Sin ignore_index, los indices del segundo frame se repiten (0, 1 de nuevo)
concat_sin_reindex = pd.concat([grupoDS_base, otroGrupoDS])
print("\nConcat por renglones SIN ignore_index (los indices 0 y 1 se repiten):")
print(concat_sin_reindex)

# Con ignore_index=True, Pandas genera indices nuevos y consecutivos
concat_con_reindex = pd.concat([grupoDS_base, otroGrupoDS], ignore_index=True)
print("\nConcat por renglones CON ignore_index=True (indices 0..5 limpios):")
print(concat_con_reindex)

# Si las columnas de los dos frames no coinciden del todo, concat rellena
# con NaN ("Not a Number") donde no hay dato.
otroGrupoDSOtrosDatos = pd.DataFrame({
    "Nombre": ["Victoria", "Manuel"],
    "Edad": [23, 24],
    "Examen": [78, 72],
    # Nota: este frame NO tiene 'Proyecto', por eso saldra NaN ahi
})
concat_con_faltantes = pd.concat(
    [grupoDS_base, otroGrupoDSOtrosDatos], ignore_index=True
)
print("\nConcat con columnas distintas: faltantes se llenan con NaN:")
print(concat_con_faltantes)

# ---------------------------------------------------------------------------
# 8. Concatenar COLUMNAS de un frame a otro ("joining"): pd.concat(axis=1)
# ---------------------------------------------------------------------------
grupoDSMasDatos = pd.DataFrame({
    "Apellido": ["Perez", "Lopez", "Hernandez", "Garcia"],
    "Edad": [23, 26, 25, 24],
})
union_columnas = pd.concat([grupoDS_base, grupoDSMasDatos], axis=1)
print("\nConcat por columnas (axis=1), mismos indices en ambos frames:")
print(union_columnas)

# Se puede seleccionar solo una columna del segundo frame antes de concatenar
solo_apellido = pd.concat([grupoDS_base, grupoDSMasDatos[["Apellido"]]], axis=1)
print("\nConcat por columnas seleccionando solo 'Apellido':")
print(solo_apellido)

# ---------------------------------------------------------------------------
# 9. Cuando el numero de renglones NO coincide: hay que alinear los indices
#    con set_index() antes de concatenar por columnas, si no, salen NaN.
# ---------------------------------------------------------------------------
grupoDSParcial = pd.DataFrame({
    "Apellido": ["Perez", "Lopez"],
    "Edad": [23, 26],
})  # Solo trae datos para los renglones 0 y 1 (Paulina y Norberto)

# Sin realinear, solo coincide donde el indice es igual (0 y 1); 2 y 3 -> NaN
concat_parcial_sin_set_index = pd.concat([grupoDS_base, grupoDSParcial], axis=1)
print("\nConcat con menos renglones, sin reindexar (coincide solo indices 0 y 1):")
print(concat_parcial_sin_set_index)

# Si en cambio esos datos correspondieran a Julia (indice 2) y a un renglon
# nuevo (indice 4), hay que decirselo con set_index():
grupoDSParcial_reindexado = grupoDSParcial.set_index(pd.Index([2, 4]))
concat_con_set_index = pd.concat([grupoDS_base, grupoDSParcial_reindexado], axis=1)
print("\nConcat tras re-indexar el segundo frame a [2, 4] (coincide con Julia):")
print(concat_con_set_index)

# ---------------------------------------------------------------------------
# 10. Los dos tipos de join en concat(axis=1): 'outer' (union, default) e
#     'inner' (interseccion: solo los indices que estan en ambos frames)
# ---------------------------------------------------------------------------
join_outer = pd.concat(
    [grupoDS_base, grupoDSParcial_reindexado], axis=1, join="outer"
)
join_inner = pd.concat(
    [grupoDS_base, grupoDSParcial_reindexado], axis=1, join="inner"
)
print("\njoin='outer' (todos los indices, con NaN donde falte):")
print(join_outer)
print("\njoin='inner' (solo los indices que coinciden en ambos frames):")
print(join_inner)

print("\nListo: distintas formas de agregar columnas y concatenar frames probadas.")
