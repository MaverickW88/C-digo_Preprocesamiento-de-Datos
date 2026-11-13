"""
Leccion 4 - Evaluacion y seleccion de caracteristicas
Guia: "Metodos automaticos de seleccion"

Que hace este script:
Reproduce el ejemplo de seleccion automatica de caracteristicas por
REGULARIZACION (regresion Ridge de scikit-learn), con la misma tabla de
10 renglones y 6 variables de entrada (x1..x6) + salida continua (y) que
usa el PDF.

Idea clave: la regularizacion penaliza pesos grandes en la regresion
lineal. Al correr Ridge con distintos valores de alpha (que es la lambda
del PDF), los pesos de las variables poco importantes se acercan a cero
por si solos, sin que nosotros tengamos que decidir manualmente cuales
quitar. Entre mas grande alpha, mas agresiva la penalizacion (y peor el
ajuste, medido con R2).

Nota: los valores de la tabla se transcribieron del PDF (la columna x3 en
los ultimos 5 renglones del documento se ve identica a x2, posiblemente
por un detalle de como se genero el PDF). Por eso los resultados de este
script son muy parecidos a los del tutorial (mismo orden de magnitud e
igual conclusion: x2/x3 se apagan primero, luego todas), pero no coinciden
a la cifra exacta. El comportamiento y la conclusion son los importantes,
no el ultimo decimal.
"""

import numpy as np
import pandas as pd
from sklearn import linear_model

# ---------------------------------------------------------------------------
# 1. Recrear el frame 'datosRegulariza' del PDF
# ---------------------------------------------------------------------------
datosRegulariza = pd.DataFrame({
    "x1": [0.8502, 0.1671, 0.4554, 0.4425, 0.7519, 0.0462, 0.3888, 0.2380, 0.8747, 0.2031],
    "x2": [0.0565, 0.8778, 0.1847, 0.7466, 0.4453, 1.0567, 0.8392, 0.4098, 0.8741, 1.0619],
    "x3": [0.4520, 1.2652, 0.5236, 1.1417, 0.8372, 1.0567, 0.8392, 0.4098, 0.8741, 1.0619],
    "x4": [1.1858, 0.5309, 0.7904, 0.7207, 1.0813, 0.3261, 0.7679, 0.5641, 1.2283, 0.6004],
    "x5": [0.9457, 0.0283, 0.0421, 0.4572, 0.0983, 0.1978, 0.8204, 0.0193, 0.6466, 0.1009],
    "x6": [0.5869, 0.4954, 0.9099, 0.7557, 0.2540, 0.1550, 0.4904, 0.7776, 0.3221, 0.1927],
    "y": [6.1105, 2.5446, 3.3846, 4.7790, 3.1322, 2.3630, 5.1113, 2.3292, 5.5384, 2.2473],
})
print("Frame 'datosRegulariza':")
print(datosRegulariza)

# ---------------------------------------------------------------------------
# 2. Separar variables de entrada (X) y variable de salida (y)
# ---------------------------------------------------------------------------
y = datosRegulariza["y"]
X = datosRegulariza[datosRegulariza.columns[0:6]]  # las primeras 6 columnas

# ---------------------------------------------------------------------------
# 3. Funcion auxiliar: correr Ridge con un alpha (lambda) dado y reportar
#    el peso de cada variable (coef_), el intercepto (intercept_, w0) y el
#    coeficiente de determinacion R2 (score), que mide que tan bueno es el
#    ajuste (cerca de 1 = muy bueno, cerca de 0 = muy malo).
# ---------------------------------------------------------------------------
def correr_ridge(alpha):
    reg = linear_model.Ridge(alpha=alpha)
    reg.fit(X, y)
    r2 = reg.score(X, y)
    pesos = dict(zip(X.columns, reg.coef_))
    print(f"\n--- Ridge con alpha (lambda) = {alpha} ---")
    print(f"Intercepto (w0): {reg.intercept_:.4f}")
    print("Pesos por variable:")
    for nombre, peso in pesos.items():
        print(f"  {nombre}: {peso:.4f}")
    print(f"R2 (coeficiente de determinacion): {r2:.4f}")
    return reg, pesos, r2


# ---------------------------------------------------------------------------
# 4. Probar 3 valores de alpha, igual que el PDF: 0.5, 3 y 100
# ---------------------------------------------------------------------------
reg_05, pesos_05, r2_05 = correr_ridge(0.5)
reg_3, pesos_3, r2_3 = correr_ridge(3)
reg_100, pesos_100, r2_100 = correr_ridge(100)

# ---------------------------------------------------------------------------
# 5. Interpretacion: con alpha=0.5, 'x2' ya tiene un peso casi 0 (poco
#    importante). Con alpha=3, 'x2' y 'x3' se acercan a 0 (se "eliminan").
#    Con alpha=100, la regularizacion es tan fuerte que practicamente
#    elimina TODAS las variables (y el R2 se vuelve muy malo).
# ---------------------------------------------------------------------------
UMBRAL_PESO_IRRELEVANTE = 0.1

print("\nResumen: variables que la regularizacion considera poco importantes")
print("(|peso| < %.2f) en cada corrida:" % UMBRAL_PESO_IRRELEVANTE)
for alpha, pesos, r2 in [(0.5, pesos_05, r2_05), (3, pesos_3, r2_3), (100, pesos_100, r2_100)]:
    poco_importantes = [v for v, w in pesos.items() if abs(w) < UMBRAL_PESO_IRRELEVANTE]
    print(f"  alpha={alpha:>5}: poco importantes = {poco_importantes} | R2 = {r2:.3f}")

print("\nConclusion: a mayor alpha (mas regularizacion), mas variables se "
      "'apagan' solas, pero el ajuste (R2) empeora. El valor de alpha se "
      "elige probando varios y quedandose con el que de mejor balance.")
