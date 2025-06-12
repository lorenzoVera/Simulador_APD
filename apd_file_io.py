def cargar_apd_desde_txt(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        # Solo omite comentarios, NO líneas vacías
        lineas = [l.strip() for l in f if not l.strip().startswith("#")]
    estado_inicial = lineas[0]
    estados_finales = lineas[1]
    tipo_aceptacion = lineas[2]
    transiciones = lineas[3:]
    return estado_inicial, estados_finales, tipo_aceptacion, transiciones

def guardar_apd_a_txt(ruta, estado_inicial, estados_finales, tipo_aceptacion, transiciones):
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("# Estado inicial\n")
        f.write(f"{estado_inicial}\n")
        f.write("# Estados finales\n")
        f.write(f"{estados_finales}\n")
        f.write("# Tipo de aceptación\n")
        f.write(f"{tipo_aceptacion}\n")
        f.write("# Transiciones\n")
        for t in transiciones:
            f.write(f"{t}\n")
