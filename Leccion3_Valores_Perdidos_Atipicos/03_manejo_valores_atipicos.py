"""
Leccion 3 - Manejo de valores perdidos y atipicos
Guia: "Manejo de valores atipicos"

Que hace este script:
Usa el archivo real valoresAtipicos.csv (carpeta datos/) para mostrar el
flujo completo de deteccion y tratamiento de valores atipicos (outliers)
en la columna 'ingresos':
  1. Detectarlos con describe() y con un boxplot
  2. Aislarlos filtrando por un umbral que se va ajustando
  3. Eliminarlos con el metodo de la media +/- N * desviacion estandar
  4. Eliminarlos (alternativa) con percentiles
  5. Corregir los que SI se pueden explicar como errores (se les fueron
     ceros de mas), usando la formula real de la empresa: ventas*2000*0.80
  6. Transformar con logaritmo el valor atipico que SI es correcto, para
     acercarlo al resto de la distribucion sin tener que borrarlo

Requiere matplotlib (para los boxplots/histograma). Si corres este script
sin entorno grafico, los plt.show() simplemente no mostraran ventana, pero
el resto del analisis se imprime en consola igual.
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # backend sin ventana, para poder correr el script en cualquier entorno
import matplotlib.pyplot as plt

CARPETA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_CSV = os.path.join(CARPETA_ACTUAL, "datos", "valoresAtipicos.csv")
CARPETA_FIGURAS = os.path.join(CARPETA_ACTUAL, "figuras")
os.makedirs(CARPETA_FIGURAS, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Leer el archivo y colocarlo en el frame 'datos2' (igual que el PDF)
# ---------------------------------------------------------------------------
datos2 = pd.read_csv(RUTA_CSV)
print(f"Frame 'datos2' (valoresAtipicos.csv): {datos2.shape[0]} renglones, {datos2.shape[1]} columnas")

# ---------------------------------------------------------------------------
# 2. Revision rapida con describe(): el PDF detecta algo raro en 'ingresos'
#    (minimo negativo, maximo muy por encima de la mediana)
# ---------------------------------------------------------------------------
print("\ndescribe() de las variables numericas:")
print(datos2.describe())

# ---------------------------------------------------------------------------
# 3. Confirmar visualmente con un boxplot (se guarda como PNG en figuras/)
# ---------------------------------------------------------------------------
datos2.boxplot(column=["ingresos"])
plt.title("Boxplot de 'ingresos' (con los 3 valores atipicos)")
plt.savefig(os.path.join(CARPETA_FIGURAS, "boxplot_ingresos_con_atipicos.png"), dpi=150)
plt.close()

# ---------------------------------------------------------------------------
# 4. Aislar los 3 valores atipicos: primero viendo los que estan arriba de
#    200,000 (para apreciar el tercero, que sin esos dos se ve mejor)...
# ---------------------------------------------------------------------------
auxiliar = datos2[datos2["ingresos"] < 200000]
auxiliar.boxplot(column=["ingresos"])
plt.title("Boxplot de 'ingresos' < 200,000 (se aprecia el 3er atipico)")
plt.savefig(os.path.join(CARPETA_FIGURAS, "boxplot_ingresos_menor_200000.png"), dpi=150)
plt.close()

# ...y luego mostrando los renglones con ingresos por encima de 50,000, que
# son justamente los 3 valores atipicos:
atipicos = datos2[datos2["ingresos"] > 50000]
print("\nLos 3 valores atipicos (ingresos > 50,000):")
print(atipicos)

# ---------------------------------------------------------------------------
# 5. Metodo 1 para eliminarlos: media +/- N * desviacion estandar (N=2)
# ---------------------------------------------------------------------------
N = 2
lim_sup = datos2["ingresos"].mean() + N * datos2["ingresos"].std()
lim_inf = datos2["ingresos"].mean() - N * datos2["ingresos"].std()
print(f"\n[Metodo media +/- {N}*std] limite superior = {lim_sup:.2f}, limite inferior = {lim_inf:.2f}")

fuera_de_rango = datos2[(datos2["ingresos"] > lim_sup) | (datos2["ingresos"] < lim_inf)]
print(f"Renglones fuera de ese rango ({len(fuera_de_rango)}):")
print(fuera_de_rango)

# Si este rango convence, se guarda en una variable nueva para seguir trabajando:
datos2_media = datos2[(datos2["ingresos"] < lim_sup) & (datos2["ingresos"] > lim_inf)]
print(f"Frame 'datos2_media' (sin esos 2 atipicos extremos): {datos2_media.shape[0]} renglones")

# ---------------------------------------------------------------------------
# 6. Metodo 2 (alternativa) para eliminarlos: percentiles 5/95.
#    Ventaja: nunca da limites fuera del rango real de los datos.
# ---------------------------------------------------------------------------
lim_sup_pct = datos2["ingresos"].quantile(0.95)
lim_inf_pct = datos2["ingresos"].quantile(0.05)
print(f"\n[Metodo percentiles 5/95] limite superior = {lim_sup_pct}, limite inferior = {lim_inf_pct}")

eliminados_pct = datos2[(datos2["ingresos"] > lim_sup_pct) | (datos2["ingresos"] < lim_inf_pct)]
print(f"Renglones eliminados con este metodo: {eliminados_pct.shape[0]} "
      f"({100 * eliminados_pct.shape[0] / len(datos2):.1f}% del total)")

data2_percentil = datos2[(datos2["ingresos"] < lim_sup_pct) & (datos2["ingresos"] > lim_inf_pct)]
print(f"Frame 'data2_percentil': {data2_percentil.shape[0]} renglones")

# ---------------------------------------------------------------------------
# 7. Cuando SI se conoce la causa: corregir los que son errores de captura.
#    La formula real del pago es ventas*2000*0.80; al aplicarla a los dos
#    primeros valores atipicos (indices 40 y 192) da 9,600 y 14,400, no los
#    960,000 y 1,440,000 capturados -> se les fueron ceros de mas.
# ---------------------------------------------------------------------------
datos2_corregido = datos2.copy()
datos2_corregido.at[40, "ingresos"] = 9600
datos2_corregido.at[192, "ingresos"] = 14400
print("\nDespues de corregir los 2 errores de captura (indices 40 y 192):")
print(datos2_corregido.loc[[40, 192], ["id_personal", "mes", "ventas", "ingresos"]])

# El tercer atipico (indice 240, ingresos=80000) SI es correcto segun la
# formula (50*2000*0.80 = 80000), asi que no se corrige: se trata con el
# metodo del rango (ya visto arriba) o con una transformacion (siguiente paso).

# ---------------------------------------------------------------------------
# 8. Cuando NO se conoce la causa: transformar con logaritmo para acercar el
#    valor atipico "correcto" (80,000) al resto de la distribucion, en vez
#    de borrarlo.
# ---------------------------------------------------------------------------
# Primero nos quedamos solo con ingresos no negativos (ya corregidos los
# errores de captura, para no mezclar ambos tratamientos):
datos2_no_negativos = datos2_corregido[datos2_corregido["ingresos"] >= 0].copy()

sesgo = datos2_no_negativos["ingresos"].skew()
print(f"\nSesgo (skew) de 'ingresos' sin negativos: {sesgo:.4f} "
      "(positivo = cola a la derecha)")

plt.hist(datos2_no_negativos["ingresos"])
plt.title("Histograma de 'ingresos' (antes del logaritmo)")
plt.savefig(os.path.join(CARPETA_FIGURAS, "histograma_ingresos_antes_log.png"), dpi=150)
plt.close()

# Se suma 1 antes del logaritmo para evitar log(0) = -infinito en los
# renglones con ingresos = 0.
datos2_no_negativos["log_ingresos"] = (datos2_no_negativos["ingresos"] + 1).transform(np.log)

plt.hist(datos2_no_negativos["log_ingresos"])
plt.title("Histograma de 'log_ingresos' (despues del logaritmo)")
plt.savefig(os.path.join(CARPETA_FIGURAS, "histograma_log_ingresos_despues_log.png"), dpi=150)
plt.close()

print("\ndescribe() antes y despues de la transformacion logaritmica:")
print(datos2_no_negativos[["ingresos", "log_ingresos"]].describe())

print(f"\nFiguras guardadas en: {CARPETA_FIGURAS}")
print("Listo: valores atipicos detectados, aislados, corregidos (errores) y transformados (log).")
