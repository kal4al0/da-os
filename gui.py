import tkinter as tk
from tkinter import ttk
from tkinter import font
from daños import CotizadorSeguros

def submitForm():
    _defaultTxt =  "Cotizador de Tarifas"

    try: # Obtener valuación
        _valuacion = float(valuacion.get())    
        board["text"] = _defaultTxt
        if _valuacion < 0:
            board["text"] = "Suma Asegurada >= 0"
            return
    except ValueError:
        board["text"] = "Suma Asegurada >= 0"
        return

    # Evaluación seguro
    # df = reporte[reporte["estado"] == estado.get()]
    # df = df[df["tipo_bien"] == tipo_bien.get()]
    # Prima de Tarifa
    pr = cotizador.calcular_prima_riesgo()
    pt = cotizador.calcular_prima_tarifa(pr) * _valuacion

    # Deducible
    _valuacion = float(valuacion.get())    
    _deducible = float(deducible.get())
    _siniestro = float(siniestro.get())
    _pago_con_deducible = cotizador.pago_con_deducible(_siniestro, _deducible)

    # Muestra 
    _pt.config(text="$ {:,.2f}".format(pt))
    _vt.config(text="$ {:,.2f}".format(_pago_con_deducible))



cotizador = CotizadorSeguros()
reporte = cotizador.generar_reporte("reporte_seguros.xlsx")

# App
root = tk.Tk()
root.title("Cotizador - HORIZONTES Seguros")
_font = font.nametofont("TkDefaultFont")
_font["size"] = 15
_font = font.nametofont("TkTextFont")
_font["size"] = 15

# Variables
valuacion = tk.StringVar()
tipo_bien = tk.StringVar()
estado    = tk.StringVar()
prima_tar = tk.StringVar()
deducible = tk.StringVar()
cobertura = tk.StringVar()

board = tk.Label(root, text="Cotizador de Tarifas")
board.grid(row=0, columnspan=2, padx=7, pady=7)
imgobj = tk.PhotoImage(file="logo.png")
tk.Label(root, image=imgobj).grid(row=0, column=2, padx=0, pady=1)

ttk.Label(root, text="Valuación").grid(row=1, column=0)
ttk.Entry(root, textvariable=valuacion).grid(row=1, column=1, pady=4)
ttk.Label(root, text="Tipo de Bien").grid(row=2, column=0)
tipo_bien_combobox = ttk.Combobox(root, textvariable=tipo_bien)
tipo_bien_combobox.grid(row=2, column=1, pady=4)
ttk.Label(root, text="Estado").grid(row=3, column=0)
estado_combobox = ttk.Combobox(root, textvariable=estado)
estado_combobox.grid(row=3, column=1, pady=4)
ttk.Label(root, text="Deducible").grid(row=5, column=0)
deducible_combobox = ttk.Combobox(root, textvariable=deducible)
deducible_combobox.grid(row=5, column=1, pady=4)
cobertura_combobox = ttk.Combobox(root, textvariable=cobertura)
ttk.Label(root, text="Cobertura").grid(row=6, column=0)
cobertura_combobox.grid(row=6, column=1, pady=4)



tipo_bien_combobox["values"] = ("Contenidos", "Edificio", "Pérdidas Consecuenciales")
estado_combobox["values"] = ("Aguascalientes",
                     "Baja California",
                     "Baja California Sur",
                     "Campeche",
                     "Chiapas",
                     "Chihuahua",
                     "CDMX",
                     "Coahuila de Zaragoza",
                     "Colima",
                     "Durango",
                     "Guanajuato",
                     "Guerrero",
                     "Hidalgo",
                     "Jalisco",
                     "México",
                     "Michoacán de Ocampo",
                     "Morelos",
                     "Nayarit",
                     "Nuevo León",
                     "Oaxaca",
                     "Puebla",
                     "Querétaro",
                     "Quintana Roo",
                     "San Luis Potosí",
                     "Sinaloa",
                     "Sonora",
                     "Tabasco",
                     "Tamaulipas",
                     "Tlaxcala",
                     "Veracruz de Ignacio de la Llave",
                     "Yucatán",
                     "Zacatecas")
deducible_combobox["values"] = tuple([500*i for i in range(100)])
cobertura_combobox["values"] = ("Todo Riesgo", "Incendio, rayo y explosión", "Gastos Extras para Casa Habitación")

f_results = ttk.Frame(root, borderwidth=5, relief="ridge")
ttk.Label(f_results, text="Prima de tarifa").grid(row=1, column=1, sticky="W")
_pt = ttk.Label(f_results, text="$ ")
_pt.grid(column=1, sticky="E")
ttk.Label(f_results, text="Porcentaje ").grid(column=1, sticky='W')
_vt = ttk.Label(f_results, text="% ")
_vt.grid(column=1, sticky="E")

ttk.Button(root, text="Calcular", command=submitForm).grid(row=5, column=2, rowspan=2, pady=5)
f_results.grid(row=1, column=2, rowspan=4, sticky="NSEW", padx=4)

# Variables
# valuacion = tk.StringVar()
# siniestro = tk.StringVar()

# ttk.Label(root, text="Valuación").grid(row=7, column=0)
# ttk.Entry(root, textvariable=valuacion).grid(row=7, column=1, pady=4)
# ttk.Label(root, text="Siniestro").grid(row=8, column=0)
# ttk.Entry(root, textvariable=siniestro).grid(row=8, column=1, pady=4)
# ttk.Label(root, text="Deducible").grid(row=9, column=0)
# deducible_combobox2 = ttk.Combobox(root, textvariable=deducible)
# deducible_combobox2.grid(row=9, column=1, pady=4)
# # ttk.Label(root, text="Siniestro").grid(row=5, column=0)
# # ttk.Entry(root, textvariable=valuacion).grid(row=5, column=1, pady=4)
# 
# deducible_combobox2["values"] = tuple([500*i for i in range(100)])
# 
# f_deducible = ttk.Frame(root, borderwidth=5, relief="ridge")
# # ttk.Label(f_deducible, text="Prima de Deducible").grid(row=1, column=1, sticky="W")
# # _pt = ttk.Label(f_deducible, text="$ ")
# # _pt.grid(column=1, sticky="E")
# ttk.Label(f_deducible, text="Deducible").grid(column=1, sticky='W')
# _vt = ttk.Label(f_deducible, text="$ ")
# _vt.grid(column=1, sticky="E")
# 
# ttk.Button(root, text="Calcular", command=computeDeductible).grid(row=10, column=2, rowspan=2, pady=5)
# 
# f_deducible.grid(row=7, column=2, rowspan=3, sticky="NSEW", padx=4)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

root.mainloop()
