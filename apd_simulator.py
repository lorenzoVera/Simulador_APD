# apd_simulator.py

def simular_palabra(palabra, transiciones, estado_inicial, tipo_aceptacion, estados_finales):
    """
    Simula el APD para una única palabra.
    Retorna True si la palabra es aceptada, False en caso contrario.
    """
    
    estado_actual_sim = estado_inicial
    # IMPORTANTE: Inicializar la pila con el símbolo de fondo correcto.
    # En tu caso, es 'R'.
    stack_sim = ['R'] 
    
    puntero_lectura = 0
    
    # Conjunto para detectar bucles infinitos de transiciones épsilon.
    # Almacena (estado, tupla_pila, puntero_lectura).
    visitados_epsilon = set() 
    
    # Límite de transiciones épsilon consecutivas en una misma posición de entrada.
    # Ayuda a prevenir bucles infinitos en APDs mal diseñados.
    max_epsilon_steps_at_pos = 100 
    pasos_epsilon_actual_pos = 0 

    print(f"\n--- Iniciando simulación para '{palabra}' ---")
    print(f"Estado inicial: {estado_inicial}, Pila inicial: {stack_sim}")

    while True:
        simbolo_actual_entrada = palabra[puntero_lectura] if puntero_lectura < len(palabra) else ''
        # Obtener el tope de la pila. Si la pila está vacía (no debería ocurrir con 'R'/'Z0'), devuelve una cadena vacía.
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
            
            # Si se consume entrada, reiniciamos el contador de pasos épsilon y el set de visitados
            pasos_epsilon_actual_pos = 0 
            visitados_epsilon.clear() 
        else:
            # 2. Si no, intentar encontrar una transición épsilon
            clave_epsilon = (estado_actual_sim, '', tope_stack_sim)
            
            if clave_epsilon in transiciones:
                # Detección de bucles épsilon: si llegamos a la misma configuración
                # (estado, estado_pila_actual, puntero_lectura) por una transición épsilon,
                # estamos en un bucle infinito de épsilon.
                configuracion_actual = (estado_actual_sim, tuple(stack_sim), puntero_lectura)
                if configuracion_actual in visitados_epsilon:
                    print(f"DEBUG: Bucle épsilon detectado en {configuracion_actual}. Terminando simulación.")
                    break # Detener la simulación para evitar bucle infinito
                
                visitados_epsilon.add(configuracion_actual)
                
                estado_siguiente_trans, simbolos_a_apilar_trans = transiciones[clave_epsilon]
                consumio_entrada = False # Las transiciones épsilon NO consumen entrada
                transicion_encontrada = True
                
                pasos_epsilon_actual_pos += 1
                if pasos_epsilon_actual_pos > max_epsilon_steps_at_pos:
                    print(f"DEBUG: Límite de transiciones épsilon consecutivas alcanzado ({max_epsilon_steps_at_pos}). Rechazando.")
                    return False # Demasiadas épsilon seguidas, posiblemente bucle
            
        # --- Aplicar la transición encontrada ---
        if transicion_encontrada:
            estado_actual_sim = estado_siguiente_trans
            
            # La regla de los APD es siempre hacer pop del tope de la pila.
            if stack_sim:
                stack_sim.pop()
            else:
                # Esto es una condición de error grave si el stack está vacío antes de 'R'.
                print("DEBUG: Error! Stack vacío antes de Pop de R. No debería ocurrir.")
                return False 
            
            # Empujar los nuevos símbolos en orden inverso para que el primero quede en el tope.
            for simbolo in reversed(simbolos_a_apilar_trans):
                stack_sim.append(simbolo)

            if consumio_entrada:
                puntero_lectura += 1
            
        else: # No se encontró ninguna transición válida (ni con símbolo, ni épsilon)
            print(f"DEBUG: No se encontró transición para ({estado_actual_sim}, '{simbolo_actual_entrada}', '{tope_stack_sim}'). Terminando simulación.")
            break # La simulación no puede continuar
            
    # --- Evaluación de la Aceptación al finalizar la simulación ---
    print(f"\n--- Fin de Simulación ---")
    print(f"Palabra completamente consumida: {puntero_lectura == len(palabra)}")
    print(f"Estado final alcanzado: {estado_actual_sim}")
    print(f"Stack final: {stack_sim}")

    # La palabra debe haberse consumido completamente.
    if puntero_lectura == len(palabra): 
        # Aceptación por stack vacío (o con solo el símbolo de fondo)
        if tipo_aceptacion == 'stack':
            # Acepta si la pila está vacía O solo contiene el símbolo de fondo ('R').
            if not stack_sim or (len(stack_sim) == 1 and stack_sim[0] == 'R'):
                print("DEBUG: Aceptado por stack vacío/fondo.")
                return True
        # Aceptación por estado final
        elif tipo_aceptacion == 'final' and estado_actual_sim in estados_finales:
            print("DEBUG: Aceptado por estado final.")
            return True
            
    print("DEBUG: Rechazada por no cumplir las condiciones de aceptación.")
    return False 

# --- PRUEBAS ---
if __name__ == "__main__":
    # Transiciones del APD para a^n b^2n (n >= 1), usando R y A
    transiciones_an_b2n_final = {
        ('q0', 'a', 'R'): ('q0', 'AAR'),
        ('q0', 'a', 'A'): ('q0', 'AAA'), # Esta es la regla clave
        ('q0', 'b', 'A'): ('q1', ''),
        ('q1', 'b', 'A'): ('q1', ''),
        ('q1', '', 'R'): ('q2', 'R')
    }

    estado_inicial_apd = 'q0'
    tipo_aceptacion_apd = 'final'
    estados_finales_apd = {'q2'}

    print("\n--- EJECUTANDO PRUEBAS ---")

    test_cases = {
        "ab": True,          # a^1 b^2 = ab -> AAR (pop R, push AAR) -> q0, [A,A,R], ab
                             #             -> b (q0,b,A) -> q1, [A,R], b
                             #             -> b (q1,b,A) -> q1, [R], ''
                             #             -> epsilon (q1,'',R) -> q2, [R], '' (ACEPTADA)
        "aabbbb": True,      # a^2 b^4 (ACEPTADA)
        "aaabbbbbb": True,   # a^3 b^6 (ACEPTADA)
        "a": False,          # Faltan b's
        "b": False,          # Faltan a's
        "aab": False,        # Faltan b's
        "abbb": False,       # Sobran b's
        "": False            # n >= 1
    }

    for word, expected in test_cases.items():
        result = simular_palabra(word, transiciones_an_b2n_final, estado_inicial_apd, tipo_aceptacion_apd, estados_finales_apd)
        print(f"\nPalabra '{word}': {'ACEPTADA' if result else 'RECHAZADA'} (Esperado: {'ACEPTADA' if expected else 'RECHAZADA'})")
        if result != expected:
            print(f"!!! DISCREPANCIA: '{word}' -> Esperado {expected}, Obtenido {result} !!!")
