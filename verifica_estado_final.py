import tkinter.messagebox as messagebox # Importamos messagebox para los cuadros de diálogo

def verificar_estado_final(transiciones, estados_finales):
    """
    Verifica si existe al menos una transición en el APD que lleva
    a uno de los estados finales. Muestra un messagebox con el resultado.
    """
    encontrado = False
    for (estado_origen, simbolo_entrada, tope_pila), (estado_destino, simbolos_apilar) in transiciones.items():
        if estado_destino in estados_finales:
            encontrado = True
            break 

    if not encontrado:
        messagebox.showwarning("Advertencia APD", "¡ADVERTENCIA! No se encontró ninguna transición que lleve a un estado final.\nEste APD podría no aceptar ninguna palabra")