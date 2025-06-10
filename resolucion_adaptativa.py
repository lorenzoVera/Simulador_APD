def obtener_geometria_adaptativa(app_instance, porcentaje_pantalla=0.80):
  
    screen_width = app_instance.winfo_screenwidth()
    screen_height = app_instance.winfo_screenheight()

    ventana_ancho = int(screen_width * porcentaje_pantalla)
    ventana_alto = int(screen_height * porcentaje_pantalla)

    pos_x = int((screen_width - ventana_ancho) / 2)
    pos_y = int((screen_height - ventana_alto) / 2)

    return f"{ventana_ancho}x{ventana_alto}+{pos_x}+{pos_y}"