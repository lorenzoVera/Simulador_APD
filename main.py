import customtkinter as ctk
from tkinter import messagebox
import re

from apd_simulator import leer_palabra
from gui_elements import agregar_transicion, eliminar_transicion, agregar_palabra, eliminar_palabra
from resolucion_adaptativa import resolucion_adaptativa
from verifica_estado_final import verificar_estado_final
from tkinter import filedialog
from apd_file_io import cargar_apd_desde_txt, guardar_apd_a_txt
from gui_elements import clear_all_transition_entries
from gui_elements import agregar_transicion

class APDSimulatorApp(ctk.CTk):
    def __init__(ventana):
        super().__init__()

        ventana.title("Simulador de Autómatas Pushdown Deterministas")
        
        # Geometría adaptativa para la ventana principal
        resolucion_calculada = resolucion_adaptativa(ventana, 0.80) 
        ventana.geometry(resolucion_calculada)
        ventana.resizable(True, True)
        ventana.minsize(1000, 500) 

        ventana.grid_rowconfigure(0, weight=0, minsize=200)
        ventana.grid_rowconfigure(1, weight=1)
        ventana.grid_columnconfigure(0, weight=1, minsize=200)
        ventana.grid_columnconfigure(1, weight=1, minsize=200)

        # --- Configuración del APD ---
        ventana.config_frame = ctk.CTkFrame(ventana)
        ventana.config_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        ventana.config_frame.grid_columnconfigure(0, weight=1, minsize=150)
        ventana.config_frame.grid_columnconfigure(1, weight=1, minsize=150)
        ventana.config_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=0)

        ctk.CTkLabel(ventana.config_frame, text="Configuración del APD", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        btn_cargar = ctk.CTkButton(ventana.config_frame, text="Cargar datos desde TXT", command=ventana.cargar_desde_txt)
        btn_cargar.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        btn_guardar = ctk.CTkButton(ventana.config_frame, text="Guardar datos a TXT", command=ventana.guardar_a_txt)
        btn_guardar.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(ventana.config_frame, text="Estado Inicial:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ventana.entrada_estados_iniciales = ctk.CTkEntry(ventana.config_frame, placeholder_text="q0")
        ventana.entrada_estados_iniciales.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(ventana.config_frame, text="Estados Finales (ej: qf1,qf2):").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        ventana.entrada_estados_finales = ctk.CTkEntry(ventana.config_frame, placeholder_text="qf")
        ventana.entrada_estados_finales.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(ventana.config_frame, text="Tipo de Aceptación:").grid(row=2, column=1, padx=5, pady=5, sticky="w")
        ventana.tipo_aceptacion_var = ctk.StringVar(value="final")
        ventana.estado_final_boton = ctk.CTkRadioButton(ventana.config_frame, text="Por Estado Final",
                                                    variable=ventana.tipo_aceptacion_var, value="final",
                                                    command=ventana.cambiar_aceptacion)
        ventana.estado_final_boton.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ventana.stack_vacio_boton = ctk.CTkRadioButton(ventana.config_frame, text="Por Stack Vacío",
                                                    variable=ventana.tipo_aceptacion_var, value="stack",
                                                    command=ventana.cambiar_aceptacion)
        ventana.stack_vacio_boton.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        ventana.cambiar_aceptacion()

        # --- Transiciones ---
        ventana.columna2 = ctk.CTkFrame(ventana)
        ventana.columna2.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        ventana.columna2.grid_rowconfigure(0, weight=0)
        ventana.columna2.grid_rowconfigure(1, weight=1)
        ventana.columna2.grid_rowconfigure(2, weight=0)
        ventana.columna2.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(ventana.columna2, text="Definir Transiciones \n(Considerar R símbolo inicial del stack)", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10, sticky="ew")

        ventana.transiciones_frame = ctk.CTkScrollableFrame(ventana.columna2)
        ventana.transiciones_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        ventana.transiciones_frame.grid_columnconfigure(0, weight=1)

        ventana.transiciones_entrada = []
        agregar_transicion(ventana)

        ventana.agregar_transicion_boton = ctk.CTkButton(ventana.columna2, text="+", command=lambda: agregar_transicion(ventana))
        ventana.agregar_transicion_boton.grid(row=2, column=0, pady=10, sticky="ew")

        # --- Palabras de Entrada y Resultados ---
        ventana.columna3 = ctk.CTkFrame(ventana)
        ventana.columna3.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        ventana.columna3.grid_rowconfigure(0, weight=0)
        ventana.columna3.grid_rowconfigure(1, weight=1)
        ventana.columna3.grid_rowconfigure(2, weight=0)
        ventana.columna3.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(ventana.columna3, text="Palabras de Entrada", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10, sticky="ew")

        ventana.palabras_frame = ctk.CTkScrollableFrame(ventana.columna3)
        ventana.palabras_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        ventana.palabras_frame.grid_columnconfigure(0, weight=1)

        ventana.entrada_palabras = []
        agregar_palabra(ventana)

        ventana.boton = ctk.CTkFrame(ventana.columna3, fg_color="transparent")
        ventana.boton.grid(row=2, column=0, pady=10, sticky="ew")
        ventana.boton.grid_columnconfigure(0, weight=1)
        ventana.boton.grid_columnconfigure(1, weight=0)

        ventana.agregar_palabra_boton = ctk.CTkButton(ventana.boton, text="+", command=lambda: agregar_palabra(ventana))
        ventana.agregar_palabra_boton.grid(row=0, column=0, sticky="w", padx=10)

        ventana.verificar_boton = ctk.CTkButton(ventana.boton, text="Verificar", command=ventana.verificar_palabra)
        ventana.verificar_boton.grid(row=0, column=1, sticky="e", padx=10)

    def cambiar_aceptacion(ventana):
        if ventana.tipo_aceptacion_var.get() == "final":
            ventana.entrada_estados_finales.configure(state="normal", 
                                              fg_color=ctk.ThemeManager.theme["CTkEntry"]["fg_color"],
                                              text_color=ctk.ThemeManager.theme["CTkEntry"]["text_color"])
        else:
            ventana.entrada_estados_finales.configure(state="disabled", 
                                              fg_color="grey50",
                                              text_color="grey80")

    def parsear_transiciones(ventana):
        transiciones = {}
        for transicion in ventana.transiciones_entrada:
            estado_actual = transicion['estado_actual'].get().strip()
            simbolo_entrada = transicion['simbolo_entrada'].get().strip()
            tope_stack = transicion['tope_stack'].get().strip()
            estado_siguiente = transicion['estado_siguiente'].get().strip()
            simbolos_a_apilar = transicion['simbolos_a_apilar'].get().strip()

            if not estado_actual:
                messagebox.showerror("Error de Transición", "El 'Estado Actual' no puede estar vacío.")
                return None
            if not estado_siguiente:
                messagebox.showerror("Error de Transición", "El 'Estado Siguiente' no puede estar vacío.")
                return None
            
            simbolo_entrada_norm = '' if simbolo_entrada == 'ε' or simbolo_entrada == '' else simbolo_entrada
            tope_stack_norm = '' if tope_stack == 'ε' or tope_stack == '' else tope_stack
            simbolos_a_apilar_norm = '' if simbolos_a_apilar == 'ε' or simbolos_a_apilar == '' else simbolos_a_apilar
            
            patron_valido = re.compile(r'^[a-zA-Z0-9_]*$')

            if not patron_valido.match(estado_actual):
                messagebox.showerror("Error de Formato", f"El 'Estado Actual' '{estado_actual}' contiene caracteres no permitidos. Use solo alfanuméricos y guiones bajos.")
                return None
            if not patron_valido.match(estado_siguiente):
                messagebox.showerror("Error de Formato", f"El 'Estado Siguiente' '{estado_siguiente}' contiene caracteres no permitidos. Use solo alfanuméricos y guiones bajos.")
                return None
            if not patron_valido.match(simbolo_entrada) and simbolo_entrada != 'ε':
                messagebox.showerror("Error de Formato", f"El 'Símbolo de Entrada' '{simbolo_entrada}' contiene caracteres no permitidos. Use solo alfanuméricos, guiones bajos o 'ε'.")
                return None
            if not patron_valido.match(tope_stack) and tope_stack != 'ε':
                messagebox.showerror("Error de Formato", f"El 'Tope de Pila' '{tope_stack}' contiene caracteres no permitidos. Use solo alfanuméricos, guiones bajos o 'ε'.")
                return None
            if not patron_valido.match(simbolos_a_apilar) and simbolos_a_apilar != 'ε':
                messagebox.showerror("Error de Formato", f"El 'Nuevo Tope Pila' '{simbolos_a_apilar}' contiene caracteres no permitidos. Use solo alfanuméricos, guiones bajos o 'ε'.")
                return None

            clave_transicion = (estado_actual, simbolo_entrada_norm, tope_stack_norm)

            if clave_transicion in transiciones:
                messagebox.showerror("Error de Determinismo", f"Transición duplicada detectada para la clave: ({estado_actual}, '{simbolo_entrada_norm}', '{tope_stack_norm}'). Un APD debe ser determinista.")
                return None

            if simbolo_entrada_norm == '':
                for (e_act, s_ent, t_stack) in transiciones:
                    if e_act == estado_actual and t_stack == tope_stack_norm and s_ent != '':
                        messagebox.showerror("Error de Determinismo", f"Conflicto de transición: Ya existe una transición para ({estado_actual}, '{s_ent}', '{tope_stack_norm}') y se intentó agregar una transición épsilon ({estado_actual}, 'ε', '{tope_stack_norm}'). Esto hace al APD no determinista.")
                        return None
            else:
                if (estado_actual, '', tope_stack_norm) in transiciones:
                     messagebox.showerror("Error de Determinismo", f"Conflicto de transición: Ya existe una transición épsilon para ({estado_actual}, 'ε', '{tope_stack_norm}') y se intentó agregar una transición para ({estado_actual}, '{simbolo_entrada_norm}', '{tope_stack_norm}'). Esto hace al APD no determinista.")
                     return None

            transiciones[clave_transicion] = (estado_siguiente, simbolos_a_apilar_norm)
        
        if not transiciones:
            messagebox.showerror("Error de Entrada", "Debe ingresar al menos una transición.")
            return None
        
        return transiciones

    def verificar_palabra(ventana):
        estado_inicial = ventana.entrada_estados_iniciales.get().strip()
        if not estado_inicial:
            messagebox.showerror("Error de Configuración", "El estado inicial no puede estar vacío.")
            return

        tipo_aceptacion = ventana.tipo_aceptacion_var.get()
        estados_finales = set()
        if tipo_aceptacion == "final":
            estados_finales_str = ventana.entrada_estados_finales.get().strip()
            if not estados_finales_str:
                messagebox.showerror("Error de Configuración", "Debe especificar al menos un estado final si la aceptación es por estado final.")
                return
            estados_finales = set(s.strip() for s in estados_finales_str.split(','))
            if any(not s for s in estados_finales): 
                messagebox.showerror("Error de Configuración", "La lista de estados finales contiene un elemento vacío. Revise la separación por comas.")
                return

        transiciones = ventana.parsear_transiciones()
        if transiciones is None:
            return

        if tipo_aceptacion == "final":
            verificar_estado_final(transiciones, estados_finales)

        palabras_entrada = []
        for transicion in ventana.entrada_palabras:
            palabra = transicion['entry'].get().strip()
            palabras_entrada.append((palabra, transicion['resultado_label'] if 'resultado_label' in transicion else transicion['result_label']))

        if not palabras_entrada:
            messagebox.showwarning("Advertencia", "No se han ingresado palabras para verificar.")
            return

        for palabra, resultado_label in palabras_entrada:
            aceptada = leer_palabra(palabra, transiciones, estado_inicial, tipo_aceptacion, estados_finales)
            if aceptada:
                resultado_label.configure(text="Aceptada", text_color="green")
            else:
                resultado_label.configure(text="Rechazada", text_color="red")

    def cargar_desde_txt(ventana):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if not ruta:
            return
        estado_inicial, estados_finales, tipo_aceptacion, transiciones = cargar_apd_desde_txt(ruta)
        ventana.entrada_estados_iniciales.delete(0, "end")
        ventana.entrada_estados_iniciales.insert(0, estado_inicial)
        ventana.entrada_estados_finales.delete(0, "end")
        ventana.entrada_estados_finales.insert(0, estados_finales)
        if tipo_aceptacion.strip().lower() in ["stack", "stack vacio", "vacia"]:
            ventana.tipo_aceptacion_var.set("stack")
        else:
            ventana.tipo_aceptacion_var.set("final")
        ventana.cambiar_aceptacion()
        ventana.update_idletasks()
        clear_all_transition_entries(ventana)
        for t in transiciones:
            agregar_transicion(ventana)
            partes = t.replace("->", ",").split(",")
            while len(partes) < 5:
                partes.append("")
            entry = ventana.transiciones_entrada[-1]
            entry['estado_actual'].insert(0, partes[0])
            entry['simbolo_entrada'].insert(0, partes[1])
            entry['tope_stack'].insert(0, partes[2])
            entry['estado_siguiente'].insert(0, partes[3])
            entry['simbolos_a_apilar'].insert(0, partes[4])
        if not transiciones:
            agregar_transicion(ventana)

    def guardar_a_txt(ventana):
        ruta = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        if not ruta:
            return
        estado_inicial = ventana.entrada_estados_iniciales.get()
        estados_finales = ventana.entrada_estados_finales.get()
        tipo_aceptacion = ventana.tipo_aceptacion_var.get()
        transiciones = []
        for entry in ventana.transiciones_entrada:
            t = f"{entry['estado_actual'].get()},{entry['simbolo_entrada'].get()},{entry['tope_stack'].get()}->{entry['estado_siguiente'].get()},{entry['simbolos_a_apilar'].get()}"
            transiciones.append(t)
        guardar_apd_a_txt(ruta, estado_inicial, estados_finales, tipo_aceptacion, transiciones)

if __name__ == "__main__":
    app = APDSimulatorApp()
    app.mainloop()
