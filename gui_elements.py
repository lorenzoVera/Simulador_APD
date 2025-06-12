# gui_elements.py
import customtkinter as ctk

def add_transition_entry_to_app(app):
    """Añade un nuevo conjunto de campos de entrada para una transición a la app."""
    frame = ctk.CTkFrame(app.transitions_scroll_frame)
    frame.grid(row=len(app.transition_entries), column=0, padx=2, pady=5, sticky="ew")
    
    # Configuración de las columnas dentro de cada frame de transición
    frame.grid_columnconfigure(0, weight=1, minsize=80)  # Estado Actual
    frame.grid_columnconfigure(1, weight=1, minsize=80)  # Símbolo de Entrada
    frame.grid_columnconfigure(2, weight=1, minsize=80)  # Tope de la Pila
    frame.grid_columnconfigure(3, weight=0, minsize=20)  # "->" (fijo, pequeño)
    frame.grid_columnconfigure(4, weight=1, minsize=80)  # Estado Siguiente
    frame.grid_columnconfigure(5, weight=1, minsize=80)  # Símbolos a Apilar
    frame.grid_columnconfigure(6, weight=0, minsize=30)  # Botón eliminar (fijo)

    # Estado Actual
    ctk.CTkLabel(frame, text="Estado:").grid(row=0, column=0, sticky="w")
    e_actual = ctk.CTkEntry(frame) 
    e_actual.grid(row=1, column=0, padx=2, sticky="ew")

    # Símbolo de Entrada
    ctk.CTkLabel(frame, text="Palabra (ε si vacío):").grid(row=0, column=1, sticky="w")
    e_entrada = ctk.CTkEntry(frame, placeholder_text="ε")
    e_entrada.grid(row=1, column=1, padx=2, sticky="ew")

    # Tope de la Pila
    ctk.CTkLabel(frame, text="Tope Pila (ε si vacío, R para fondo):").grid(row=0, column=2, sticky="w")
    e_tope = ctk.CTkEntry(frame, placeholder_text="ε")
    e_tope.grid(row=1, column=2, padx=2, sticky="ew")

    ctk.CTkLabel(frame, text="->").grid(row=1, column=3, padx=5)

    # Estado Siguiente
    ctk.CTkLabel(frame, text="Estado Siguiente:").grid(row=0, column=4, sticky="w")
    e_siguiente = ctk.CTkEntry(frame)
    e_siguiente.grid(row=1, column=4, padx=2, sticky="ew")

    # Símbolos a Apilar
    ctk.CTkLabel(frame, text="Nuevo Tope Pila (ε si vacío, R para fondo):").grid(row=0, column=5, sticky="w")
    e_apilar = ctk.CTkEntry(frame, placeholder_text="ε")
    e_apilar.grid(row=1, column=5, padx=2, sticky="ew")
    
    # Botón para eliminar esta transición
    remove_button = ctk.CTkButton(frame, text="-", width=30, command=lambda f=frame: remove_transition_entry_from_app(app, f))
    remove_button.grid(row=1, column=6, padx=2)

    app.transition_entries.append({
        'frame': frame,
        'estado_actual': e_actual,
        'simbolo_entrada': e_entrada,
        'tope_stack': e_tope,
        'estado_siguiente': e_siguiente,
        'simbolos_a_apilar': e_apilar
    })
    app.transitions_scroll_frame.update_idletasks()

def remove_transition_entry_from_app(app, frame_to_remove):
    """Elimina un conjunto de campos de entrada de transición de la app."""
    for i, item in enumerate(app.transition_entries):
        if item['frame'] == frame_to_remove:
            item['frame'].destroy()
            del app.transition_entries[i]
            for j in range(i, len(app.transition_entries)):
                # Aseguramos que la reubicación use sticky="ew" para mantener la expansión
                app.transition_entries[j]['frame'].grid(row=j, column=0, padx=2, pady=5, sticky="ew")
            break
    
    if not app.transition_entries:
        # Añadir una entrada inicial si todas han sido eliminadas
        add_transition_entry_to_app(app)
    app.transitions_scroll_frame.update_idletasks() # Actualizar para reflejar el cambio de tamaño

def add_word_entry_to_app(app):
    """Añade un nuevo campo de entrada para una palabra y su label de resultado a la app."""
    frame = ctk.CTkFrame(app.words_scroll_frame)
    frame.grid(row=len(app.word_entries), column=0, padx=2, pady=2, sticky="ew")
    
    # Configuración de las columnas dentro de cada frame de palabra
    frame.grid_columnconfigure(0, weight=1, minsize=150) # La entrada de palabra se expande, mínimo 150px
    frame.grid_columnconfigure(1, weight=0, minsize=80)  # El label de resultado no se expande, mínimo 80px
    frame.grid_columnconfigure(2, weight=0, minsize=30)  # El botón "-" no se expande, mínimo 30px

    word_entry = ctk.CTkEntry(frame, placeholder_text="palabra")
    word_entry.grid(row=0, column=0, padx=2, pady=2, sticky="ew") # sticky="ew" para expandir horizontalmente

    result_label = ctk.CTkLabel(frame, text="")
    result_label.grid(row=0, column=1, padx=5, pady=2, sticky="e") # sticky="e" para pegarlo a la derecha

    remove_button = ctk.CTkButton(frame, text="-", width=30, command=lambda f=frame: remove_word_entry_from_app(app, f))
    remove_button.grid(row=0, column=2, padx=2, pady=2)

    app.word_entries.append({'frame': frame, 'entry': word_entry, 'result_label': result_label})
    app.words_scroll_frame.update_idletasks()

def remove_word_entry_from_app(app, frame_to_remove):
    """Elimina un campo de entrada de palabra y su label de resultado de la app."""
    for i, item in enumerate(app.word_entries):
        if item['frame'] == frame_to_remove:
            item['frame'].destroy()
            del app.word_entries[i]
            for j in range(i, len(app.word_entries)):
                # Aseguramos que la reubicación use sticky="ew" para mantener la expansión
                app.word_entries[j]['frame'].grid(row=j, column=0, padx=2, pady=2, sticky="ew")
            break
    
    if not app.word_entries:
        # Añadir una entrada inicial si todas han sido eliminadas
        add_word_entry_to_app(app)
    app.words_scroll_frame.update_idletasks() # Actualizar para reflejar el cambio de tamaño
