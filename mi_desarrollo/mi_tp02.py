# =====================================================================
#  TP02 - Programacion I
#  Controlador de misiones
#
#  ESTE ES EL ARCHIVO DONDE ESCRIBIS TU PROGRAMA.
#
#  Antes de ejecutarlo:
#    1. Abri INICIAR_SIMULADOR (elegi G1 o Go2)
#    2. Espera a que aparezca la ventana con el robot
#    3. Recien ahi ejecuta este archivo
#
#  Nombre y apellido:  .....................................
#  Comision:           .....................................
# =====================================================================

from robot import ErrorDeSeguridad, Robot

from misiones import MISION_BASICA, MISION_CON_ERRORES, MISION_CUADRADO


# =====================================================================
#  PARTE 1 - Validar un comando
# =====================================================================
def comando_es_valido(comando):
    """Decide si un comando se puede ejecutar. Devuelve True o False.

    Un comando es una tupla. El primer elemento dice que hacer:

        ("avanzar", velocidad, tiempo)    velocidad en m/s, tiempo en s
        ("girar", velocidad, tiempo)      velocidad en rad/s, tiempo en s
        ("detenerse",)
        ("saludar",)

    Cosas que conviene revisar:
      - que la tupla no este vacia
      - que el nombre del comando sea uno de los cuatro validos
      - que tenga la cantidad de datos que corresponde
        (avanzar y girar llevan dos; detenerse y saludar, ninguno)
      - que velocidad y tiempo sean numeros de verdad, no textos
      - que el tiempo no sea negativo
    """
    # TU CODIGO ACA
    
    
def comando_es_valido(comando):
    if not isinstance(comando, tuple) or len(comando) == 0:
        return False

    accion = comando[0]

    if accion == "avanzar" or accion == "girar":
        if len(comando) != 3:
            return False

        velocidad = comando[1]
        tiempo = comando[2]

        if isinstance(velocidad, bool) or not isinstance(velocidad, (int, float)):
            return False

        if isinstance(tiempo, bool) or not isinstance(tiempo, (int, float)):
            return False

        if tiempo < 0:
            return False

        if accion == "avanzar" and abs(velocidad) > 0.20:
            return False

        if accion == "girar" and abs(velocidad) > 0.50:
            return False

        if tiempo > 10:
            return False

        return True

    elif accion == "detenerse" or accion == "saludar":
        return len(comando) == 1

    return False




# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================
def ejecutar_comando(robot, comando):
    """Ejecuta UN comando en el robot. Devuelve un texto con lo que paso.

    Ordenes que podes usar:

        robot.avanzar(velocidad=..., tiempo=...)
        robot.girar(velocidad=..., tiempo=...)
        robot.detenerse()
        robot.saludar()

    Ojo: aunque el comando parezca valido, el robot puede rechazarlo
    igual (por ejemplo, si la velocidad supera el limite de la materia).
    Eso llega como un ErrorDeSeguridad y conviene atraparlo.
    """
    # TU CODIGO ACA
    
    if not comando_es_valido(comando):
        return "Comando rechazado: formato invalido"

    accion = comando[0]

    try:
        if accion == "avanzar":
            robot.avanzar(velocidad=comando[1], tiempo=comando[2])
        elif accion == "girar":
            robot.girar(velocidad=comando[1], tiempo=comando[2])
        elif accion == "detenerse":
            robot.detenerse()
        elif accion == "saludar":
            robot.saludar()

        return "Comando ejecutado correctamente"

    except ErrorDeSeguridad as error:
        return f"Comando rechazado por seguridad: {error}"



# =====================================================================
#  PARTE 3 - Recorrer la mision entera
# =====================================================================
def ejecutar_mision(robot, mision, historial):
    """Recorre la lista de comandos, uno por uno.

    Por cada comando:
      - si NO es valido, lo rechaza y sigue con el siguiente
      - si es valido, lo ejecuta
      - en los dos casos, guarda en 'historial' que fue lo que paso

    Un comando invalido NO tiene que cortar la mision.
    """
    # TU CODIGO ACA
    
    for comando in mision:
        resultado = ejecutar_comando(robot, comando)

        historial.append({
            "comando": comando,
            "resultado": resultado
        })



# =====================================================================
#  PARTE 4 - El reporte final
# =====================================================================
def generar_reporte(historial):
    """Muestra por pantalla un resumen de la mision.

    Tiene que decir, como minimo:
      - cuantos comandos se ejecutaron bien
      - cuantos se rechazaron
      - cual fue el motivo de cada rechazo
    """
    # TU CODIGO ACA
    
    ejecutados = 0
    rechazados = 0

    print("\n===== REPORTE DE LA MISION =====")

    for registro in historial:
        resultado = registro["resultado"]
        print(f"Comando: {registro['comando']}")
        print(f"Resultado: {resultado}")

        if resultado == "Comando ejecutado correctamente":
            ejecutados += 1
        else:
            rechazados += 1
            print(f"Motivo del rechazo: {resultado}")

        print("------------------------------")

    print(f"Comandos ejecutados correctamente: {ejecutados}")
    print(f"Comandos rechazados: {rechazados}")



# =====================================================================
#  PROGRAMA PRINCIPAL
# =====================================================================
def main():
    robot = Robot()
    robot.conectar()

    historial = []

    try:
        # Empeza probando con MISION_BASICA.
        # Cuando funcione, proba con MISION_CON_ERRORES: esa tiene
        # comandos invalidos a proposito.
        ejecutar_mision(robot, MISION_BASICA, historial)
        generar_reporte(historial)
    finally:
        robot.detenerse()
        robot.desconectar()


if __name__ == "__main__":
    main()
