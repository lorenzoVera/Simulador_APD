# apd_simulator.py

def simular_palabra(palabra, transiciones, estado_inicial, tipo_aceptacion, estados_finales):
    """
    Simula el APD para una única palabra.
    Retorna True si la palabra es aceptada, False en caso contrario.
    """
    
    estado_actual_sim = estado_inicial
    # El símbolo de fondo de la pila es 'R'
    stack_sim = ['R'] 
    
    puntero_lectura = 0
    
    # Conjunto para detectar bucles infinitos de transiciones épsilon
    visitados_epsilon = set() 
    
    max_epsilon_steps_at_pos = 100 
    pasos_epsilon_actual_pos = 0 

    print(f"\n--- Iniciando simulación para '{palabra}' ---")
    print(f"Estado inicial: {estado_inicial}, Pila inicial: {stack_sim} (R es el símbolo de fondo)")

    while True:
        simbolo_actual_entrada = palabra[puntero_lectura] if puntero_lectura < len(palabra) else ''
        tope_stack_sim = stack_sim[-1] if stack_sim else '' 
        
        print(f"\n--- Paso: Puntero={puntero_lectura}, Símbolo='{simbolo_actual_entrada}', Estado='{estado_actual_sim}', Stack={stack_sim}, Tope='{tope_stack_sim}' ---")

        transicion_encontrada = False
        estado_siguiente_trans = None
        simbolos_a_apilar_trans = None
        consumio_entrada = False

        # 1. Intentar encontrar una transición que consuma un símbolo de entrada
        clave_con_simbolo = (estado_actual_sim, simbolo_actual_entrada, tope_stack_sim)
        
        if simbolo_actual_entrada != '' and clave_con_simbolo in transiciones:
            estado_siguiente_trans, simbolos_a_apilar_trans = transiciones[clave_con_simbolo]
            consumio_entrada = True
            transicion_encontrada = True
            
            pasos_epsilon_actual_pos = 0 
            visitados_epsilon.clear() 
        else:
            # 2. Si no, intentar encontrar una transición épsilon
            clave_epsilon = (estado_actual_sim, '', tope_stack_sim)
            
            if clave_epsilon in transiciones:
                configuracion_actual = (estado_actual_sim, tuple(stack_sim), puntero_lectura)
                if configuracion_actual in visitados_epsilon:
                    print(f"DEBUG: Bucle épsilon detectado en {configuracion_actual}. Terminando simulación.")
                    break
                
                visitados_epsilon.add(configuracion_actual)
                
                estado_siguiente_trans, simbolos_a_apilar_trans = transiciones[clave_epsilon]
                consumio_entrada = False
                transicion_encontrada = True
                
                pasos_epsilon_actual_pos += 1
                if pasos_epsilon_actual_pos > max_epsilon_steps_at_pos:
                    print(f"DEBUG: Límite de transiciones épsilon consecutivas alcanzado ({max_epsilon_steps_at_pos}). Rechazando.")
                    return False
            
        if transicion_encontrada:
            estado_actual_sim = estado_siguiente_trans
            
            if stack_sim:
                stack_sim.pop()
            else:
                print("DEBUG: Error! Stack vacío antes de Pop de R. No debería ocurrir.")
                return False 
            
            # Empujar los nuevos símbolos (excepto si es ε)
            if simbolos_a_apilar_trans != '':
                for simbolo in reversed(simbolos_a_apilar_trans):
                    stack_sim.append(simbolo)

            if consumio_entrada:
                puntero_lectura += 1
            
        else:
            print(f"DEBUG: No se encontró transición para ({estado_actual_sim}, '{simbolo_actual_entrada}', '{tope_stack_sim}'). Terminando simulación.")
            break
            
    print(f"\n--- Fin de Simulación ---")
    print(f"Palabra completamente consumida: {puntero_lectura == len(palabra)}")
    print(f"Estado final alcanzado: {estado_actual_sim}")
    print(f"Stack final: {stack_sim} (R es el símbolo de fondo)")

    if puntero_lectura == len(palabra): 
        if tipo_aceptacion == 'stack':
            if not stack_sim or (len(stack_sim) == 1 and stack_sim[0] == 'R'):
                print("DEBUG: Aceptado por stack vacío/fondo (contiene solo R).")
                return True
        elif tipo_aceptacion == 'final' and estado_actual_sim in estados_finales:
            print("DEBUG: Aceptado por estado final.")
            return True
            
    print("DEBUG: Rechazada por no cumplir las condiciones de aceptación.")
    return False
