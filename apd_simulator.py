# apd_simulator.py

def simular_palabra(palabra, transiciones, estado_inicial, tipo_aceptacion, estados_finales):
    """
    Simula el APD para una única palabra.
    Retorna True si la palabra es aceptada, False en caso contrario.
    """
    estado_actual_sim = estado_inicial
    stack_sim = ['Z0'] # Símbolo de fondo del stack, ajustar si no se usa
    puntero_lectura = 0
    
    if not stack_sim:
        stack_sim.append('Z0')

    pasos_simulacion = 0
    max_pasos = len(palabra) * 200 + 100 

    while True:
        pasos_simulacion += 1
        if pasos_simulacion > max_pasos:
            # Límite de pasos para evitar bucles infinitos en APDs no deterministas
            # o si el APD no está bien diseñado para la entrada.
            return False 

        simbolo_actual_entrada = palabra[puntero_lectura] if puntero_lectura < len(palabra) else '' 
        tope_stack_sim = stack_sim[-1] if stack_sim else '' 

        transicion_encontrada = False
        estado_siguiente_trans = None
        simbolos_a_apilar_trans = None
        consumio_entrada = False

        # Intenta encontrar una transición que consuma un símbolo de entrada
        clave_busqueda_con_simbolo = (estado_actual_sim, simbolo_actual_entrada, tope_stack_sim)
        if clave_busqueda_con_simbolo in transiciones:
            estado_siguiente_trans, simbolos_a_apilar_trans = transiciones[clave_busqueda_con_simbolo]
            consumio_entrada = True
            transicion_encontrada = True
        else:
            # Si no, intenta encontrar una transición epsilon
            if simbolo_actual_entrada != '' or (simbolo_actual_entrada == '' and puntero_lectura == len(palabra)): # Permite epsilon en fin de cadena
                clave_busqueda_epsilon = (estado_actual_sim, '', tope_stack_sim) 
                if clave_busqueda_epsilon in transiciones:
                    estado_siguiente_trans, simbolos_a_apilar_trans = transiciones[clave_busqueda_epsilon]
                    consumio_entrada = False
                    transicion_encontrada = True
            
        if transicion_encontrada:
            estado_actual_sim = estado_siguiente_trans
            
            # Pop del tope de la pila
            if stack_sim:
                stack_sim.pop()
            
            # Push de los nuevos símbolos (si no es epsilon)
            if simbolos_a_apilar_trans != '': 
                for simbolo in reversed(simbolos_a_apilar_trans):
                    stack_sim.append(simbolo)

            if consumio_entrada:
                puntero_lectura += 1
            
            # Condición de parada para evitar bucles infinitos de transiciones epsilon
            # Si se llega al final de la palabra y no se consumió entrada, y no hay más transiciones epsilon disponibles,
            # se rompe el bucle para evaluar la aceptación.
            if not consumio_entrada and puntero_lectura == len(palabra) and not transiciones.get((estado_actual_sim, '', stack_sim[-1] if stack_sim else ''), False):
                break 
            
        else: # No se encontró ninguna transición válida
            break

    # Evaluar aceptación al finalizar la simulación
    if puntero_lectura == len(palabra): # Se ha leído toda la palabra de entrada
        if tipo_aceptacion == 'stack' and (not stack_sim or (len(stack_sim) == 1 and stack_sim[0] == 'Z0')): # Stack vacío o solo el símbolo de fondo
            return True
        elif tipo_aceptacion == 'final' and estado_actual_sim in estados_finales: # Estado final alcanzado
            return True
    return False