"""
Leccion 6 - Creacion de caracteristicas por transformacion
Guia: "Como reducir las dimensiones? El metodo PCA"

Que hace este script:
Recrea el ejemplo basico del PDF: una tabla de puntos en 2 dimensiones
(x1, x2) donde x2 depende LINEALMENTE de x1 (x2 = 2*x1 + 1), es decir, la
segunda columna no aporta informacion nueva: toda la variacion de los datos
se explica con una sola dimension. El PDF usa esto para mostrar, de la
forma mas simple posible, como PCA (Principal Component Analysis) encuentra
esa dimension "real" de los datos.

Pasos que se muestran, igual que en el PDF:
  1. Crear los puntos 2D y graficarlos (para ver visualmente que estan
     sobre una linea recta).
  2. Aplicar PCA con 2 componentes y revisar:
       - components_ : los nuevos ejes (vectores) que encontro PCA
       - explained_variance_ : cuanta varianza (informacion) explica cada
         componente
       - explained_variance_ratio_ : lo mismo, pero en proporcion (0 a 1)
  3. Confirmar que el primer componente explica (casi) el 100% de la
     varianza -> con un solo componente ya representamos los datos.
  4. Transformar los datos originales a el nuevo espacio reducido
     (.transform()) y quedarnos solo con la primera columna resultante.
"""

import matplotlib
matplotlib.use("Agg")  # backend sin pantalla (no hay monitor en este entorno)
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

# ---------------------------------------------------------------------------
# 1. Recrear el frame 'puntos2D' del PDF: x2 = 2*x1 + 1 (dependencia lineal)
# ---------------------------------------------------------------------------
x1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
x2 = 2 * x1 + 1

puntos2D = pd.DataFrame({"x1": x1, "x2": x2})
print("Frame 'puntos2D' (x2 = 2*x1 + 1, dependencia lineal perfecta):")
print(puntos2D)

# ---------------------------------------------------------------------------
# 2. Graficar los puntos para ver que caen sobre una linea recta
# ---------------------------------------------------------------------------
import os
carpeta_figuras = os.path.join(os.path.dirname(__file__), "figuras")
os.makedirs(carpeta_figuras, exist_ok=True)

plt.figure()
plt.scatter(puntos2D["x1"], puntos2D["x2"])
plt.xlabel("x1")
plt.ylabel("x2")
plt.title("puntos2D: todos los puntos caen sobre una linea recta")
ruta_grafica = os.path.join(carpeta_figuras, "puntos2D_dispersión.png")
plt.savefig(ruta_grafica)
plt.close()
print(f"\nGrafica de dispersion guardada en: {ruta_grafica}")

# ---------------------------------------------------------------------------
# 3. Aplicar PCA con 2 componentes (el maximo posible, igual al numero de
#    columnas originales) para poder ver cuanta varianza explica cada uno.
# ---------------------------------------------------------------------------
pca = PCA(n_components=2)
pca.fit(puntos2D)

print("\ncomponents_ (los nuevos ejes/vectores que encontro PCA):")
print(pca.components_)

print("\nexplained_variance_ (varianza que explica cada componente):")
print(pca.explained_variance_)

print("\nexplained_variance_ratio_ (proporcion de varianza explicada, suma 1.0):")
print(pca.explained_variance_ratio_)

# ---------------------------------------------------------------------------
# 4. Confirmar que el primer componente explica (casi) toda la varianza
# ---------------------------------------------------------------------------
porcentaje_primer_componente = pca.explained_variance_ratio_[0] * 100
print(f"\nEl primer componente explica {porcentaje_primer_componente:.2f}% de la varianza.")
print("Esto confirma que, aunque los datos tienen 2 columnas, en realidad solo")
print("tienen 1 dimension 'real' de informacion (la linea x2 = 2*x1 + 1).")

# ---------------------------------------------------------------------------
# 5. Transformar los datos originales al nuevo espacio (reducido) de PCA, y
#    quedarnos solo con la primera columna (el componente que importa).
# ---------------------------------------------------------------------------
puntos_transformados = pca.transform(puntos2D)
print("\nDatos transformados al espacio de PCA (2 columnas, una por componente):")
print(puntos_transformados)

puntos_reducidos = puntos_transformados[:, 0]
print("\nDatos reducidos a 1 sola dimension (solo el primer componente):")
print(puntos_reducidos)

print("\nListo: PCA aplicado sobre 'puntos2D', confirmando que una sola")
print("dimension basta para representar toda la informacion de los datos.")
