import customtkinter as ctk
from tkinter import messagebox
import re

from apd_simulator import simular_palabra
from gui_elements import add_transition_entry_to_app, remove_transition_entry_from_app, add_word_entry_to_app, remove_word_entry_from_app
from resolucion_adaptativa import obtener_geometria_adaptativa

class APDSimulatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Simulador de Autómatas Pushdown Deterministas")
        
        # Geometría adaptativa para la ventana principal
        geometria_calculada = obtener_geometria_adaptativa(self, 0.80) 
        self.geometry(geometria_calculada)
        self.resizable(True, True) # Aseguramos que la ventana sea redimensionable

        # --- Configuración de la cuadrícula principal de la ventana (2 FILAS) ---
        # Fila 0 (banner/configuración APD): weight=0 para que no se expanda en altura.
        # Quitamos maxsize ya que no es una opción válida. Con weight=0 y el diseño interno
        # de apd_config_frame, la altura se adaptará al contenido sin crecer excesivamente.
        self.grid_rowconfigure(0, weight=0, minsize=200) # Un minsize razonable para el contenido del banner
        
        # Fila 1 (contenido principal): weight=1 para que ocupe todo el espacio vertical restante.
        self.grid_rowconfigure(1, weight=1) 

        # Las columnas de la fila 1 (donde estarán transiciones y palabras) se expanden
        self.grid_columnconfigure(0, weight=1, minsize=200) # Columna para Transiciones (ajustado minsize)
        self.grid_columnconfigure(1, weight=1, minsize=200) # Columna para Palabras/Resultados (ajustado minsize)


        # --- Fila 1: Configuración del APD (ahora en la fila 0 principal) ---
        self.apd_config_frame = ctk.CTkFrame(self)
        self.apd_config_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Configuración de la cuadrícula dentro del apd_config_frame
        # Hemos ajustado los weights y minsize para que los elementos se distribuyan mejor horizontalmente
        # para que se expandan y no se amontonen.
        self.apd_config_frame.grid_columnconfigure(0, weight=1, minsize=150) # Columna para Estado Inicial y Finales
        self.apd_config_frame.grid_columnconfigure(1, weight=1, minsize=150) # Columna para Tipo de Aceptación
        
        # Todas las filas dentro de apd_config_frame con weight=0 (no se expanden en altura)
        # Esto es crucial para que el frame del banner no se estire más allá de lo necesario.
        # Los elementos se ajustarán a su tamaño ideal.
        self.apd_config_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=0) 

        # Reubicación de los elementos de Configuración del APD
        # Usamos columnspan para que el título se centre sobre ambas "subcolumnas" del banner
        ctk.CTkLabel(self.apd_config_frame, text="Configuración del APD", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        # Columna 0 de apd_config_frame
        ctk.CTkLabel(self.apd_config_frame, text="Estado Inicial:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.initial_state_entry = ctk.CTkEntry(self.apd_config_frame, placeholder_text="q0")
        self.initial_state_entry.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        ctk.CTkLabel(self.apd_config_frame, text="Estados Finales (ej: qf1,qf2):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.final_states_entry = ctk.CTkEntry(self.apd_config_frame, placeholder_text="qf")
        self.final_states_entry.grid(row=4, column=0, padx=5, pady=5, sticky="ew")
        
        # Columna 1 de apd_config_frame
        ctk.CTkLabel(self.apd_config_frame, text="Tipo de Aceptación:").grid(row=1, column=1, padx=5, pady=5, sticky="w")
        self.acceptance_type_var = ctk.StringVar(value="final")
        self.final_state_radio = ctk.CTkRadioButton(self.apd_config_frame, text="Por Estado Final",
                                                    variable=self.acceptance_type_var, value="final",
                                                    command=self.toggle_final_state_entry)
        self.final_state_radio.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.stack_empty_radio = ctk.CTkRadioButton(self.apd_config_frame, text="Por Stack Vacío",
                                                    variable=self.acceptance_type_var, value="stack",
                                                    command=self.toggle_final_state_entry)
        self.stack_empty_radio.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.toggle_final_state_entry() # Llamada inicial para establecer el estado correcto


        # --- Fila 2, Columna 1: Transiciones ---
        self.column2_frame = ctk.CTkFrame(self)
        self.column2_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        # Configuración de las filas del column2_frame
        self.column2_frame.grid_rowconfigure(0, weight=0) 
        self.column2_frame.grid_rowconfigure(1, weight=1) # ScrollableFrame: se expande en altura
        self.column2_frame.grid_rowconfigure(2, weight=0) 

        # Configuración de la columna del column2_frame
        self.column2_frame.grid_columnconfigure(0, weight=1) 

        ctk.CTkLabel(self.column2_frame, text="Definir Transiciones", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10, sticky="ew")

        self.transitions_scroll_frame = ctk.CTkScrollableFrame(self.column2_frame)
        self.transitions_scroll_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew") 

        self.transition_entries = []
        add_transition_entry_to_app(self)

        self.add_transition_button = ctk.CTkButton(self.column2_frame, text="+", command=lambda: add_transition_entry_to_app(self))
        self.add_transition_button.grid(row=2, column=0, pady=10, sticky="ew")


        # --- Fila 2, Columna 2: Palabras de Entrada y Resultados ---
        self.column3_frame = ctk.CTkFrame(self)
        self.column3_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        # Configuración de las filas del column3_frame
        self.column3_frame.grid_rowconfigure(0, weight=0) 
        self.column3_frame.grid_rowconfigure(1, weight=1) 
        self.column3_frame.grid_rowconfigure(2, weight=0) 

        # Configuración de la columna del column3_frame
        self.column3_frame.grid_columnconfigure(0, weight=1) 

        ctk.CTkLabel(self.column3_frame, text="Palabras de Entrada", font=("Arial", 16, "bold")).grid(row=0, column=0, pady=10, sticky="ew")

        self.words_scroll_frame = ctk.CTkScrollableFrame(self.column3_frame)
        self.words_scroll_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        self.word_entries = []
        add_word_entry_to_app(self)

        self.bottom_buttons_frame = ctk.CTkFrame(self.column3_frame, fg_color="transparent")
        self.bottom_buttons_frame.grid(row=2, column=0, pady=10, sticky="ew")
        self.bottom_buttons_frame.grid_columnconfigure(0, weight=1) 
        self.bottom_buttons_frame.grid_columnconfigure(1, weight=0) 

        self.add_word_button = ctk.CTkButton(self.bottom_buttons_frame, text="+", command=lambda: add_word_entry_to_app(self))
        self.add_word_button.grid(row=0, column=0, sticky="w", padx=10) 

        self.verify_button = ctk.CTkButton(self.bottom_buttons_frame, text="Verificar", command=self.verify_words)
        self.verify_button.grid(row=0, column=1, sticky="e", padx=10)


    def toggle_final_state_entry(self):
        """Habilita/deshabilita la entrada de estados finales según el tipo de aceptación."""
        if self.acceptance_type_var.get() == "final":
            self.final_states_entry.configure(state="normal", 
                                              fg_color=ctk.ThemeManager.theme["CTkEntry"]["fg_color"],
                                              text_color=ctk.ThemeManager.theme["CTkEntry"]["text_color"])
        else:
            self.final_states_entry.configure(state="disabled", 
                                              fg_color="grey50", # Un gris más oscuro para el modo oscuro, o un gris más claro para el modo claro.
                                              text_color="grey80") # Un gris claro para el texto cuando está deshabilitado
            # Nota: Los colores "greyXX" son una forma rápida. Para un control más preciso
            # podrías usar valores RGB o HEX, o basarte en el tema actual para "disabled_fg_color"
            # si existiera en la definición del tema de CustomTkinter.

    def parse_transitions(self):
        """
        Parsea las transiciones ingresadas por el usuario desde los campos separados.
        Retorna un diccionario de transiciones o None si hay errores/no determinismo.
        """
        parsed_transitions = {}
        for item in self.transition_entries:
            estado_actual = item['estado_actual'].get().strip()
            simbolo_entrada = item['simbolo_entrada'].get().strip()
            tope_stack = item['tope_stack'].get().strip()
            estado_siguiente = item['estado_siguiente'].get().strip()
            simbolos_a_apilar = item['simbolos_a_apilar'].get().strip()

            # Validar campos obligatorios
            if not estado_actual:
                messagebox.showerror("Error de Transición", "El 'Estado Actual' no puede estar vacío.")
                return None
            if not estado_siguiente:
                messagebox.showerror("Error de Transición", "El 'Estado Siguiente' no puede estar vacío.")
                return None
            
            # Normalizar 'ε' (ingresado por el usuario o campo vacío) a cadena vacía '' para la lógica interna
            simbolo_entrada_norm = '' if simbolo_entrada == 'ε' or simbolo_entrada == '' else simbolo_entrada
            tope_stack_norm = '' if tope_stack == 'ε' or tope_stack == '' else tope_stack
            simbolos_a_apilar_norm = '' if simbolos_a_apilar == 'ε' or simbolos_a_apilar == '' else simbolos_a_apilar
            
            valid_char_pattern = re.compile(r'^[a-zA-Z0-9_]*$')

            if not valid_char_pattern.match(estado_actual):
                messagebox.showerror("Error de Formato", f"El 'Estado Actual' '{estado_actual}' contiene caracteres no permitidos. Use solo alfanuméricos y guiones bajos.")
                return None
            if not valid_char_pattern.match(estado_siguiente):
                messagebox.showerror("Error de Formato", f"El 'Estado Siguiente' '{estado_siguiente}' contiene caracteres no permitidos. Use solo alfanuméricos y guiones bajos.")
                return None
            if not valid_char_pattern.match(simbolo_entrada) and simbolo_entrada != 'ε':
                messagebox.showerror("Error de Formato", f"El 'Símbolo de Entrada' '{simbolo_entrada}' contiene caracteres no permitidos. Use solo alfanuméricos, guiones bajos o 'ε'.")
                return None
            if not valid_char_pattern.match(tope_stack) and tope_stack != 'ε':
                messagebox.showerror("Error de Formato", f"El 'Tope de Pila' '{tope_stack}' contiene caracteres no permitidos. Use solo alfanuméricos, guiones bajos o 'ε'.")
                return None
            if not valid_char_pattern.match(simbolos_a_apilar) and simbolos_a_apilar != 'ε':
                messagebox.showerror("Error de Formato", f"El 'Nuevo Tope Pila' '{simbolos_a_apilar}' contiene caracteres no permitidos. Use solo alfanuméricos, guiones bajos o 'ε'.")
                return None


            clave_transicion = (estado_actual, simbolo_entrada_norm, tope_stack_norm)

            # --- Verificación de Determinismo (Mejorada) ---
            if clave_transicion in parsed_transitions:
                messagebox.showerror("Error de Determinismo", f"Transición duplicada detectada para la clave: ({estado_actual}, '{simbolo_entrada_norm}', '{tope_stack_norm}'). Un APD debe ser determinista.")
                return None

            if simbolo_entrada_norm == '':
                for (e_act, s_ent, t_stack) in parsed_transitions:
                    if e_act == estado_actual and t_stack == tope_stack_norm and s_ent != '':
                        messagebox.showerror("Error de Determinismo", f"Conflicto de transición: Ya existe una transición para ({estado_actual}, '{s_ent}', '{tope_stack_norm}') y se intentó agregar una transición épsilon ({estado_actual}, 'ε', '{tope_stack_norm}'). Esto hace al APD no determinista.")
                        return None
            else:
                if (estado_actual, '', tope_stack_norm) in parsed_transitions:
                     messagebox.showerror("Error de Determinismo", f"Conflicto de transición: Ya existe una transición épsilon para ({estado_actual}, 'ε', '{tope_stack_norm}') y se intentó agregar una transición para ({estado_actual}, '{simbolo_entrada_norm}', '{tope_stack_norm}'). Esto hace al APD no determinista.")
                     return None
            # --- Fin Verificación de Determinismo ---

            parsed_transitions[clave_transicion] = (estado_siguiente, simbolos_a_apilar_norm)
        
        if not parsed_transitions:
            messagebox.showerror("Error de Entrada", "Debe ingresar al menos una transición.")
            return None
        
        return parsed_transitions

    def verify_words(self):
        """
        Recopila la configuración del APD y las palabras,
        luego ejecuta el simulador y muestra los resultados.
        """
        estado_inicial = self.initial_state_entry.get().strip()
        if not estado_inicial:
            messagebox.showerror("Error de Configuración", "El estado inicial no puede estar vacío.")
            return

        tipo_aceptacion = self.acceptance_type_var.get()
        estados_finales = set()
        if tipo_aceptacion == "final":
            final_states_str = self.final_states_entry.get().strip()
            if not final_states_str:
                messagebox.showerror("Error de Configuración", "Debe especificar al menos un estado final si la aceptación es por estado final.")
                return
            estados_finales = set(s.strip() for s in final_states_str.split(','))
            if any(not s for s in estados_finales): 
                messagebox.showerror("Error de Configuración", "La lista de estados finales contiene un elemento vacío. Revise la separación por comas.")
                return

        transiciones = self.parse_transitions()
        if transiciones is None:
            return

        palabras_entrada = []
        for item in self.word_entries:
            word = item['entry'].get().strip()
            if word:
                palabras_entrada.append((word, item['result_label']))
            else:
                item['result_label'].configure(text="")

        if not palabras_entrada:
            messagebox.showwarning("Advertencia", "No se han ingresado palabras para verificar.")
            return

        for palabra, result_label in palabras_entrada:
            aceptada = simular_palabra(palabra, transiciones, estado_inicial, tipo_aceptacion, estados_finales)
            if aceptada:
                result_label.configure(text="Aceptada", text_color="green")
            else:
                result_label.configure(text="Rechazada", text_color="red")

if __name__ == "__main__":
    app = APDSimulatorApp()
    app.mainloop()