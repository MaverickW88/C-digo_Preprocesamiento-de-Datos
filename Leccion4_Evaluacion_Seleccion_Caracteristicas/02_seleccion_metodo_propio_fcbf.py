"""
Leccion 4 - Evaluacion y seleccion de caracteristicas
Guia: "Seleccion con metodos propios"

Que hace este script:
Implementa, paso a paso, el algoritmo FCBF (Fast Correlation-Based Filter,
Yu y Liu, 2003) tal como lo describe el PDF, y lo corre sobre la misma
tabla de ejemplo (7 variables de entrada x1..x7 y una salida y) para
reproducir exactamente el resultado del tutorial: al final deben quedar
las variables x6, x3, x5, x7 (y se eliminan x4, x1, x2).

Pasos del algoritmo (parametros lvs y lev tal como en el PDF):
  1. Eliminar las variables de entrada cuya correlacion absoluta con la
     salida sea menor que lvs (limite-variable-salida).
  2. Para las que quedan, ir comparando cada variable contra las demas
     variables de entrada: si dos tienen correlacion absoluta >= lev
     (limite-entre-variables), son redundantes y sólo se queda la que
     tenga mayor correlacion absoluta con la salida.
"""

import pandas as pd

# ---------------------------------------------------------------------------
# 1. Recrear la tabla de ejemplo del PDF (7 variables de entrada + salida y)
# ---------------------------------------------------------------------------
datos = pd.DataFrame({
    "x1": [0.92084194, 0.17955529, 0.55158038, 0.43850599, 0.06904929,
           0.85971092, 0.87546309, 0.78013499, 0.94917318, 0.11831619],
    "x2": [0.90753688, 0.78225311, 0.08563669, 0.871024, 0.93718697,
           0.74783553, 0.47039562, 0.81574963, 0.03290477, 0.10211451],
    "x3": [1.17330136, 1.14666355, 0.37096428, 1.16584447, 1.24641406,
           1.04448428, 0.7860944, 1.19390023, 0.43064494, 0.39895298],
    "x4": [1.30849693, 0.52967872, 0.92092191, 0.80830521, 0.3915693,
           1.13937777, 1.27440124, 1.17907659, 1.3224779, 0.36615762],
    "x5": [0.25477118, 0.43276604, 0.33857751, 0.62365827, 0.56694801,
           0.09662614, 0.71897326, 0.94345814, 0.55150973, 0.27992557],
    "x6": [2.08847712, 1.14956544, 1.74774918, 1.38989867, 1.23470891,
           1.92841686, 1.8899622, 1.84807891, 1.79729764, 0.92594999],
    "x7": [0.4962464, 0.0927571, 0.85785703, 0.04713553, 0.47200909,
           0.74234208, 0.95181965, 0.68507747, 0.93515104, 0.75820658],
    "y": [1, 0, 1, 0, 1, 1, 1, 0, 1, 1],
})
print("Tabla de entrada (7 variables x1..x7 + salida y):")
print(datos)


def fcbf(frame, columna_salida, lvs=0.2, lev=0.8, verboso=True):
    """
    Implementacion del algoritmo FCBF descrito en el PDF.

    frame: DataFrame con las variables de entrada + la columna de salida.
    columna_salida: nombre de la columna de salida (y).
    lvs: limite minimo de |correlacion| con la salida para conservar una
         variable de entrada.
    lev: limite a partir del cual dos variables de entrada se consideran
         redundantes entre si (|correlacion| >= lev).

    Regresa la lista de variables de entrada que sobreviven al filtrado.
    """
    salida = frame[columna_salida]
    entradas = [c for c in frame.columns if c != columna_salida]

    # --- Paso 1: correlacion de cada variable de entrada con la salida ---
    corr_con_salida = {c: frame[c].corr(salida) for c in entradas}
    if verboso:
        print("\nCorrelacion de cada variable de entrada con 'y':")
        print({c: round(v, 4) for c, v in corr_con_salida.items()})

    # --- Paso 2: eliminar las que tengan |correlacion| < lvs ---
    candidatas = [c for c in entradas if abs(corr_con_salida[c]) >= lvs]
    eliminadas_por_salida = [c for c in entradas if c not in candidatas]
    if verboso:
        print(f"\nEliminadas por baja correlacion con la salida (< {lvs}): {eliminadas_por_salida}")
        print(f"Quedan tras el paso 1: {candidatas}")

    # --- Paso 3: eliminar variables redundantes entre si ---
    # Se recorre la lista de candidatas en orden; por cada variable actual
    # se compara contra el resto de las que siguen en la lista. Si alguna
    # tiene |correlacion| >= lev con la actual, de las dos sólo sobrevive la
    # que tenga mayor |correlacion| con la salida (y toma el lugar de la
    # variable actual en la lista); el resto de las redundantes se eliminan.
    seleccionadas = list(candidatas)
    i = 0
    while i < len(seleccionadas):
        actual = seleccionadas[i]
        resto = seleccionadas[i + 1:]
        if not resto:
            break

        corr_con_actual = {c: frame[actual].corr(frame[c]) for c in resto}
        redundantes = [c for c in resto if abs(corr_con_actual[c]) >= lev]

        if verboso:
            print(f"\nCorrelacion de '{actual}' con el resto {resto}:")
            print({c: round(v, 4) for c, v in corr_con_actual.items()})

        if redundantes:
            # Entre 'actual' y sus redundantes, se queda la de mayor
            # |correlacion| con la salida.
            grupo = [actual] + redundantes
            ganadora = max(grupo, key=lambda c: abs(corr_con_salida[c]))
            if verboso:
                print(f"'{actual}' es redundante con {redundantes} (|corr| >= {lev}); "
                      f"se conserva '{ganadora}' (mayor relacion con la salida)")

            # Quitar todas las del grupo de la lista y reinsertar solo la ganadora
            # en la posicion donde estaba 'actual'.
            seleccionadas = [c for c in seleccionadas if c not in grupo]
            seleccionadas.insert(i, ganadora)
            # No avanzamos i todavia: hay que volver a comparar la ganadora
            # contra lo que le sigue ahora.
            continue

        i += 1

    return seleccionadas


# ---------------------------------------------------------------------------
# 2. Correr FCBF con los mismos parametros del PDF (lvs=0.2, lev=0.8)
# ---------------------------------------------------------------------------
variables_finales = fcbf(datos, "y", lvs=0.2, lev=0.8)
print(f"\nVariables finales tras FCBF: {variables_finales}")
print("Esperado segun el PDF: ['x6', 'x3', 'x5', 'x7'] (mismo contenido, el orden puede variar)")

assert set(variables_finales) == {"x6", "x3", "x5", "x7"}, \
    "El resultado no coincide con el esperado por el tutorial"

# ---------------------------------------------------------------------------
# 3. Construir el frame final con las variables seleccionadas + la salida
# ---------------------------------------------------------------------------
frame_final = datos[variables_finales + ["y"]]
print("\nFrame final (variables seleccionadas + salida):")
print(frame_final)

print("\nListo: FCBF implementado y verificado contra el resultado esperado del tutorial.")
