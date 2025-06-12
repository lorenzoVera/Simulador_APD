# gui_elements.py
import customtkinter as ctk

def agregar_transicion(app):
    """Añade un nuevo conjunto de campos de entrada para una transición a la app."""
    frame = ctk.CTkFrame(app.transiciones_frame)
    frame.grid(row=len(app.transiciones_entrada), column=0, padx=2, pady=5, sticky="ew")
    
    # Configuración de las columnas dentro de cada frame de transición
    frame.grid_columnconfigure(0, weight=1)  # Estado Actual
    frame.grid_columnconfigure(1, weight=2)  # Símbolo de Entrada
    frame.grid_columnconfigure(2, weight=1)  # Tope de la Pila
    frame.grid_columnconfigure(3, weight=0)  # "->" (fijo, pequeño)
    frame.grid_columnconfigure(4, weight=1)  # Estado Siguiente
    frame.grid_columnconfigure(5, weight=1)  # Símbolos a Apilar
    frame.grid_columnconfigure(6, weight=0)  # Botón eliminar (fijo)

    # Estado Actual
    ctk.CTkLabel(frame, text="Estado:").grid(row=0, column=0, sticky="w")
    e_actual = ctk.CTkEntry(frame) 
    e_actual.grid(row=1, column=0, padx=2, sticky="ew")

    # Símbolo de Entrada
    ctk.CTkLabel(frame, text="Palabra").grid(row=0, column=1, sticky="w")
    e_entrada = ctk.CTkEntry(frame, placeholder_text="ε")
    e_entrada.grid(row=1, column=1, padx=2, sticky="ew")

    # Tope de la Pila
    ctk.CTkLabel(frame, text="Tope Pila:").grid(row=0, column=2, sticky="w")
    e_tope = ctk.CTkEntry(frame, placeholder_text="ε")
    e_tope.grid(row=1, column=2, padx=2, sticky="ew")

    ctk.CTkLabel(frame, text="->").grid(row=1, column=3, padx=5)

    # Estado Siguiente
    ctk.CTkLabel(frame, text="Estado Siguiente:").grid(row=0, column=4, sticky="w")
    e_siguiente = ctk.CTkEntry(frame)
    e_siguiente.grid(row=1, column=4, padx=2, sticky="ew")

    # Símbolos a Apilar
    ctk.CTkLabel(frame, text="Nuevo Tope Pila:").grid(row=0, column=5, sticky="w")
    e_apilar = ctk.CTkEntry(frame, placeholder_text="ε")
    e_apilar.grid(row=1, column=5, padx=2, sticky="ew")
    
    # Botón para eliminar esta transición
    remove_button = ctk.CTkButton(frame, text="-", width=30, command=lambda f=frame: eliminar_transicion(app, f))
    remove_button.grid(row=1, column=6, padx=2)

    app.transiciones_entrada.append({
        'frame': frame,
        'estado_actual': e_actual,
        'simbolo_entrada': e_entrada,
        'tope_stack': e_tope,
        'estado_siguiente': e_siguiente,
        'simbolos_a_apilar': e_apilar
    })
    app.transiciones_frame.update_idletasks()

def eliminar_transicion(app, frame_to_remove):
    """Elimina un conjunto de campos de entrada de transición de la app."""
    for i, item in enumerate(app.transiciones_entrada):
        if item['frame'] == frame_to_remove:
            item['frame'].destroy()
            del app.transiciones_entrada[i]
            for j in range(i, len(app.transiciones_entrada)):
                # Aseguramos que la reubicación use sticky="ew" para mantener la expansión
                app.transiciones_entrada[j]['frame'].grid(row=j, column=0, padx=2, pady=5, sticky="ew")
            break
    
    if not app.transiciones_entrada:
        # Añadir una entrada inicial si todas han sido eliminadas
        agregar_transicion(app)
    app.transiciones_frame.update_idletasks() # Actualizar para reflejar el cambio de tamaño

def agregar_palabra(app):
    """Añade un nuevo campo de entrada para una palabra y su label de resultado a la app."""
    frame = ctk.CTkFrame(app.palabras_frame)
    frame.grid(row=len(app.entrada_palabras), column=0, padx=2, pady=2, sticky="ew")
    
    # Configuración de las columnas dentro de cada frame de palabra
    frame.grid_columnconfigure(0, weight=1, minsize=150) # La entrada de palabra se expande, mínimo 150px
    frame.grid_columnconfigure(1, weight=0, minsize=80)  # El label de resultado no se expande, mínimo 80px
    frame.grid_columnconfigure(2, weight=0, minsize=30)  # El botón "-" no se expande, mínimo 30px

    word_entry = ctk.CTkEntry(frame, placeholder_text="palabra")
    word_entry.grid(row=0, column=0, padx=2, pady=2, sticky="ew") # sticky="ew" para expandir horizontalmente

    result_label = ctk.CTkLabel(frame, text="")
    result_label.grid(row=0, column=1, padx=5, pady=2, sticky="e") # sticky="e" para pegarlo a la derecha

    remove_button = ctk.CTkButton(frame, text="-", width=30, command=lambda f=frame: eliminar_palabra(app, f))
    remove_button.grid(row=0, column=2, padx=2, pady=2)

    app.entrada_palabras.append({'frame': frame, 'entry': word_entry, 'result_label': result_label})
    app.palabras_frame.update_idletasks()

def eliminar_palabra(app, frame_to_remove):
    """Elimina un campo de entrada de palabra y su label de resultado de la app."""
    for i, item in enumerate(app.entrada_palabras):
        if item['frame'] == frame_to_remove:
            item['frame'].destroy()
            del app.entrada_palabras[i]
            for j in range(i, len(app.entrada_palabras)):
                # Aseguramos que la reubicación use sticky="ew" para mantener la expansión
                app.entrada_palabras[j]['frame'].grid(row=j, column=0, padx=2, pady=2, sticky="ew")
            break
    
    if not app.entrada_palabras:
        # Añadir una entrada inicial si todas han sido eliminadas
        agregar_palabra(app)
    app.palabras_frame.update_idletasks() # Actualizar para reflejar el cambio de tamaño

def clear_all_transition_entries(app):
    """Elimina todas las transiciones sin agregar ninguna nueva."""
    while app.transiciones_entrada:
        item = app.transiciones_entrada[0]
        item['frame'].destroy()
        del app.transiciones_entrada[0]
    app.transiciones_frame.update_idletasks()
