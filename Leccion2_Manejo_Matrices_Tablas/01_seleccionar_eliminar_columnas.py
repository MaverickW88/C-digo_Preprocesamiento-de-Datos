"""
Leccion 2 - Manejo de matrices y tablas
Guia: "Seleccionar / eliminar columnas de una tabla"

Que hace este script:
Reproduce, paso a paso y con el mismo frame de ejemplo que usa el PDF (un
frame llamado `hoteles` con 3 hoteles ficticios), todas las formas de:
  1. Seleccionar una columna (por nombre, por punto, por numero con iloc)
  2. Seleccionar varias columnas (en orden libre, o consecutivas con slicing)
  3. Eliminar columnas (drop, con lista, con el parametro columns=)
  4. Eliminar renglones (drop con axis=0)

No usa ningun CSV del curso porque el PDF construye el ejemplo a mano; aqui
se recrea esa misma tabla para que puedas correr el archivo de forma
independiente y comparar tu salida contra la del PDF.
"""

import pandas as pd

# ---------------------------------------------------------------------------
# 1. Recrear el frame "hoteles" exactamente como aparece en el PDF
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
# 2. Seleccionar UNA columna
# ---------------------------------------------------------------------------
# a) Por nombre, como string entre corchetes
col_pais = hoteles["pais"]
print("\nColumna 'pais' (por nombre):")
print(col_pais)

# b) Por nombre, usando el operador punto (solo funciona si el nombre de la
#    columna no tiene espacios ni caracteres especiales)
col_pais_punto = hoteles.pais
print("\nColumna 'pais' (con punto):", list(col_pais_punto))

# c) Por numero de columna (indexing), con iloc[renglones, columnas].
#    'pais' es la columna numero 3 (la numeracion empieza en 0).
valor_0_3 = hoteles.iloc[0, 3]             # renglon 0, columna 3 -> un solo valor
columna_3_completa = hoteles.iloc[:, 3]     # ':' en renglones = todos los renglones
print("\nhoteles.iloc[0, 3] ->", valor_0_3)
print("hoteles.iloc[:, 3] (columna completa):")
print(columna_3_completa)

# d) Alternativa: usar hoteles.columns[3] para obtener el nombre y luego
#    indexar con ese nombre.
col_por_nombre_dinamico = hoteles[hoteles.columns[3]]
print("\nhoteles[hoteles.columns[3]] (mismo resultado que arriba):")
print(col_por_nombre_dinamico)

# ---------------------------------------------------------------------------
# 3. Seleccionar VARIAS columnas en cualquier orden
# ---------------------------------------------------------------------------
# Con una lista de nombres entre corchetes dobles. El orden de la lista es
# el orden en el que aparecen en el resultado.
seleccion_1 = hoteles[["nombre", "precio", "playa"]]
seleccion_2 = hoteles[["playa", "precio", "nombre"]]  # mismo contenido, distinto orden
print("\nSeleccion ['nombre', 'precio', 'playa']:")
print(seleccion_1)
print("\nSeleccion ['playa', 'precio', 'nombre'] (orden distinto):")
print(seleccion_2)

# Para dejar la seleccion como un nuevo frame independiente, basta con
# asignarla a una variable (ya quedo arriba en seleccion_1/seleccion_2).
hotelPlaya = hoteles[["playa", "precio", "nombre"]]

# La misma seleccion, pero con iloc (por numero de columna) y con loc (por
# nombre). Las tres formas dan el mismo resultado:
hotelPlaya_iloc = hoteles.iloc[:, [7, 5, 0]]              # columnas playa(7), precio(5), nombre(0)
hotelPlaya_loc = hoteles.loc[:, ["playa", "precio", "nombre"]]
print("\nMismo resultado via iloc:")
print(hotelPlaya_iloc)
print("\nMismo resultado via loc:")
print(hotelPlaya_loc)

# ---------------------------------------------------------------------------
# 4. Seleccionar columnas CONSECUTIVAS (slicing)
# ---------------------------------------------------------------------------
# Con iloc, por numero: de la columna 1 ('ciudad') a la 5 ('precio').
# OJO: en slicing con numeros, el ultimo indice NO se incluye, por eso
# hay que llegar hasta 6 para que la ultima columna incluida sea la 5.
consecutivas_iloc = hoteles.iloc[:, 1:6]
print("\nColumnas consecutivas con iloc[:, 1:6] (ciudad...precio):")
print(consecutivas_iloc)

# Con loc, por nombre: aqui el slicing SI incluye el ultimo nombre.
consecutivas_loc = hoteles.loc[:, "ciudad":"precio"]
print("\nMismo resultado con loc[:, 'ciudad':'precio']:")
print(consecutivas_loc)

# ---------------------------------------------------------------------------
# 5. Eliminar columnas con drop()
# ---------------------------------------------------------------------------
# a) Una sola columna por nombre. axis=1 indica "es una columna" (axis=0
#    seria un renglon). drop() NO modifica el frame original, regresa uno
#    nuevo (por eso se asigna a nuevo_frame).
nuevo_frame = hoteles.drop("estrellas", axis=1)
print("\nFrame sin la columna 'estrellas':")
print(nuevo_frame)
print("El frame original 'hoteles' sigue intacto:")
print(hoteles.columns.tolist())

# Dos formas de que el cambio se quede en el propio frame:
#   1) Reasignando:       hoteles = hoteles.drop("estrellas", axis=1)
#   2) Con inplace=True:  hoteles.drop("estrellas", axis=1, inplace=True)
# (No se ejecutan aqui para conservar 'hoteles' completo para los ejemplos
# siguientes; se dejan solo como referencia en el comentario.)

# b) Varias columnas a la vez, pasando una lista de nombres.
sin_precio_playa = hoteles.drop(["playa", "precio"], axis=1)
print("\nFrame sin 'playa' y 'precio' (lista de nombres):")
print(sin_precio_playa)

# c) Usando el parametro columns= en vez de axis=1 (ya no hace falta axis).
sin_precio = hoteles.drop(columns="precio")
print("\nFrame sin 'precio' (parametro columns=):")
print(sin_precio)

# d) Varias columnas con columns= y una lista.
sin_pais_estado = hoteles.drop(columns=["pais", "estado"])
print("\nFrame sin 'pais' y 'estado' (columns= con lista):")
print(sin_pais_estado)

# ---------------------------------------------------------------------------
# 6. Eliminar RENGLONES con la misma funcion drop (axis=0)
# ---------------------------------------------------------------------------
# Un renglon se identifica por su indice. axis=0 indica "es un renglon".
sin_renglon_1 = hoteles.drop(1, axis=0)
print("\nFrame sin el renglon de indice 1 (Colonial):")
print(sin_renglon_1)

# Para borrar varios renglones, se usa una lista de indices.
sin_renglones_0_2 = hoteles.drop([0, 2], axis=0)
print("\nFrame sin los renglones 0 y 2 (solo queda Colonial):")
print(sin_renglones_0_2)

print("\nListo: selección, eliminación de columnas y eliminación de renglones probadas.")
