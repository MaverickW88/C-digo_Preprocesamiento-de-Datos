"""
Leccion 5 - Creacion de caracteristicas por agrupamiento y separacion
Guia: "Agrupamiento de datos"

Que hace este script:
Recrea las tablas de ejemplo del PDF (ventas de 3 meses, luego 2 anios) y
muestra todas las variantes del metodo groupby() de Pandas:
  1. Agrupar por una columna y sumar todo (groupby().sum())
  2. reset_index() para que la columna de agrupamiento vuelva a ser una
     columna normal (no un indice)
  3. Quedarse solo con una columna agregada, como serie o como frame
  4. Agrupar por varias columnas a la vez (ej. anio y mes)
  5. as_index=False, para ahorrarse el reset_index()
  6. Otras funciones de agregacion ademas de sum(): mean, std, count, max, min
  7. get_group(): recuperar un grupo especifico ya formado
"""

import pandas as pd

# ---------------------------------------------------------------------------
# 1. Recrear la tabla 'ventas' (3 meses) del PDF
# ---------------------------------------------------------------------------
ventas = pd.DataFrame({
    "unidades": [7, 13, 5, 21, 11, 7, 16, 15, 11],
    "importe": [2268, 4212, 1620, 6804, 3564, 2268, 5184, 4860, 3564],
    "anio": [2021] * 9,
    "mes": ["sept", "sept", "sept", "oct", "oct", "oct", "oct", "nov", "nov"],
    "dia": [5, 17, 28, 7, 12, 13, 30, 3, 26],
    "diaSemana": ["sabado", "jueves", "lunes", "miercoles", "lunes",
                  "martes", "viernes", "martes", "jueves"],
})
print("Frame original 'ventas':")
print(ventas)

# ---------------------------------------------------------------------------
# 2. Agrupar por 'mes' y sumar todas las columnas numericas (sum())
# ---------------------------------------------------------------------------
ventasMes = ventas.groupby(["mes"]).sum(numeric_only=True)
print("\nventas.groupby(['mes']).sum(): el mes queda como INDICE del nuevo frame:")
print(ventasMes)
# Nota: columnas de texto (dia, diaSemana) se excluyen automaticamente con
# numeric_only=True; sumar 'anio' da un numero sin sentido real (solo es
# ilustrativo, igual que en el PDF).

# ---------------------------------------------------------------------------
# 3. reset_index(): convierte el indice 'mes' de vuelta en una columna normal
# ---------------------------------------------------------------------------
ventasMes = ventasMes.reset_index()
print("\nDespues de reset_index(), 'mes' vuelve a ser una columna:")
print(ventasMes)

# ---------------------------------------------------------------------------
# 4. Quedarse solo con una columna: como SERIE (corchetes simples) o como
#    FRAME (corchetes dobles, con una lista de un solo nombre)
# ---------------------------------------------------------------------------
unidades_por_mes_serie = ventas.groupby(["mes"])["unidades"].sum()
unidades_por_mes_frame = ventas.groupby(["mes"])[["unidades"]].sum()
print("\nSolo 'unidades', como SERIE (corchetes simples):")
print(unidades_por_mes_serie)
print("\nSolo 'unidades', como FRAME (corchetes dobles):")
print(unidades_por_mes_frame)

# ---------------------------------------------------------------------------
# 5. Agregar solo las columnas que tienen sentido sumar: unidades e importe
# ---------------------------------------------------------------------------
ventasMes_limpio = ventas.groupby(["mes"])[["unidades", "importe"]].sum().reset_index()
print("\nSolo sumando 'unidades' e 'importe' (ignorando anio y dia):")
print(ventasMes_limpio)

# ---------------------------------------------------------------------------
# 6. Recrear la segunda tabla del PDF: ventas de DOS anios (2020 y 2021)
# ---------------------------------------------------------------------------
ventasDos = pd.DataFrame({
    "unidades": [7, 13, 21, 11, 15, 11, 5, 8, 7, 16, 5, 10],
    "importe": [2268, 4212, 6804, 3564, 4860, 3564, 1620, 2592, 2268, 5184, 1620, 3240],
    "anio": [2020, 2020, 2020, 2020, 2020, 2020, 2021, 2021, 2021, 2021, 2021, 2021],
    "mes": ["sept", "sept", "oct", "oct", "nov", "nov",
            "sept", "sept", "oct", "oct", "oct", "nov"],
    "dia": [5, 17, 7, 12, 3, 26, 28, 30, 13, 18, 30, 27],
    "diaSemana": ["sabado", "jueves", "miercoles", "lunes", "martes", "jueves",
                  "martes", "jueves", "miercoles", "lunes", "sabado", "sabado"],
})
print("\nFrame 'ventasDos' (dos anios):")
print(ventasDos)

# ---------------------------------------------------------------------------
# 7. Agrupar por DOS columnas (anio, luego mes dentro de cada anio)
# ---------------------------------------------------------------------------
ventasAnioMes = ventasDos.groupby(["anio", "mes"])[["unidades", "importe"]].sum()
print("\nAgrupado por ['anio', 'mes'] (indice de 2 niveles):")
print(ventasAnioMes)

ventasAnioMes_reset = ventasAnioMes.reset_index()
print("\nMismo resultado, con reset_index() (anio y mes como columnas):")
print(ventasAnioMes_reset)

# as_index=False hace lo mismo que el reset_index(), en un solo paso
ventasAnioMes_as_index_false = ventasDos.groupby(
    ["anio", "mes"], as_index=False
)[["unidades", "importe"]].sum()
print("\nMismo resultado usando as_index=False (sin necesitar reset_index):")
print(ventasAnioMes_as_index_false)

# ---------------------------------------------------------------------------
# 8. Otras funciones de agregacion ademas de sum(): mean, std, count, max, min
# ---------------------------------------------------------------------------
agrupado_mes = ventasDos.groupby(["mes"])[["unidades", "importe"]]
print("\nOtras funciones de agregacion sobre el agrupamiento por 'mes':")
print("mean():\n", agrupado_mes.mean())
print("\nstd():\n", agrupado_mes.std())
print("\ncount():\n", agrupado_mes.count())
print("\nmax():\n", agrupado_mes.max())
print("\nmin():\n", agrupado_mes.min())

# ---------------------------------------------------------------------------
# 9. get_group(): recuperar un grupo ya formado, sin tener que re-filtrar
#    con condiciones booleanas
# ---------------------------------------------------------------------------
# Nota: en versiones recientes de Pandas, si se agrupa pasando una LISTA de
# columnas (aunque sea una sola), get_group espera una tupla como llave. Por
# eso aqui se agrupa pasando el nombre de la columna como string (no como
# lista de un elemento), que es la forma mas simple cuando solo se agrupa
# por una columna.
ventasAnio = ventasDos.groupby("anio")[["unidades", "importe", "mes"]]
ventas_2020 = ventasAnio.get_group(2020)
print("\nget_group(2020): solo las ventas del anio 2020:")
print(ventas_2020)

print("\nListo: agrupamiento con groupby() probado en todas sus variantes.")
