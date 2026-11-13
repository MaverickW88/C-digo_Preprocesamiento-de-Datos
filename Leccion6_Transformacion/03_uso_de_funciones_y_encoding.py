"""
Leccion 6 - Creacion de caracteristicas por transformacion
Guia: "Uso de funciones y reduccion de dimensiones"

Que hace este script:
Reproduce las transformaciones por FUNCION que describe el PDF (todas menos
PCA, que ya se cubrio a fondo en 02_pca_reduccion_dimensiones.py):

  1. Potencias (caracteristicas polinomiales): crear x^2, x^3, x1*x2, etc.
     a mano y con PolynomialFeatures de scikit-learn.
  2. Logaritmos: transformar una columna con np.log, np.log10, np.log2,
     y el cuidado que hay que tener con valores 0 o negativos.
  3. Codificacion One-Hot: convertir una columna categorica en varias
     columnas binarias, con pandas.get_dummies, LabelBinarizer y
     OneHotEncoder (las 3 formas que menciona el PDF).
  4. Codificacion categorica simple (Categorical Encoding): convertir cada
     categoria en un numero entero con .astype('category').cat.codes.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelBinarizer, OneHotEncoder, PolynomialFeatures

# ===========================================================================
# 1. POTENCIAS / CARACTERISTICAS POLINOMIALES
# ===========================================================================
puntos = pd.DataFrame({
    "x1": [1, 2, 3, 4, 5],
    "x2": [2, 3, 5, 7, 11],
})
print("Frame original 'puntos':")
print(puntos)

# a) A mano: elevar al cuadrado y al cubo, y crear el producto cruzado x1*x2
puntos_a = puntos.copy()
puntos_a["x1_2"] = puntos_a["x1"] ** 2
puntos_a["x1_3"] = puntos_a["x1"] ** 3
puntos_a["x1_x2"] = puntos_a["x1"] * puntos_a["x2"]
print("\n[Potencias, a mano] x1^2, x1^3 y producto cruzado x1*x2:")
print(puntos_a)

# b) Con scikit-learn: PolynomialFeatures genera TODAS las combinaciones
#    polinomiales hasta el grado indicado (incluye 1, x1, x2, x1^2, x1*x2,
#    x2^2 para degree=2).
generador_poly = PolynomialFeatures(degree=2, include_bias=False)
caracteristicas_poly = generador_poly.fit_transform(puntos[["x1", "x2"]])
nombres_poly = generador_poly.get_feature_names_out(["x1", "x2"])
puntos_poly = pd.DataFrame(caracteristicas_poly, columns=nombres_poly)
print("\n[Potencias, scikit-learn] PolynomialFeatures(degree=2):")
print(puntos_poly)

# ===========================================================================
# 2. LOGARITMOS
# ===========================================================================
# Se agrega una columna con un 0 a proposito, para mostrar el problema de
# tomar log(0) (indefinido / -infinito) y como se resuelve sumando 1 antes.
datos_log = pd.DataFrame({"valor": [1, 10, 0, 100, 1000]})
print("\nFrame 'datos_log' (incluye un 0 a proposito):")
print(datos_log)

datos_log["log_natural"] = np.log(datos_log["valor"] + 1)   # +1 evita log(0)
datos_log["log_base10"] = np.log10(datos_log["valor"] + 1)
datos_log["log_base2"] = np.log2(datos_log["valor"] + 1)
print("\nLogaritmos (natural, base 10, base 2), todos con +1 para evitar log(0):")
print(datos_log)
print("\nNota: np.log(0) da -inf (o error/advertencia segun el caso), por eso")
print("el PDF recomienda sumar 1 a la columna antes de transformarla cuando")
print("puede haber ceros (log(x+1) en vez de log(x)).")

# ===========================================================================
# 3. CODIFICACION ONE-HOT
# ===========================================================================
fruta = pd.DataFrame({
    "nombre": ["manzana", "platano", "naranja", "manzana", "naranja"],
    "precio": [12, 8, 10, 13, 9],
})
print("\nFrame original 'fruta':")
print(fruta)

# a) pandas.get_dummies: crea una columna binaria por cada categoria
one_hot_pandas = pd.get_dummies(fruta["nombre"])
print("\n[One-Hot, pandas.get_dummies] una columna por categoria:")
print(one_hot_pandas)

fruta_con_dummies = pd.concat([fruta, one_hot_pandas], axis=1)
print("\nUnido de vuelta al frame original (fruta + columnas one-hot):")
print(fruta_con_dummies)

# b) LabelBinarizer de scikit-learn: hace lo mismo, pero regresa un arreglo
#    de numpy en vez de columnas con nombre.
binarizador = LabelBinarizer()
one_hot_lb = binarizador.fit_transform(fruta["nombre"])
print("\n[One-Hot, LabelBinarizer] arreglo de numpy (columnas en el orden de "
      f"binarizador.classes_ = {list(binarizador.classes_)}):")
print(one_hot_lb)

# c) OneHotEncoder de scikit-learn: version mas completa/configurable,
#    pensada para usarse dentro de un pipeline de scikit-learn.
codificador = OneHotEncoder(sparse_output=False)
one_hot_ohe = codificador.fit_transform(fruta[["nombre"]])
print(f"\n[One-Hot, OneHotEncoder] columnas = {list(codificador.categories_[0])}:")
print(one_hot_ohe)

# ===========================================================================
# 4. CODIFICACION CATEGORICA SIMPLE (Categorical Encoding)
# ===========================================================================
# En vez de una columna binaria por categoria, se le asigna un solo numero
# entero a cada categoria distinta. Es mas compacto que one-hot, pero el
# PDF advierte: implica un ORDEN entre categorias (0 < 1 < 2...) que puede
# no existir realmente entre ellas (por eso one-hot suele preferirse para
# variables categoricas SIN orden natural).
fruta_cat = fruta.copy()
fruta_cat["nombre"] = fruta_cat["nombre"].astype("category")
fruta_cat["nombre_codigo"] = fruta_cat["nombre"].cat.codes
print("\n[Categorical Encoding] cada categoria se vuelve un entero:")
print(fruta_cat)
print("\nCategorias y su codigo asignado:")
print(dict(enumerate(fruta_cat["nombre"].cat.categories)))

print("\nListo: potencias, logaritmos, one-hot (3 formas) y codificacion "
      "categorica simple, todos probados.")
