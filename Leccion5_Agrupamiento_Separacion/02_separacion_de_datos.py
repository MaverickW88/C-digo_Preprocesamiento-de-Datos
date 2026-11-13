"""
Leccion 5 - Creacion de caracteristicas por agrupamiento y separacion
Guia: "Separacion de datos"

Que hace este script:
Recrea la tabla de ventas con fechas en un solo string (formato dd/mm/aaaa)
y muestra las 3 formas que da el PDF para separar/extraer informacion de
una fecha:
  1. Manipulando la fecha como STRING (slicing de caracteres, o split)
  2. Usando el constructor pd.DatetimeIndex
  3. Usando la funcion pd.to_datetime

Tambien muestra, al final, un ejemplo de otra tecnica de separacion que el
PDF menciona en texto pero no en codigo: separar un nombre completo en
nombre y apellido.
"""

import pandas as pd

# ---------------------------------------------------------------------------
# 1. Recrear la tabla 'ventas' con la fecha en un solo string dd/mm/aaaa
# ---------------------------------------------------------------------------
ventas = pd.DataFrame({
    "unidades": [7, 13, 21, 11, 15, 11, 5, 8, 7, 16, 5, 10],
    "importe": [2268, 4212, 6804, 3564, 4860, 3564, 1620, 2592, 2268, 5184, 1620, 3240],
    "fecha": ["05/09/2020", "17/09/2020", "07/10/2020", "12/10/2020",
              "03/11/2020", "26/11/2020", "28/09/2021", "30/09/2021",
              "13/10/2021", "18/10/2021", "30/10/2021", "27/11/2021"],
})
print("Frame original 'ventas' (fecha como un solo string):")
print(ventas)

print(f"\nTipo del primer valor de 'fecha': {type(ventas['fecha'][0])}")

# ---------------------------------------------------------------------------
# 2. Metodo 1: manipular la fecha como STRING
# ---------------------------------------------------------------------------
# a) Tomando los ultimos 4 caracteres (los dos digitos de dia y mes, mas
#    los 2 separadores, dejan el anio siempre al final en dd/mm/aaaa)
ventas_a = ventas.copy()
ventas_a["anio"] = ventas_a["fecha"].str[-4:].astype(int)
print("\n(a) Anio extraido con slicing de string (ultimos 4 caracteres):")
print(ventas_a[["fecha", "anio"]])

# b) Partiendo el string por "/" y tomando el tercer elemento (indice 2)
ventas_b = ventas.copy()
ventas_b["anio"] = ventas_b["fecha"].str.split(pat="/").str[2].astype(int)
print("\n(b) Anio extraido con split('/') y tomando el elemento de indice 2:")
print(ventas_b[["fecha", "anio"]])

assert ventas_a["anio"].equals(ventas_b["anio"]), "Ambas formas deberian dar el mismo resultado"

# ---------------------------------------------------------------------------
# 3. Metodo 2: constructor pd.DatetimeIndex
#    dayfirst=True le dice que en el string el DIA viene antes que el mes
#    (necesario aqui porque el formato es dd/mm/aaaa, no mm/dd/aaaa).
# ---------------------------------------------------------------------------
ventas_dt = ventas.copy()
ventas_dt["anio"] = pd.DatetimeIndex(ventas_dt["fecha"]).year
ventas_dt["mes"] = pd.DatetimeIndex(ventas_dt["fecha"], dayfirst=True).month
ventas_dt["dia"] = pd.DatetimeIndex(ventas_dt["fecha"], dayfirst=True).day
print("\nMetodo 2 (DatetimeIndex): anio, mes y dia extraidos como enteros:")
print(ventas_dt[["fecha", "anio", "mes", "dia"]])

# Ejemplo adicional del PDF: DatetimeIndex tambien acepta fechas en varios
# formatos distintos dentro de la misma serie.
fechas_mixtas = pd.Series(["01/02/2021", "08-05-2017", "28 April 2020", "12-16-2019"])
anios_mixtos = pd.DatetimeIndex(fechas_mixtas).year
print("\nDatetimeIndex tambien funciona con formatos de fecha mezclados:")
print(f"  {list(fechas_mixtas)} -> anios: {list(anios_mixtos)}")

# ---------------------------------------------------------------------------
# 4. Metodo 3: pd.to_datetime + el accessor .dt
# ---------------------------------------------------------------------------
ventas_to_datetime = ventas.copy()
ventas_to_datetime["anio"] = pd.to_datetime(
    ventas_to_datetime["fecha"], dayfirst=True
).dt.year
print("\nMetodo 3 (to_datetime + .dt.year):")
print(ventas_to_datetime[["fecha", "anio"]])

# format="mixed" le dice a Pandas que cada elemento puede traer un formato
# de fecha distinto (necesario aqui porque mezclamos dd/mm/aaaa, dd-mm-aaaa
# y "28 April 2020" en la misma serie); sin esto, Pandas intenta usar un
# solo formato para toda la serie y falla en el segundo valor.
anios_mixtos_to_datetime = pd.to_datetime(fechas_mixtas, format="mixed").dt.year
print("\nto_datetime tambien acepta formatos mezclados:")
print(list(anios_mixtos_to_datetime))

# ---------------------------------------------------------------------------
# 5. Otro ejemplo de separacion que el PDF menciona (sin codigo): separar un
#    nombre completo en nombre y apellido usando split() sobre espacios.
# ---------------------------------------------------------------------------
personas = pd.DataFrame({"nombre_completo": ["Paulina Perez", "Norberto Lopez", "Julia Hernandez"]})
personas[["nombre", "apellido"]] = personas["nombre_completo"].str.split(" ", n=1, expand=True)
print("\nEjemplo extra: separar 'nombre_completo' en 'nombre' y 'apellido':")
print(personas)

print("\nListo: las 3 formas de separar/extraer el anio de una fecha fueron probadas.")
