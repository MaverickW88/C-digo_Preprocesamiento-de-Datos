"""
Leccion 6 - Creacion de caracteristicas por transformacion
Guia: "Escalamiento de caracteristicas"

Que hace este script:
Recrea el frame 'casas' del PDF (3 casas, con columnas en escalas MUY
distintas: metros en cientos, cuartos en unidades, precio en millones) y
aplica los 3 metodos de escalamiento, cada uno de 2 formas:
  a) "a mano", con la formula directa
  b) con scikit-learn (preprocessing.MaxAbsScaler / MinMaxScaler / StandardScaler)

Los 3 metodos:
  1. Escalamiento de maximo absoluto: xi / max(|x|)              -> rango [-1, 1]
  2. Escalamiento min-max (normalizacion): (xi - min) / (max-min) -> rango [0, 1]
  3. Estandarizacion: (xi - media) / desviacion_estandar          -> media 0, std 1
"""

import pandas as pd
from sklearn import preprocessing

# ---------------------------------------------------------------------------
# 1. Recrear el frame 'casas' del PDF
# ---------------------------------------------------------------------------
casas = pd.DataFrame({
    "metros_terreno": [200, 400, 120],
    "metros_construccion": [130, 312, 120],
    "cuartos": [3, 6, 3],
    "estacionamientos": [2, 3, 1],
    "precio": [1825000, 2850000, 1375000],
})
print("Frame original 'casas' (escalas muy distintas: cientos, unidades, millones):")
print(casas)

# ===========================================================================
# 1. ESCALAMIENTO DE MAXIMO ABSOLUTO sobre 'metros_terreno'
# ===========================================================================
# a) A mano, con max() y abs() de Python/Pandas
casas_a = casas.copy()
maximo = max(abs(casas_a["metros_terreno"]))
casas_a["metros_terreno_norm"] = casas_a["metros_terreno"] / maximo
print(f"\n[Max absoluto, a mano] maximo encontrado = {maximo}")
print(casas_a[["metros_terreno", "metros_terreno_norm"]])

# Version en una sola linea, equivalente:
casas_a2 = casas.copy()
casas_a2["metros_terreno_norm"] = (
    casas_a2["metros_terreno"] / casas_a2["metros_terreno"].abs().max()
)
assert casas_a["metros_terreno_norm"].equals(casas_a2["metros_terreno_norm"])

# b) Con scikit-learn: preprocessing.MaxAbsScaler()
escalador = preprocessing.MaxAbsScaler()
frame_escalado = escalador.fit_transform(casas)  # regresa una matriz de numpy
casas_b = casas.copy()
casas_b["metros_terreno_norm"] = pd.Series(frame_escalado[:, 0])
print("\n[Max absoluto, scikit-learn] columna 0 de la matriz escalada:")
print(casas_b[["metros_terreno", "metros_terreno_norm"]])

# ===========================================================================
# 2. ESCALAMIENTO MIN-MAX sobre 'metros_terreno' (a mano) y 'cuartos' (sklearn)
# ===========================================================================
# a) A mano
casas_c = casas.copy()
casas_c["metros_terreno_norm"] = (
    casas_c["metros_terreno"] - casas_c["metros_terreno"].min()
) / (casas_c["metros_terreno"].max() - casas_c["metros_terreno"].min())
print("\n[Min-max, a mano] sobre 'metros_terreno':")
print(casas_c[["metros_terreno", "metros_terreno_norm"]])

# b) Con scikit-learn, aplicado a 'cuartos' (columna 2 del frame)
escalador = preprocessing.MinMaxScaler()
frame_escalado = escalador.fit_transform(casas)
casas_d = casas.copy()
casas_d["cuartos_norm"] = pd.Series(frame_escalado[:, 2])
print("\n[Min-max, scikit-learn] sobre 'cuartos' (columna 2):")
print(casas_d[["cuartos", "cuartos_norm"]])

# ===========================================================================
# 3. ESTANDARIZACION sobre 'metros_terreno' (a mano) y 'estacionamientos' (sklearn)
# ===========================================================================
# a) A mano
casas_e = casas.copy()
casas_e["metros_terreno_norm"] = (
    casas_e["metros_terreno"] - casas_e["metros_terreno"].mean()
) / casas_e["metros_terreno"].std()
print("\n[Estandarizacion, a mano] sobre 'metros_terreno':")
print(casas_e[["metros_terreno", "metros_terreno_norm"]])

# b) Con scikit-learn, aplicado a 'estacionamientos' (columna 3 del frame)
# Nota: StandardScaler de sklearn usa la desviacion estandar POBLACIONAL
# (divide entre n), mientras que pandas.std() usa la MUESTRAL (divide entre
# n-1) por default; por eso el resultado "a mano" y el de sklearn pueden
# diferir ligeramente para muestras muy chicas como esta de 3 renglones.
escalador = preprocessing.StandardScaler()
frame_escalado = escalador.fit_transform(casas)
casas_f = casas.copy()
casas_f["estacionamientos_norm"] = pd.Series(frame_escalado[:, 3])
print("\n[Estandarizacion, scikit-learn] sobre 'estacionamientos' (columna 3):")
print(casas_f[["estacionamientos", "estacionamientos_norm"]])

print("\nListo: los 3 metodos de escalamiento (maximo absoluto, min-max, "
      "estandarizacion) probados a mano y con scikit-learn.")
