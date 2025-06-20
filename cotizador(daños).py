# -*- coding: utf-8 -*-
"""cotizador(daños).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1cZo9mLi7NmnGYcvTt8cbFTBcPRdC35HI
"""

# Conecta la carpeta a la cuenta de drive para el proyecto
from google.colab import drive
drive.mount("/content/drive/")

import os
# crea la carpeta donde se tiene los archivos
carpeta_drive = "/content/drive/MyDrive/CI/"
os.makedirs(carpeta_drive, exist_ok=True) # Crea la carpeta si no existe
os.chdir(carpeta_drive)

# -*- coding: utf-8 -*-
"""
Cotizador de Seguros contra Incendio y Riesgos Financieros
"""

import pandas as pd

# CONSTANTES
GASTOS_ADM = 0.10
GASTOS_ADQ = 0.18
MARGEN_UTIL = 0.07
TASA_FINANCIAMIENTO = 0.08

def cargar_datos(excel_path):
    """Carga y procesa los datos del archivo Excel"""
    try:
        xls = pd.ExcelFile(excel_path)

        # FRECUENCIA
        freq_df = pd.read_excel(xls, sheet_name="P y CR")
        freq_df.columns = [
            "Cobertura", "Tipo de bien", "Frec_2019", "Frec_2020", "Frec_2021",
            "Frec_2022", "Frec_2023", "Frecuencia_total", *[f"col{i}" for i in range(9)]
        ]
        freq_df = freq_df.dropna(subset=["Frecuencia_total"])
        freq_df = freq_df[freq_df["Cobertura"] != "COBERTURA"]
        freq_df = freq_df[["Cobertura", "Tipo de bien", "Frecuencia_total"]]

        # SEVERIDAD
        calc_df = pd.read_excel(xls, sheet_name="Cálculos")
        sev_section = calc_df.iloc[13:22, [0, 1, 2, 19]]
        sev_section.columns = ["Cobertura", "Tipo de bien", "N_siniestros", "Monto_total"]
        sev_df = sev_section.dropna(subset=["Cobertura", "Tipo de bien", "N_siniestros", "Monto_total"])
        sev_df = sev_df[sev_df["Cobertura"] != "COBERTURA"]
        sev_df["N_siniestros"] = pd.to_numeric(sev_df["N_siniestros"], errors='coerce')
        sev_df["Monto_total"] = pd.to_numeric(sev_df["Monto_total"], errors='coerce')
        sev_df["Severidad"] = sev_df["Monto_total"] / sev_df["N_siniestros"]
        sev_df = sev_df[["Cobertura", "Tipo de bien", "Severidad"]]

        # PRIMA BASE
        merged = pd.merge(freq_df, sev_df, on=["Cobertura", "Tipo de bien"])
        merged["Prima_riesgo_base"] = merged["Frecuencia_total"] * merged["Severidad"]

        primas = {
            (row["Tipo de bien"], row["Cobertura"]): row["Prima_riesgo_base"]
            for _, row in merged.iterrows()
        }

        # FACTORES
        estado_df = pd.read_excel(xls, sheet_name="CR Estatal", usecols="A:B", skiprows=1)
        factores_estado = dict(zip(estado_df.iloc[:, 1], estado_df.iloc[:, 0]))

        deducible_df = pd.read_excel(xls, sheet_name="deducible fd", usecols="A:B")
        deducible_df.columns = ["Deducible", "Factor"]
        factores_deducible = dict(zip(deducible_df["Deducible"], deducible_df["Factor"])

        return primas, factores_estado, factores_deducible

    except Exception as e:
        raise ValueError(f"Error al cargar archivo Excel: {str(e)}")

def mostrar_menu(opciones, titulo):
    """Muestra un menú de opciones numeradas"""
    print(f"\n{titulo}:")
    for i, opcion in enumerate(opciones, 1):
        print(f"  {i}. {opcion}")

def seleccionar_opcion(opciones, mensaje):
    """Valida la selección del usuario"""
    while True:
        try:
            seleccion = int(input(mensaje)) - 1
            if 0 <= seleccion < len(opciones):
                return opciones[seleccion]
            print(f"Por favor ingrese un número entre 1 y {len(opciones)}")
        except ValueError:
            print("Entrada inválida. Por favor ingrese un número.")

def cotizar(tipo_bien, cobertura, suma_asegurada, estado, deducible,
            primas_dict, factores_estado, factores_deducible):
    """Calcula la cotización completa"""
    clave = (tipo_bien, cobertura)
    prima_riesgo_base = primas_dict.get(clave)

    if prima_riesgo_base is None:
        raise ValueError("Combinación de tipo de bien y cobertura no válida")

    factor_estado = factores_estado.get(estado, 1.0)
    factor_deducible = factores_deducible.get(deducible, 1.0)

    prima_riesgo_ajustada = prima_riesgo_base * factor_estado * factor_deducible
    prima_tarifa = prima_riesgo_ajustada / (1 - GASTOS_ADM - GASTOS_ADQ - MARGEN_UTIL)
    prima_financiada = prima_tarifa * (1 + TASA_FINANCIAMIENTO)

    return {
        "Prima base": round(prima_riesgo_base, 2),
        "Prima ajustada": round(prima_riesgo_ajustada, 2),
        "Prima tarifa": round(prima_tarifa, 2),
        "Prima total": round(prima_financiada, 2),
        "Factor estado": factor_estado,
        "Factor deducible": factor_deducible
    }

def main():
    """Función principal del programa"""
    print("\n" + "="*50)
    print("  SISTEMA DE COTIZACIÓN DE SEGUROS CONTRA INCENDIO")
    print("="*50)

    try:
        # Carga de datos
        ruta_excel = "seguro incendios.xlsx"
        primas, factores_estado, factores_deducible = cargar_datos(ruta_excel)

        # Selección de opciones
        tipos_disponibles = sorted(set(k[0] for k in primas))
        coberturas_disponibles = sorted(set(k[1] for k in primas))

        tipo_bien = seleccionar_opcion(tipos_disponibles, "Seleccione el tipo de bien (número): ")
        cobertura = seleccionar_opcion(coberturas_disponibles, "Seleccione la cobertura (número): ")

        # Datos adicionales
        suma_asegurada = float(input("\nIngrese el monto a asegurar: $"))
        deducible = int(input("Ingrese el deducible (ej. 10000, 20000): $"))
        estado = input("Ingrese el estado: ").title()

        # Cálculo y resultados
        resultado = cotizar(
            tipo_bien, cobertura, suma_asegurada, estado, deducible,
            primas, factores_estado, factores_deducible
        )

        # Presentación de resultados
        print("\n" + "="*50)
        print("  RESULTADO DE COTIZACIÓN")
        print("="*50)
        for k, v in resultado.items():
            print(f"{k:>20}: {v:>10,.2f}" if isinstance(v, (float, int)) else f"{k:>20}: {v:>10}")
        print("="*50)

    except Exception as e:
        print(f"\nERROR: {str(e)}")
        print("Por favor verifique los datos e intente nuevamente.")

if __name__ == "__main__":
    main()