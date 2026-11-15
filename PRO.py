# pgzero
import random

HEIGHT = 1136
WIDTH = 1384
TITLE = "EARTHSIGNAL"
FPS = 30

mode = "menu"

agro = Actor("agro")

# ==================================
# SISTEMA DE MISIONES AGRICOLAS
# ==================================

tareas = [
    {"tomate": 4, "fresa": 1, "lechuga": 1},
    {"tomate": 1, "fresa": 3, "lechuga": 2},
    {"tomate": 2, "fresa": 2, "lechuga": 2},
    {"tomate": 3, "fresa": 1, "lechuga": 2},
    {"tomate": 1, "fresa": 2, "lechuga": 3},
    {"tomate": 2, "fresa": 3, "lechuga": 1}
]

try:
    archivo = open("ultima_tarea.txt", "r")
    ultima_tarea = int(archivo.read())
    archivo.close()
except:
    ultima_tarea = -1

opciones = []

for i in range(len(tareas)):
    if i != ultima_tarea:
        opciones.append(i)

indice_tarea = random.choice(opciones)
tarea_actual = tareas[indice_tarea]

try:
    archivo = open("ultima_tarea.txt", "w")
    archivo.write(str(indice_tarea))
    archivo.close()
except:
    pass


# ==================================
# SISTEMA DE PUNTOS LUNARES
# ==================================

puntos_lunares = 0

DURACION_MISION = 20
tiempo_mision = DURACION_MISION

cultivos_mision = {
    "tomate": 0,
    "fresa": 0,
    "lechuga": 0
}


# ==================================
# PORTADA
# ==================================

bg = Actor("portada")
bg.pos = (WIDTH // 2, HEIGHT // 2)
bg.width = WIDTH
bg.height = HEIGHT


# ==================================
# MAPA LUNAR
# ==================================

luna = Actor("luna")
luna.pos = (WIDTH // 2, HEIGHT // 2)
luna.width = WIDTH
luna.height = HEIGHT


# ==================================
# BOTONES
# ==================================

boton = Rect((344, 670), (700, 185))
boton_kepler = Rect((950, 450), (350, 100))
boton_comunicacion = Rect((650, 330), (290, 140))
boton_volver = Rect((40, 40), (180, 65))


# ==================================
# ESTACION DE COMUNICACIONES
# ==================================

comunicacion_bg = Actor("comunicacion")
comunicacion_bg.pos = (WIDTH // 2, HEIGHT // 2)
comunicacion_bg.width = WIDTH
comunicacion_bg.height = HEIGHT


# ==================================
# POSICIONES DE LAS CELDAS
# ==================================

posiciones = [
    (350, 350), (570, 350), (790, 350), (1010, 350),
    (350, 570), (570, 570), (790, 570), (1010, 570),
    (350, 790), (570, 790), (790, 790), (1010, 790),
]


# ==================================
# PLANTAS
# ==================================

lechuga = Actor("lechuga", (1260, 350))
tomate = Actor("tomate", (1260, 570))
fresa = Actor("fresa", (1260, 790))

planta_seleccionada = None


# ==================================
# CRECIMIENTO
# ==================================

crecimiento = {

    "fresa": {
        "pequena": "pequena",
        "madura": "fresa",
        "tiempo": 6
    },

    "lechuga": {
        "pequena": "pequena",
        "madura": "lechuga",
        "tiempo": 3.3
    },

    "tomate": {
        "pequena": "pequena",
        "madura": "tomate",
        "tiempo": 9
    }
}


# ==================================
# CREAR CELDAS
# ==================================

celdas = []

for posicion in posiciones:

    celda = Actor("piedra")
    celda.pos = posicion
    celda.width = 90
    celda.height = 90

    celdas.append({
        "actor": celda,
        "creciendo": False,
        "tiempo": 0,
        "planta": None
    })


# ==================================
# SISTEMA DE MENSAJES SORPRESA
# ==================================

tiempo_sin_actividad = 0
mensaje_recibido = False
mensaje_abierto = False

mensajes_sorpresa = [
    {
        "titulo": "GREETINGS FROM EARTH!",
        "texto": "Earth sends greetings to the entire lunar crew. Keep up the great work!"
    },
    {
        "titulo": "MISSION CONTROL NOTICE",
        "texto": "Remember to check your equipment and take care of the lunar base resources."
    },
    {
        "titulo": "NEW COMMUNICATION",
        "texto": "Excellent work! The Earth station successfully received your signal."
    },
    {
        "titulo": "MESSAGE FROM EARTH",
        "texto": "Scientists on Earth are proud of your work on the Moon."
    },
    {
        "titulo": "COMMUNICATION ALERT",
        "texto": "A new signal has been detected near the base. Keep your antennas active."
    }
]

mensaje_actual = None

boton_leer = Rect((450, 650), (480, 90))
boton_cerrar_mensaje = Rect((1100, 40), (220, 65))


def reiniciar_reloj():

    global tiempo_sin_actividad
    global mensaje_recibido

    tiempo_sin_actividad = 0
    mensaje_recibido = False


def dibujar_notificacion():

    if mensaje_recibido and not mensaje_abierto:

        screen.draw.filled_rect(
            Rect((350, 25), (680, 105)),
            "#172E49"
        )

        screen.draw.rect(
            Rect((350, 25), (680, 105)),
            "#FFD43B"
        )

        screen.draw.text(
            "NEW MESSAGE FROM MISSION CONTROL!",
            center=(690, 60),
            fontsize=23,
            color="yellow"
        )

        screen.draw.text(
            "CLICK HERE TO READ",
            center=(690, 100),
            fontsize=18,
            color="white"
        )


def dibujar_mensaje():

    if mensaje_actual is None:
        return

    screen.draw.filled_rect(
        Rect((250, 300), (880, 500)),
        "#172E49"
    )

    screen.draw.rect(
        Rect((250, 300), (880, 500)),
        "#FFD43B"
    )

    screen.draw.text(
        "MESSAGE RECEIVED",
        center=(690, 370),
        fontsize=38,
        color="yellow"
    )

    screen.draw.text(
        mensaje_actual["titulo"],
        center=(690, 460),
        fontsize=30,
        color="#75D6B0"
    )

    screen.draw.text(
        mensaje_actual["texto"],
        center=(690, 550),
        fontsize=25,
        color="white",
        width=760
    )

    screen.draw.filled_rect(
        boton_cerrar_mensaje,
        "#287A91"
    )

    screen.draw.text(
        "CLOSE",
        center=boton_cerrar_mensaje.center,
        fontsize=22,
        color="white"
    )


# ==================================
# CONTAR CULTIVOS DE LA MISION
# ==================================

def contar_plantas(nombre):

    return cultivos_mision[nombre]


# ==================================
# GENERAR NUEVA MISION AGRICOLA
# ==================================

def generar_nueva_mision():

    global indice_tarea
    global tarea_actual
    global tiempo_mision
    global cultivos_mision
    global puntos_lunares
    global planta_seleccionada

    # REVISAR SI SE COMPLETO LA MISION

    completada = True

    for nombre in ["tomate", "fresa", "lechuga"]:

        if cultivos_mision[nombre] < tarea_actual[nombre]:
            completada = False

    # SUMAR O RESTAR PUNTOS LUNARES

    if completada:

        puntos_lunares += 10

    else:

        puntos_lunares = max(0, puntos_lunares - 5)

    # ELEGIR UNA NUEVA MISION ALEATORIA

    opciones_nuevas = []

    for i in range(len(tareas)):

        if i != indice_tarea:
            opciones_nuevas.append(i)

    indice_tarea = random.choice(opciones_nuevas)

    tarea_actual = tareas[indice_tarea]

    # GUARDAR LA ULTIMA MISION

    try:
        archivo = open("ultima_tarea.txt", "w")
        archivo.write(str(indice_tarea))
        archivo.close()
    except:
        pass

    # REINICIAR CONTADORES

    cultivos_mision = {
        "tomate": 0,
        "fresa": 0,
        "lechuga": 0
    }

    tiempo_mision = DURACION_MISION

    planta_seleccionada = None

    # LIMPIAR LAS CELDAS

    for celda in celdas:

        celda["actor"].image = "piedra"
        celda["creciendo"] = False
        celda["tiempo"] = 0
        celda["planta"] = None


# ==================================
# ACTUALIZAR JUEGO
# ==================================

def update(dt):

    global numero_mensaje
    global respuesta_marcada
    global respuesta_correcta
    global tiempo_espera

    global tiempo_sin_actividad
    global mensaje_recibido
    global mensaje_actual

    global tiempo_mision

    # CRECIMIENTO DE LAS PLANTAS

    for celda in celdas:

        if celda["creciendo"]:

            celda["tiempo"] -= dt

            if celda["tiempo"] <= 0:

                nombre = celda["planta"]

                celda["actor"].image = crecimiento[nombre]["madura"]

                celda["actor"].width = 90
                celda["actor"].height = 90

                celda["creciendo"] = False
                celda["tiempo"] = 0

    # TEMPORIZADOR DE MISIONES AGRICOLAS

    if mode == "kepler":

        tiempo_mision -= dt

        if tiempo_mision <= 0:

            generar_nueva_mision()

    # PASAR A LA SIGUIENTE PREGUNTA

    if mode == "comunicacion" and respuesta_marcada:

        tiempo_espera -= dt

        if tiempo_espera <= 0:

            numero_mensaje += 1
            respuesta_marcada = False
            respuesta_correcta = False

    # CONTAR LOS CINCO MINUTOS

    if not mensaje_recibido and not mensaje_abierto:

        tiempo_sin_actividad += dt

        if tiempo_sin_actividad >= 300:

            mensaje_recibido = True
            mensaje_actual = random.choice(mensajes_sorpresa)


# ==================================
# DIBUJAR MISIONES AGRICOLAS
# ==================================

def dibujar_tareas():

    screen.draw.filled_rect(
        Rect((300, 205), (800, 85)),
        "#26364B"
    )

    screen.draw.rect(
        Rect((300, 205), (800, 85)),
        "#75D6B0"
    )

    screen.draw.text(
        "AGRICULTURAL ORDER - 6 CROPS",
        center=(700, 225),
        fontsize=23,
        color="white"
    )

    cantidad_tomate = contar_plantas("tomate")
    cantidad_fresa = contar_plantas("fresa")
    cantidad_lechuga = contar_plantas("lechuga")

    color_tomate = "green"

    if cantidad_tomate < tarea_actual["tomate"]:
        color_tomate = "white"

    screen.draw.text(
        "TOMATOES: " + str(cantidad_tomate) + "/" + str(tarea_actual["tomate"]),
        center=(440, 265),
        fontsize=19,
        color=color_tomate
    )

    color_fresa = "green"

    if cantidad_fresa < tarea_actual["fresa"]:
        color_fresa = "white"

    screen.draw.text(
        "STRAWBERRIES: " + str(cantidad_fresa) + "/" + str(tarea_actual["fresa"]),
        center=(700, 265),
        fontsize=19,
        color=color_fresa
    )

    color_lechuga = "green"

    if cantidad_lechuga < tarea_actual["lechuga"]:
        color_lechuga = "white"

    screen.draw.text(
        "LETTUCES: " + str(cantidad_lechuga) + "/" + str(tarea_actual["lechuga"]),
        center=(960, 265),
        fontsize=19,
        color=color_lechuga
    )


# ==================================
# MINIJUEGO DE COMUNICACIONES
# ==================================

mensajes = [

    {
        "desorden": "OXYGEN / WE / NEED / MORE / TO / LIVE",
        "respuestas": [
            "We need more oxygen to live",
            "Oxygen live to need we more",
            "To more we need live oxygen"
        ],
        "correcta": 0
    },

    {
        "desorden": "EARTH / GREETINGS / FROM / THE / MOON",
        "respuestas": [
            "From the Moon greetings Earth",
            "Greetings from Earth and the Moon",
            "Greetings from the Moon to Earth"
        ],
        "correcta": 2
    },

    {
        "desorden": "URGENT / BASE / WE / NEED / HELP / AT / THE",
        "respuestas": [
            "We need urgent help at the base",
            "Urgent at the base we need help",
            "At help we need the base urgent"
        ],
        "correcta": 0
    },

    {
        "desorden": "STATION / EVERYTHING / IN / THE / ORDER / IS",
        "respuestas": [
            "The station everything is in order",
            "Everything is in order at the station",
            "Order in station everything is the"
        ],
        "correcta": 1
    },

    {
        "desorden": "MESSAGE / RECEIVED / SUCCESSFULLY / FROM / THE / EARTH",
        "respuestas": [
            "From Earth message successfully received",
            "Message successfully received from Earth",
            "Successfully Earth from received message the"
        ],
        "correcta": 1
    },

    {
        "desorden": "ANTENNAS / WE / MUST / CHECK / TODAY / THE",
        "respuestas": [
            "We must check the antennas today",
            "The today antennas check we must",
            "Check we must today the antennas"
        ],
        "correcta": 0
    },

    {
        "desorden": "SIGNAL / SENDING / WE / ARE / A / NEW",
        "respuestas": [
            "A new signal we are sending",
            "We are sending a new signal",
            "New we signal a sending are"
        ],
        "correcta": 1
    },

    {
        "desorden": "CREW / THE / SAFE / IS / LUNAR",
        "respuestas": [
            "The lunar crew is safe",
            "Safe is lunar crew the",
            "Lunar safe the crew is"
        ],
        "correcta": 0
    },

    {
        "desorden": "WATER / WE / NEED / FOR / THE / CROPS",
        "respuestas": [
            "We need water for the crops",
            "Water the need we crops for",
            "Need we the water for crops"
        ],
        "correcta": 0
    },

    {
        "desorden": "COMMUNICATION / KEEP / WE / MUST / ACTIVE / THE",
        "respuestas": [
            "Active we must communication keep the",
            "We must keep the communication active",
            "The active communication we must keep"
        ],
        "correcta": 1
    }

]


# ==================================
# BOTONES DE RESPUESTAS
# ==================================

opcion_1 = Rect((250, 650), (880, 85))
opcion_2 = Rect((250, 760), (880, 85))
opcion_3 = Rect((250, 870), (880, 85))

boton_siguiente = Rect((500, 990), (380, 80))


# ==================================
# VARIABLES DEL MINIJUEGO
# ==================================

numero_mensaje = 0
puntos_comunicacion = 0

respuesta_marcada = False
respuesta_correcta = False

tiempo_espera = 0


# ==================================
# DIBUJAR COMUNICACIONES
# ==================================

def dibujar_comunicacion():

    comunicacion_bg.draw()

    screen.draw.text(
        "COPERNICUS CRATER",
        center=(WIDTH // 2, 75),
        fontsize=45,
        color="white"
    )

    screen.draw.text(
        "COMMUNICATION CENTER",
        center=(WIDTH // 2, 130),
        fontsize=30,
        color="#FFD43B"
    )

    if numero_mensaje >= len(mensajes):

        screen.draw.filled_rect(
            Rect((300, 350), (780, 400)),
            "#26364B"
        )

        screen.draw.text(
            "MISSION COMPLETED!",
            center=(690, 430),
            fontsize=45,
            color="#75D6B0"
        )

        screen.draw.text(
            "YOU HAVE FINISHED ALL THE QUESTIONS!",
            center=(690, 520),
            fontsize=28,
            color="white"
        )

        screen.draw.filled_rect(
            boton_siguiente,
            "#287A91"
        )

        screen.draw.text(
            "PLAY AGAIN",
            center=boton_siguiente.center,
            fontsize=25,
            color="white"
        )

        screen.draw.filled_rect(
            boton_volver,
            "#343A50"
        )

        screen.draw.text(
            "BACK",
            center=boton_volver.center,
            fontsize=25,
            color="white"
        )

        return

    mensaje = mensajes[numero_mensaje]

    screen.draw.text(
        "MESSAGE " + str(numero_mensaje + 1) + " OF " + str(len(mensajes)),
        center=(WIDTH // 2, 220),
        fontsize=27,
        color="white"
    )

    screen.draw.text(
        "PUT THE WORDS IN ORDER!",
        center=(WIDTH // 2, 300),
        fontsize=34,
        color="#75D6B0"
    )

    screen.draw.filled_rect(
        Rect((250, 360), (880, 130)),
        "#26364B"
    )

    screen.draw.text(
        mensaje["desorden"],
        center=(690, 425),
        fontsize=27,
        color="yellow"
    )

    respuestas = mensaje["respuestas"]
    botones = [opcion_1, opcion_2, opcion_3]

    for i in range(3):

        color = "#26364B"

        if respuesta_marcada and i == mensaje["correcta"]:
            color = "#27834D"

        screen.draw.filled_rect(
            botones[i],
            color
        )

        screen.draw.rect(
            botones[i],
            "white"
        )

        screen.draw.text(
            respuestas[i],
            center=botones[i].center,
            fontsize=25,
            color="white"
        )

    if respuesta_marcada:

        if respuesta_correcta:
            texto = "GREAT JOB! CORRECT ANSWER"
            color = "#75D6B0"
        else:
            texto = "KEEP TRYING!"
            color = "#FF8C8C"

        screen.draw.text(
            texto,
            center=(WIDTH // 2, 940),
            fontsize=26,
            color=color
        )

    screen.draw.filled_rect(
        boton_volver,
        "#343A50"
    )

    screen.draw.text(
        "BACK",
        center=boton_volver.center,
        fontsize=25,
        color="white"
    )


# ==================================
# DIBUJAR PANTALLAS
# ==================================

def draw():

    screen.clear()

    if mode == "menu":

        bg.draw()

    # MAPA LUNAR

    elif mode == "jugar":

        luna.draw()

        screen.draw.text(
            "FLEET MANAGEMENT",
            center=(240, 290),
            fontsize=24,
            color="white",
            shadow=(2, 2),
            scolor="black"
        )

        screen.draw.text(
            "PLATO CRATER",
            center=(240, 320),
            fontsize=20,
            color="#36BFFF",
            shadow=(2, 2),
            scolor="black"
        )

        screen.draw.text(
            "RESEARCH &",
            center=(830, 375),
            fontsize=21,
            color="white",
            shadow=(2, 2),
            scolor="black"
        )

        screen.draw.text(
            "COMMUNICATION",
            center=(830, 400),
            fontsize=21,
            color="white",
            shadow=(2, 2),
            scolor="black"
        )

        screen.draw.text(
            "COPERNICUS CRATER",
            center=(830, 425),
            fontsize=17,
            color="#FFD43B",
            shadow=(2, 2),
            scolor="black"
        )

        screen.draw.text(
            "AGRICULTURAL STATION",
            center=(1120, 490),
            fontsize=24,
            color="white",
            shadow=(2, 2),
            scolor="black"
        )

        screen.draw.text(
            "KEPLER CRATER",
            center=(1120, 520),
            fontsize=21,
            color="#FF5C9D",
            shadow=(2, 2),
            scolor="black"
        )

        # CONTADOR DE PUNTOS LUNARES
        # SOLO APARECE EN EL MAPA LUNAR

        screen.draw.filled_rect(
            Rect((1110, 25), (245, 55)),
            "#172E49"
        )

        screen.draw.rect(
            Rect((1110, 25), (245, 55)),
            "#FFD43B"
        )

        screen.draw.text(
            "LUNAR POINTS: " + str(puntos_lunares),
            center=(1232, 52),
            fontsize=19,
            color="yellow"
        )

    # ESTACION AGRICOLA

    elif mode == "kepler":

        agro.draw()

        screen.draw.text(
            "KEPLER CRATER",
            center=(WIDTH // 2, 75),
            fontsize=48,
            color="white"
        )

        screen.draw.text(
            "AGRICULTURAL STATION",
            center=(WIDTH // 2, 125),
            fontsize=30,
            color="#FF5C9D"
        )

        screen.draw.text(
            "SELECT A PLANT AND THEN SELECT A CELL TO PLANT IT",
            center=(WIDTH // 2, 175),
            fontsize=23,
            color="#B9FFB9"
        )

        dibujar_tareas()

        # TEMPORIZADOR

        screen.draw.text(
            "NEW MISSION IN: " + str(max(0, int(tiempo_mision))) + " SEC",
            topleft=(40, 185),
            fontsize=23,
            color="white"
        )

        lechuga.draw()
        tomate.draw()
        fresa.draw()

        if planta_seleccionada == "lechuga":

            screen.draw.rect(
                Rect((lechuga.x - 48, lechuga.y - 48), (96, 96)),
                "yellow"
            )

        elif planta_seleccionada == "tomate":

            screen.draw.rect(
                Rect((tomate.x - 48, tomate.y - 48), (96, 96)),
                "yellow"
            )

        elif planta_seleccionada == "fresa":

            screen.draw.rect(
                Rect((fresa.x - 48, fresa.y - 48), (96, 96)),
                "yellow"
            )

        if planta_seleccionada is not None:

            nombres_ingles = {
                "lechuga": "LETTUCE",
                "tomate": "TOMATO",
                "fresa": "STRAWBERRY"
            }

            screen.draw.text(
                "SELECTED PLANT: " + nombres_ingles[planta_seleccionada],
                center=(1260, 900),
                fontsize=23,
                color="yellow"
            )

        for celda in celdas:
            celda["actor"].draw()

        screen.draw.filled_rect(
            boton_volver,
            "#343A50"
        )

        screen.draw.text(
            "BACK",
            center=boton_volver.center,
            fontsize=25,
            color="white"
        )

    # CENTRO DE COMUNICACIONES

    elif mode == "comunicacion":

        dibujar_comunicacion()

    # NOTIFICACION DE MENSAJE

    if mensaje_recibido and not mensaje_abierto:
        dibujar_notificacion()

    # MENSAJE ABIERTO

    if mensaje_abierto:
        dibujar_mensaje()


# ==================================
# CONTROLES DEL MOUSE
# ==================================

def on_mouse_down(pos):

    global mode, planta_seleccionada

    global numero_mensaje, puntos_comunicacion
    global puntos_lunares

    global respuesta_marcada, respuesta_correcta
    global tiempo_espera

    global mensaje_abierto, mensaje_recibido

    # ABRIR MENSAJE RECIBIDO

    if mensaje_recibido and not mensaje_abierto:

        if Rect((350, 25), (680, 105)).collidepoint(pos):

            mensaje_abierto = True
            return

    # CERRAR MENSAJE

    if mensaje_abierto:

        if boton_cerrar_mensaje.collidepoint(pos):

            mensaje_abierto = False
            mensaje_recibido = False
            reiniciar_reloj()
            return

        return

    # MENU PRINCIPAL

    if mode == "menu":

        if boton.collidepoint(pos):
            mode = "jugar"

    # MAPA LUNAR

    elif mode == "jugar":

        if boton_kepler.collidepoint(pos):

            mode = "kepler"

        elif boton_comunicacion.collidepoint(pos):

            mode = "comunicacion"

            numero_mensaje = 0
            puntos_comunicacion = 0
            respuesta_marcada = False
            respuesta_correcta = False

    # ESTACION AGRICOLA

    elif mode == "kepler":

        if boton_volver.collidepoint(pos):

            mode = "jugar"
            planta_seleccionada = None
            return

        if lechuga.collidepoint(pos):

            planta_seleccionada = "lechuga"
            return

        if tomate.collidepoint(pos):

            planta_seleccionada = "tomate"
            return

        if fresa.collidepoint(pos):

            planta_seleccionada = "fresa"
            return

        # SEMBRAR

        if planta_seleccionada is not None:

            for celda in celdas:

                if celda["actor"].collidepoint(pos):

                    if celda["planta"] is None:

                        nombre = planta_seleccionada

                        # EVITAR SEMBRAR MAS DE LO SOLICITADO

                        if cultivos_mision[nombre] < tarea_actual[nombre]:

                            celda["planta"] = nombre

                            cultivos_mision[nombre] += 1

                            celda["actor"].image = "pequena"

                            celda["actor"].width = 90
                            celda["actor"].height = 90

                            celda["creciendo"] = True
                            celda["tiempo"] = crecimiento[nombre]["tiempo"]

                            # REINICIAR RELOJ DE MENSAJES

                            reiniciar_reloj()

                    break

    # CENTRO DE COMUNICACIONES

    elif mode == "comunicacion":

        if boton_volver.collidepoint(pos):

            mode = "jugar"
            return

        # SI TERMINARON LAS PREGUNTAS

        if numero_mensaje >= len(mensajes):

            if boton_siguiente.collidepoint(pos):

                numero_mensaje = 0
                puntos_comunicacion = 0
                respuesta_marcada = False
                respuesta_correcta = False

            return

        # EVITAR DOBLE RESPUESTA

        if respuesta_marcada:
            return

        mensaje = mensajes[numero_mensaje]

        if opcion_1.collidepoint(pos):
            seleccion = 0

        elif opcion_2.collidepoint(pos):
            seleccion = 1

        elif opcion_3.collidepoint(pos):
            seleccion = 2

        else:
            return

        respuesta_marcada = True
        tiempo_espera = 0.5

        # REINICIAR RELOJ DE MENSAJES

        reiniciar_reloj()

        if seleccion == mensaje["correcta"]:

            respuesta_correcta = True

            # PUNTO PARA EL MINIJUEGO
            puntos_comunicacion += 1

            # TAMBIEN SE SUMA AL TOTAL LUNAR
            puntos_lunares += 1

        else:

            respuesta_correcta = False
