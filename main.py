#INSTITUTO TECNOLÓGICO DE COSTA RICA
#Proyecto defensa y asalto de base
#Fabián Cambronero Núñez  Carné: 2026079420
#Alejandro Campos Lopez Carne: 2026090719

#-------
#IMPORTS
#-------
import tkinter as tk
import json
import os


#-----------------------
#Archivos de usuarios---
#-----------------------

RUTA_PROYECTO = os.path.dirname(os.path.abspath(__file__))
CARPETA_DATOS =os.path.join(RUTA_PROYECTO,'datos')
ARCHIVO_USUARIOS = os.path.join(CARPETA_DATOS,'usuarios.json')


#Funcion para crear el archivo usuarios.json si no existe
#E: nada
#S: crea la carpeta datos y el archivo usuarios.json

def crear_archivo_usuarios():
    if not os.path.exists(CARPETA_DATOS):
        os.makedirs(CARPETA_DATOS) #si no existe la carpeta datos la crea

    if not os.path.exists(ARCHIVO_USUARIOS):
        with open(ARCHIVO_USUARIOS,'w', encoding = 'utf-8') as archivo: # igual si no existe el json lo crea y lo deja con todo listo
            json.dump({}, archivo, indent=4, ensure_ascii=False)

# -------------------------
# Clase Jugador - cada jugador va aqui 
# -------------------------
class Jugador:
    '''
    atributos --> nombre_usuario, contrasena, victorias_defensor, victorias_atacante
    metodos --> convertir_a_diccionario, sumar_victoria
    '''
    def __init__(self, nombre_usuario, contrasena, victorias_defensor=0, victorias_atacante=0):
        self.nombre_usuario = nombre_usuario
        self.contrasena = contrasena
        self.victorias_defensor = victorias_defensor
        self.victorias_atacante = victorias_atacante

    # metodo para convertir el objeto Jugador en un diccionario.
    def convertir_a_diccionario(self): #todos los objetos se guardan en el json
        return {
            "contrasena": self.contrasena,
            "victorias_defensor": self.victorias_defensor,
            "victorias_atacante": self.victorias_atacante
        }

    # metodo para sumar una victoria según el rol utilizado.
    def sumar_victoria(self, rol):
        if rol == "defensor":
            self.victorias_defensor += 1

        elif rol == "atacante":
            self.victorias_atacante += 1

# -------------------------
# Funciones para manejar usuarios
# -------------------------

# Función para cargar los usuarios guardados en el archivo usuarios.json.
# Entradas: ninguna.
# Salidas: un diccionario con los usuarios cargados como objetos Jugador.
def cargar_usuarios():

    # Se asegura que el archivo exista antes de intentar leerlo.
    crear_archivo_usuarios()

    # Se abre el archivo en modo lectura.
    with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as archivo:
        try:
            datos = json.load(archivo)

        # Si el archivo está vacío o tiene un error, se usa un diccionario vacío.
        except json.JSONDecodeError:
            datos = {}

    # Diccionario donde se guardarán los usuarios como objetos Jugador.
    usuarios = {}

    # Se recorre cada usuario guardado en el archivo.
    for nombre_usuario in datos:

        # Se obtiene la información del usuario actual.
        informacion = datos[nombre_usuario]

        # Se crea un objeto Jugador con la información guardada.
        jugador = Jugador(
            nombre_usuario,
            informacion.get("contrasena", ""),
            informacion.get("victorias_defensor", 0),
            informacion.get("victorias_atacante", 0)
        )

        # Se guarda el jugador en el diccionario de usuarios.
        usuarios[nombre_usuario] = jugador

    # Se retorna el diccionario con todos los usuarios cargados.
    return usuarios


# Función para guardar los usuarios en el archivo usuarios.json.
# Entradas: diccionario de usuarios.
# Salidas: ninguna, guarda la información en el archivo.
def guardar_usuarios(usuarios):

    # Diccionario donde se guardará la información lista para escribir en JSON.
    datos = {}

    # Se recorre cada usuario del diccionario.
    for nombre_usuario in usuarios:

        # Se obtiene el objeto Jugador.
        jugador = usuarios[nombre_usuario]

        # Se convierte el objeto Jugador en un diccionario.
        datos[nombre_usuario] = jugador.convertir_a_diccionario()

    # Se abre el archivo en modo escritura y se guarda la información actualizada.
    with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


# Función para registrar un nuevo usuario.
# Entradas: nombre_usuario, contrasena 
# Salidas: True o False, además de un mensaje explicativo.
def registrar_usuario(nombre_usuario, contrasena):

    # Se eliminan espacios innecesarios al inicio o final.
    nombre_usuario = nombre_usuario.strip()
    contrasena = contrasena.strip()

    # Se valida que el usuario no esté vacío.
    if nombre_usuario == "":
        return False, "Debe ingresar un nombre de usuario."

    # Se valida que la contraseña no esté vacía.
    if contrasena == "":
        return False, "Debe ingresar una contraseña."

    # Se cargan los usuarios existentes.
    usuarios = cargar_usuarios()

    # Se revisa si el usuario ya existe.
    if nombre_usuario in usuarios:
        return False, "Ese nombre de usuario ya existe."

    # Se crea un nuevo jugador con cero victorias.
    nuevo_jugador = Jugador(nombre_usuario, contrasena)

    # Se agrega al diccionario de usuarios.
    usuarios[nombre_usuario] = nuevo_jugador

    # Se guarda la información actualizada en el archivo.
    guardar_usuarios(usuarios)

    return True, "Usuario registrado correctamente."


# Función para validar el inicio de sesión de un usuario.
# Entradas: nombre_usuario, contrasena 
# Salidas: True o False, el objeto Jugador si existe, y un mensaje.
def validar_login(nombre_usuario, contrasena):

    nombre_usuario = nombre_usuario.strip()
    contrasena = contrasena.strip()

    if nombre_usuario == "":
        return False, None, "Debe ingresar un nombre de usuario."

    if contrasena == "":
        return False, None, "Debe ingresar una contraseña."

    usuarios = cargar_usuarios()

    if nombre_usuario not in usuarios:
        return False, None, "El usuario no existe."

    jugador = usuarios[nombre_usuario]

    if jugador.contrasena != contrasena:
        return False, None, "La contraseña es incorrecta."

    return True, jugador, "Inicio de sesión correcto."







#----------------------------------------------------------
# MAPA, ENTIDADES, FACCIONES Y COMBATE
#-----------------------------------------------------------

# -------------------------
# Constantes generales
# -------------------------

TAMANIO_MAPA = 10
POSICION_BASE = (5, 5)

DINERO_INICIAL_DEFENSOR = 300
DINERO_INICIAL_ATACANTE = 300

LIMITE_TURNOS_COMBATE = 30

BONO_DINERO_POR_RONDA = 50
RONDAS_PARA_GANAR = 3
# -------------------------
# Clases base del juego
# -------------------------

#Clase Facción
class Faccion:
    def __init__(self, nombre, color_torre, color_muro, color_unidad, color_base):
        self.nombre = nombre
        self.color_torre = color_torre
        self.color_muro = color_muro
        self.color_unidad = color_unidad
        self.color_base = color_base

#Clase Torre
class Torre:
    def __init__(self, nombre, costo, vida, danio, alcance, habilidad, turnos_habilidad):
        self.nombre = nombre
        self.costo = costo
        self.vida = vida
        self.danio = danio
        self.alcance = alcance
        self.habilidad = habilidad
        self.turnos_habilidad = turnos_habilidad

    def esta_viva(self):
        return self.vida > 0

    def recibir_danio(self, cantidad):
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0

#Clase Unidad
class Unidad:
    def __init__(self, nombre, costo, vida, danio, velocidad, habilidad, turnos_habilidad):
        self.nombre = nombre
        self.costo = costo
        self.vida = vida
        self.danio = danio
        self.velocidad = velocidad
        self.habilidad = habilidad
        self.turnos_habilidad = turnos_habilidad

    def esta_viva(self):
        return self.vida > 0

    def recibir_danio(self, cantidad):
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0

#Clase Muro
class Muro:
    def __init__(self, costo=30, vida=80):
        self.nombre = "Muro"
        self.costo = costo
        self.vida = vida

    def esta_vivo(self):
        return self.vida > 0

    def recibir_danio(self, cantidad):
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0

#Clase BaseCentral
class BaseCentral:
    def __init__(self, vida=500):
        self.nombre = "Base Central"
        self.vida = vida

    def esta_viva(self):
        return self.vida > 0

    def recibir_danio(self, cantidad):
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0


# -------------------------
# Facciones 
# -------------------------

FACCIONES = {
    "Medieval": Faccion(
        nombre="Medieval",
        color_torre="#8B4513",    # Marrón
        color_muro="#808080",     # Gris
        color_unidad="#B22222",   # Rojo oscuro
        color_base="#DAA520"      # Dorado
    ),

    "Futurista": Faccion(
        nombre="Futurista",
        color_torre="#00CED1",    # Turquesa
        color_muro="#4682B4",     # Azul metálico
        color_unidad="#9370DB",   # Morado claro
        color_base="#C0C0C0"      # Plateado
    ),

    "Oscura": Faccion(
        nombre="Oscura",
        color_torre="#4B0082",    # Índigo
        color_muro="#2F2F2F",     # Gris oscuro
        color_unidad="#111111",   # Casi negro
        color_base="#8B0000"      # Rojo oscuro
    )
}

# Facciones temporales para probar la parte jugable.
# Luego estas variables se conectarán con la pantalla de selección.
faccion_defensor_actual = FACCIONES["Medieval"]
faccion_atacante_actual = FACCIONES["Oscura"]

# Función para validar que las facciones sean diferentes
# Entradas: facción del defensor y facción del atacante
# Salidas: True si son diferentes, False si son iguales
def validar_facciones(faccion_defensor, faccion_atacante):
    
    return faccion_defensor.nombre != faccion_atacante.nombre

#Busca facción por nombre para verificar que exista 
#Entradas: Nombre en string
#Salida: None o return del nombre si existe 
def obtener_faccion(nombre_faccion):
    return FACCIONES.get(nombre_faccion)

# ----------------------------
# Catálogo de torres y unidades
# ----------------------------

DATOS_TORRES = {
    "Basica": {
        "nombre": "Torre Básica",
        "costo": 50,
        "vida": 100,
        "danio": 25,
        "alcance": 2,
        "habilidad": "Disparo doble",
        "turnos_habilidad": 3
    },

    "Pesada": {
        "nombre": "Torre Pesada",
        "costo": 90,
        "vida": 180,
        "danio": 40,
        "alcance": 2,
        "habilidad": "Aumentar daño",
        "turnos_habilidad": 4
    },

    "Magica": {
        "nombre": "Torre Mágica",
        "costo": 75,
        "vida": 80,
        "danio": 20,
        "alcance": 3,
        "habilidad": "Congelar unidad",
        "turnos_habilidad": 3
    }
}


DATOS_UNIDADES = {
    "Soldado": {
        "nombre": "Soldado",
        "costo": 40,
        "vida": 80,
        "danio": 20,
        "velocidad": 1,
        "habilidad": "Ataque doble",
        "turnos_habilidad": 3
    },

    "Tanque": {
        "nombre": "Tanque",
        "costo": 90,
        "vida": 180,
        "danio": 35,
        "velocidad": 1,
        "habilidad": "Escudo temporal",
        "turnos_habilidad": 4
    },

    "Rapida": {
        "nombre": "Unidad Rápida",
        "costo": 60,
        "vida": 60,
        "danio": 15,
        "velocidad": 2,
        "habilidad": "Aumento de velocidad",
        "turnos_habilidad": 3
    }
}


# Función para crear una torre nueva según el tipo seleccionado
# Entradas: tipo de torre
# Salidas: objeto Torre nuevo o None si el tipo no existe
def crear_torre(tipo_torre):
    datos = DATOS_TORRES.get(tipo_torre)

    if datos is None:
        return None

    return Torre(
        nombre=datos["nombre"],
        costo=datos["costo"],
        vida=datos["vida"],
        danio=datos["danio"],
        alcance=datos["alcance"],
        habilidad=datos["habilidad"],
        turnos_habilidad=datos["turnos_habilidad"]
    )


# Función para crear una unidad nueva según el tipo seleccionado
# Entradas: tipo de unidad
# Salidas: objeto Unidad nuevo o None si el tipo no existe
def crear_unidad(tipo_unidad):
    datos = DATOS_UNIDADES.get(tipo_unidad)

    if datos is None:
        return None

    return Unidad(
        nombre=datos["nombre"],
        costo=datos["costo"],
        vida=datos["vida"],
        danio=datos["danio"],
        velocidad=datos["velocidad"],
        habilidad=datos["habilidad"],
        turnos_habilidad=datos["turnos_habilidad"]
    )

# -------------------------
# Mapa del juego
# -------------------------

# Función para crear una matriz vacía del tamaño del mapa
# Entradas: ninguna
# Salidas: matriz 10x10 con todas las casillas vacías
def crear_matriz_mapa():
    mapa = []

    for fila in range(TAMANIO_MAPA):
        fila_mapa = []

        for columna in range(TAMANIO_MAPA):
            fila_mapa.append(None)

        mapa.append(fila_mapa)

    return mapa


# Función para validar que una posición esté dentro del mapa
# Entradas: fila y columna
# Salidas: True si la posición existe en el mapa, False si no existe
def posicion_en_rango(fila, columna):
    return 0 <= fila < TAMANIO_MAPA and 0 <= columna < TAMANIO_MAPA


# Función para revisar si una casilla del mapa está vacía
# Entradas: mapa, fila y columna
# Salidas: True si la casilla está vacía, False si está ocupada o fuera del mapa
def casilla_esta_vacia(mapa, fila, columna):
    if not posicion_en_rango(fila, columna):
        return False

    return mapa[fila][columna] is None


# Función para colocar la base central en su posición fija
# Entradas: mapa
# Salidas: objeto BaseCentral creado y colocado en el mapa
def colocar_base_central(mapa):
    fila_base, columna_base = POSICION_BASE
    base = BaseCentral()
    mapa[fila_base][columna_base] = base

    return base


# Función para crear el mapa inicial con la base central
# Entradas: ninguna
# Salidas: mapa inicial y base central
def crear_mapa_inicial():
    mapa = crear_matriz_mapa()
    base = colocar_base_central(mapa)

    return mapa, base


# Función para obtener el símbolo de una casilla del mapa
# Entradas: objeto guardado en una casilla
# Salidas: símbolo de texto para representar la casilla
def obtener_simbolo_casilla(objeto):
    if objeto is None:
        return "."

    if isinstance(objeto, BaseCentral):
        return "B"

    if isinstance(objeto, Torre):
        return "T"

    if isinstance(objeto, Muro):
        return "M"

    if isinstance(objeto, Unidad):
        return "U"

    return "?"


# Función para imprimir el mapa en consola
# Entradas: mapa
# Salidas: ninguna, solo imprime el mapa
def imprimir_mapa_consola(mapa):
    for fila in range(TAMANIO_MAPA):
        linea = ""

        for columna in range(TAMANIO_MAPA):
            simbolo = obtener_simbolo_casilla(mapa[fila][columna])
            linea += simbolo + " "

        print(linea)


# -------------------------
# Estado inicial del juego
# -------------------------

mapa_juego, base_central_actual = crear_mapa_inicial()

dinero_defensor = DINERO_INICIAL_DEFENSOR
dinero_atacante = DINERO_INICIAL_ATACANTE

numero_ronda = 1
rondas_ganadas_defensor = 0
rondas_ganadas_atacante = 0

partida_terminada = False

# Función para reiniciar todos los datos principales de la partida
# Entradas: ninguna
# Salidas: ninguna, reinicia mapa, dinero, marcador, ronda y fase
def reiniciar_estado_partida():
    global mapa_juego
    global base_central_actual
    global dinero_defensor
    global dinero_atacante
    global numero_ronda
    global rondas_ganadas_defensor
    global rondas_ganadas_atacante
    global partida_terminada
    global fase_actual
    global defensa_seleccionada
    global unidad_seleccionada
    global modo_venta

    mapa_juego, base_central_actual = crear_mapa_inicial()

    dinero_defensor = DINERO_INICIAL_DEFENSOR
    dinero_atacante = DINERO_INICIAL_ATACANTE

    numero_ronda = 1
    rondas_ganadas_defensor = 0
    rondas_ganadas_atacante = 0
    partida_terminada = False

    fase_actual = "defensor"
    defensa_seleccionada = None
    unidad_seleccionada = None
    modo_venta = False

# -------------------------
# Estado de la ronda actual
# -------------------------

fase_actual = "defensor"
defensa_seleccionada = None
unidad_seleccionada = None
modo_venta = False

etiqueta_estado = None
etiqueta_mensaje = None
boton_siguiente_ronda = None





# -------------------------
# Interfaz gráfica del mapa
# -------------------------

botones_mapa = []


# Función para obtener el texto visual de una casilla
# Entradas: objeto guardado en una casilla
# Salidas: texto que se mostrará en el botón
def obtener_texto_casilla(objeto):
    if objeto is None:
        return ""

    if isinstance(objeto, BaseCentral):
        return "BASE"

    if isinstance(objeto, Torre):
        if objeto.nombre == "Torre Básica":
            return "TB"
        elif objeto.nombre == "Torre Pesada":
            return "TP"
        elif objeto.nombre == "Torre Mágica":
            return "TM"
        else:
            return "T"

    if isinstance(objeto, Muro):
        return "M"

    if isinstance(objeto, Unidad):
        if objeto.nombre == "Soldado":
            return "S"
        elif objeto.nombre == "Tanque":
            return "TQ"
        elif objeto.nombre == "Unidad Rápida":
            return "UR"
        else:
            return "U"

    return "?"


# Función para obtener el color visual de una casilla
# Entradas: objeto guardado en una casilla
# Salidas: color que se usará en el botón
def obtener_color_casilla(objeto):
    if objeto is None:
        return "white"

    if isinstance(objeto, BaseCentral):
        return faccion_defensor_actual.color_base

    if isinstance(objeto, Torre):
        return faccion_defensor_actual.color_torre

    if isinstance(objeto, Muro):
        return faccion_defensor_actual.color_muro

    if isinstance(objeto, Unidad):
        return faccion_atacante_actual.color_unidad

    return "white"


# Función para actualizar el texto de estado de la partida
# Entradas: ninguna
# Salidas: ninguna, actualiza las etiquetas de estado
def actualizar_estado_visual():
    if etiqueta_estado is not None:
        etiqueta_estado.config(
            text=f"Ronda: {numero_ronda} | Fase: {fase_actual.upper()} | "
                 f"Vida base: {base_central_actual.vida} | "
                 f"Dinero defensor: {dinero_defensor} | Dinero atacante: {dinero_atacante} | "
                 f"Marcador: Defensor {rondas_ganadas_defensor} - Atacante {rondas_ganadas_atacante}"
        )


# Función para actualizar visualmente una casilla del mapa
# Entradas: fila y columna de la casilla
# Salidas: ninguna, actualiza el botón en pantalla
def actualizar_boton_casilla(fila, columna):
    objeto = mapa_juego[fila][columna]

    texto = obtener_texto_casilla(objeto)
    color = obtener_color_casilla(objeto)

    botones_mapa[fila][columna].config(
        text=texto,
        bg=color
    )


# Función para actualizar todo el mapa visual
# Entradas: ninguna
# Salidas: ninguna, actualiza todos los botones del mapa
def actualizar_mapa_visual():
    for fila in range(TAMANIO_MAPA):
        for columna in range(TAMANIO_MAPA):
            actualizar_boton_casilla(fila, columna)

    actualizar_estado_visual()


# Función para seleccionar una defensa para colocar en el mapa
# Entradas: tipo de defensa seleccionada
# Salidas: ninguna, guarda la defensa seleccionada
def seleccionar_defensa(tipo_defensa):
    global defensa_seleccionada
    global unidad_seleccionada
    global modo_venta

    if fase_actual != "defensor":
        etiqueta_mensaje.config(text="No estás en la fase del defensor.")
        return

    defensa_seleccionada = tipo_defensa
    unidad_seleccionada = None
    modo_venta = False

    etiqueta_mensaje.config(text=f"Defensa seleccionada: {tipo_defensa}")


# Función para crear una defensa según la selección actual
# Entradas: tipo de defensa
# Salidas: objeto Muro o Torre, o None si no existe
def crear_defensa(tipo_defensa):
    if tipo_defensa == "Muro":
        return Muro()

    if tipo_defensa in DATOS_TORRES:
        return crear_torre(tipo_defensa)

    return None


# Función para colocar una defensa en el mapa
# Entradas: fila y columna donde se desea colocar
# Salidas: ninguna, coloca la defensa si cumple las condiciones
def colocar_defensa(fila, columna):
    global dinero_defensor

    if defensa_seleccionada is None:
        etiqueta_mensaje.config(text="Primero selecciona una defensa.")
        return

    if not casilla_esta_vacia(mapa_juego, fila, columna):
        etiqueta_mensaje.config(text="No puedes colocar en una casilla ocupada.")
        return

    defensa = crear_defensa(defensa_seleccionada)

    if defensa is None:
        etiqueta_mensaje.config(text="La defensa seleccionada no existe.")
        return

    if dinero_defensor < defensa.costo:
        etiqueta_mensaje.config(text="No tienes suficiente dinero para comprar esta defensa.")
        return

    mapa_juego[fila][columna] = defensa
    dinero_defensor -= defensa.costo

    etiqueta_mensaje.config(text=f"Se colocó {defensa.nombre} en la posición ({fila}, {columna}).")
    actualizar_mapa_visual()

# Función para seleccionar una unidad para colocar en el mapa
# Entradas: tipo de unidad seleccionada
# Salidas: ninguna, guarda la unidad seleccionada
def seleccionar_unidad(tipo_unidad):
    global unidad_seleccionada
    global defensa_seleccionada
    global modo_venta

    if fase_actual != "atacante":
        etiqueta_mensaje.config(text="No estás en la fase del atacante.")
        return

    unidad_seleccionada = tipo_unidad
    defensa_seleccionada = None
    modo_venta = False

    etiqueta_mensaje.config(text=f"Unidad seleccionada: {tipo_unidad}")

# Función para colocar una unidad atacante en el mapa
# Entradas: fila y columna donde se desea colocar
# Salidas: ninguna, coloca la unidad si cumple las condiciones
def colocar_unidad(fila, columna):
    global dinero_atacante

    if unidad_seleccionada is None:
        etiqueta_mensaje.config(text="Primero selecciona una unidad.")
        return

    if not casilla_esta_vacia(mapa_juego, fila, columna):
        etiqueta_mensaje.config(text="No puedes colocar una unidad en una casilla ocupada.")
        return

    unidad = crear_unidad(unidad_seleccionada)

    if unidad is None:
        etiqueta_mensaje.config(text="La unidad seleccionada no existe.")
        return

    if dinero_atacante < unidad.costo:
        etiqueta_mensaje.config(text="No tienes suficiente dinero para comprar esta unidad.")
        return

    mapa_juego[fila][columna] = unidad
    dinero_atacante -= unidad.costo

    etiqueta_mensaje.config(text=f"Se colocó {unidad.nombre} en la posición ({fila}, {columna}).")
    actualizar_mapa_visual()


# Función para activar el modo de venta o eliminación
# Entradas: ninguna
# Salidas: ninguna, activa el modo venta
def activar_modo_venta():
    global modo_venta
    global defensa_seleccionada
    global unidad_seleccionada

    if fase_actual != "defensor" and fase_actual != "atacante":
        etiqueta_mensaje.config(text="Solo puedes vender durante la fase defensor o atacante.")
        return

    modo_venta = True
    defensa_seleccionada = None
    unidad_seleccionada = None

    etiqueta_mensaje.config(text="Modo vender activado. Haz clic sobre el objeto que deseas quitar.")


# Función para cancelar cualquier selección actual
# Entradas: ninguna
# Salidas: ninguna, limpia selección de defensa, unidad y modo venta
def cancelar_seleccion():
    global modo_venta
    global defensa_seleccionada
    global unidad_seleccionada

    modo_venta = False
    defensa_seleccionada = None
    unidad_seleccionada = None

    etiqueta_mensaje.config(text="Selección cancelada.")


# Función para vender o quitar un objeto del mapa
# Entradas: fila y columna donde se hizo clic
# Salidas: ninguna, elimina el objeto si se puede vender
def vender_objeto(fila, columna):
    global dinero_defensor
    global dinero_atacante
    global modo_venta

    objeto = mapa_juego[fila][columna]

    if objeto is None:
        etiqueta_mensaje.config(text="No hay ningún objeto para vender en esta casilla.")
        return

    if isinstance(objeto, BaseCentral):
        etiqueta_mensaje.config(text="No puedes vender la base central.")
        return

    if fase_actual == "defensor":
        if isinstance(objeto, Torre) or isinstance(objeto, Muro):
            dinero_defensor += objeto.costo
            mapa_juego[fila][columna] = None
            modo_venta = False

            etiqueta_mensaje.config(
                text=f"Se vendió {objeto.nombre}. Dinero recuperado: ${objeto.costo}."
            )

            actualizar_mapa_visual()
            return

        etiqueta_mensaje.config(text="El defensor solo puede vender torres o muros.")
        return

    if fase_actual == "atacante":
        if isinstance(objeto, Unidad):
            dinero_atacante += objeto.costo
            mapa_juego[fila][columna] = None
            modo_venta = False

            etiqueta_mensaje.config(
                text=f"Se vendió {objeto.nombre}. Dinero recuperado: ${objeto.costo}."
            )

            actualizar_mapa_visual()
            return

        etiqueta_mensaje.config(text="El atacante solo puede vender unidades.")
        return

    etiqueta_mensaje.config(text="No puedes vender objetos en esta fase.")


# Función para obtener las posiciones de todas las unidades vivas
# Entradas: ninguna
# Salidas: lista con posiciones de unidades vivas
def obtener_posiciones_unidades():
    posiciones = []

    for fila in range(TAMANIO_MAPA):
        for columna in range(TAMANIO_MAPA):
            objeto = mapa_juego[fila][columna]

            if isinstance(objeto, Unidad) and objeto.esta_viva():
                posiciones.append((fila, columna))

    return posiciones


# Función para obtener las posiciones de todas las torres vivas
# Entradas: ninguna
# Salidas: lista con posiciones de torres vivas
def obtener_posiciones_torres():
    posiciones = []

    for fila in range(TAMANIO_MAPA):
        for columna in range(TAMANIO_MAPA):
            objeto = mapa_juego[fila][columna]

            if isinstance(objeto, Torre) and objeto.esta_viva():
                posiciones.append((fila, columna))

    return posiciones


# Función para calcular la distancia entre dos casillas
# Entradas: fila y columna de dos posiciones
# Salidas: distancia entre las dos casillas
def calcular_distancia(fila_1, columna_1, fila_2, columna_2):
    return abs(fila_1 - fila_2) + abs(columna_1 - columna_2)


# Función para buscar una unidad dentro del alcance de una torre
# Entradas: torre, fila de la torre y columna de la torre
# Salidas: posición de la unidad encontrada o None si no hay unidad cerca
def buscar_unidad_en_alcance(torre, fila_torre, columna_torre):
    unidades = obtener_posiciones_unidades()
    unidad_mas_cercana = None
    distancia_mas_cercana = None

    for fila_unidad, columna_unidad in unidades:
        distancia = calcular_distancia(
            fila_torre,
            columna_torre,
            fila_unidad,
            columna_unidad
        )

        if distancia <= torre.alcance:
            if distancia_mas_cercana is None or distancia < distancia_mas_cercana:
                unidad_mas_cercana = (fila_unidad, columna_unidad)
                distancia_mas_cercana = distancia

    return unidad_mas_cercana


# Función para eliminar unidades derrotadas del mapa
# Entradas: ninguna
# Salidas: ninguna, elimina unidades sin vida y suma dinero al defensor
def eliminar_unidades_derrotadas():
    global dinero_defensor

    for fila in range(TAMANIO_MAPA):
        for columna in range(TAMANIO_MAPA):
            objeto = mapa_juego[fila][columna]

            if isinstance(objeto, Unidad) and not objeto.esta_viva():
                dinero_ganado = objeto.costo // 2
                dinero_defensor += dinero_ganado
                mapa_juego[fila][columna] = None


# Función para hacer que las torres ataquen a las unidades
# Entradas: ninguna
# Salidas: ninguna, aplica daño a unidades dentro del alcance
def ejecutar_ataque_torres():
    posiciones_torres = obtener_posiciones_torres()

    for fila_torre, columna_torre in posiciones_torres:
        torre = mapa_juego[fila_torre][columna_torre]

        if not isinstance(torre, Torre):
            continue

        posicion_objetivo = buscar_unidad_en_alcance(torre, fila_torre, columna_torre)

        if posicion_objetivo is not None:
            fila_unidad, columna_unidad = posicion_objetivo
            unidad = mapa_juego[fila_unidad][columna_unidad]

            if isinstance(unidad, Unidad):
                unidad.recibir_danio(torre.danio)

    eliminar_unidades_derrotadas()


# Función para obtener posibles pasos hacia la base central
# Entradas: fila y columna actual de la unidad
# Salidas: lista de posiciones hacia la base
def obtener_pasos_hacia_base(fila, columna):
    fila_base, columna_base = POSICION_BASE
    pasos = []

    diferencia_fila = fila_base - fila
    diferencia_columna = columna_base - columna

    if abs(diferencia_fila) >= abs(diferencia_columna):
        if diferencia_fila > 0:
            pasos.append((fila + 1, columna))
        elif diferencia_fila < 0:
            pasos.append((fila - 1, columna))

        if diferencia_columna > 0:
            pasos.append((fila, columna + 1))
        elif diferencia_columna < 0:
            pasos.append((fila, columna - 1))
    else:
        if diferencia_columna > 0:
            pasos.append((fila, columna + 1))
        elif diferencia_columna < 0:
            pasos.append((fila, columna - 1))

        if diferencia_fila > 0:
            pasos.append((fila + 1, columna))
        elif diferencia_fila < 0:
            pasos.append((fila - 1, columna))

    return pasos


# Función para mover una unidad o atacar un obstáculo cercano
# Entradas: fila y columna de la unidad
# Salidas: ninguna, mueve o ataca según la casilla siguiente
def mover_o_atacar_unidad(fila, columna):
    unidad = mapa_juego[fila][columna]

    if not isinstance(unidad, Unidad):
        return

    for movimiento in range(unidad.velocidad):
        if not unidad.esta_viva() or not base_central_actual.esta_viva():
            return

        pasos = obtener_pasos_hacia_base(fila, columna)
        accion_realizada = False

        for nueva_fila, nueva_columna in pasos:
            if not posicion_en_rango(nueva_fila, nueva_columna):
                continue

            objetivo = mapa_juego[nueva_fila][nueva_columna]

            if objetivo is None:
                mapa_juego[nueva_fila][nueva_columna] = unidad
                mapa_juego[fila][columna] = None

                fila = nueva_fila
                columna = nueva_columna
                accion_realizada = True
                break

            if isinstance(objetivo, BaseCentral):
                objetivo.recibir_danio(unidad.danio)
                accion_realizada = True
                return

            if isinstance(objetivo, Muro) or isinstance(objetivo, Torre):
                objetivo.recibir_danio(unidad.danio)

                if isinstance(objetivo, Muro) and not objetivo.esta_vivo():
                    mapa_juego[nueva_fila][nueva_columna] = None

                if isinstance(objetivo, Torre) and not objetivo.esta_viva():
                    mapa_juego[nueva_fila][nueva_columna] = None

                accion_realizada = True
                return
            
        if not accion_realizada:
            return


# Función para ejecutar el turno de movimiento y ataque de las unidades
# Entradas: ninguna
# Salidas: ninguna, mueve unidades o daña defensas/base
def ejecutar_turno_unidades():
    posiciones_unidades = obtener_posiciones_unidades()

    for fila, columna in posiciones_unidades:
        objeto = mapa_juego[fila][columna]

        if isinstance(objeto, Unidad):
            mover_o_atacar_unidad(fila, columna)


# Función para verificar si ya existe un ganador de la ronda
# Entradas: ninguna
# Salidas: "atacante", "defensor" o None
def verificar_ganador_ronda():
    if not base_central_actual.esta_viva():
        return "atacante"

    if len(obtener_posiciones_unidades()) == 0:
        return "defensor"

    return None


# Función para registrar el ganador de una ronda
# Entradas: ganador de la ronda
# Salidas: ninguna, actualiza marcador y verifica si terminó la partida
def registrar_ganador_ronda(ganador):
    global rondas_ganadas_defensor
    global rondas_ganadas_atacante
    global fase_actual
    global partida_terminada

    fase_actual = "fin_ronda"

    if ganador == "defensor":
        rondas_ganadas_defensor += 1
        mensaje = f"Gana el defensor la ronda {numero_ronda}."

    elif ganador == "atacante":
        rondas_ganadas_atacante += 1
        mensaje = f"Gana el atacante la ronda {numero_ronda}."

    else:
        mensaje = "No se pudo determinar el ganador de la ronda."

    if rondas_ganadas_defensor >= RONDAS_PARA_GANAR:
        partida_terminada = True
        mensaje += " El defensor ganó la partida completa."

    elif rondas_ganadas_atacante >= RONDAS_PARA_GANAR:
        partida_terminada = True
        mensaje += " El atacante ganó la partida completa."

    else:
        mensaje += " Presiona 'Siguiente ronda' para continuar."

    etiqueta_mensaje.config(text=mensaje)

    if boton_siguiente_ronda is not None:
        if partida_terminada:
            boton_siguiente_ronda.config(state="disabled")
        else:
            boton_siguiente_ronda.config(state="normal")

    actualizar_mapa_visual()


# Función para preparar una nueva ronda
# Entradas: ninguna
# Salidas: ninguna, reinicia mapa, dinero, base y fase
def preparar_siguiente_ronda():
    global mapa_juego
    global base_central_actual
    global dinero_defensor
    global dinero_atacante
    global numero_ronda
    global fase_actual
    global defensa_seleccionada
    global unidad_seleccionada
    global modo_venta

    if partida_terminada:
        etiqueta_mensaje.config(text="La partida ya terminó. No se pueden iniciar más rondas.")
        return

    if fase_actual != "fin_ronda":
        etiqueta_mensaje.config(text="Primero debe terminar la ronda actual.")
        return

    numero_ronda += 1

    mapa_juego, base_central_actual = crear_mapa_inicial()

    dinero_defensor = DINERO_INICIAL_DEFENSOR + ((numero_ronda - 1) * BONO_DINERO_POR_RONDA)
    dinero_atacante = DINERO_INICIAL_ATACANTE + ((numero_ronda - 1) * BONO_DINERO_POR_RONDA)

    fase_actual = "defensor"
    defensa_seleccionada = None
    unidad_seleccionada = None
    modo_venta = False

    if boton_siguiente_ronda is not None:
        boton_siguiente_ronda.config(state="disabled")

    etiqueta_mensaje.config(
        text=f"Inicia la ronda {numero_ronda}. El defensor debe colocar sus defensas."
    )

    actualizar_mapa_visual()

# Función para ejecutar el combate completo de la ronda
# Entradas: ninguna
# Salidas: ninguna, ejecuta combate y determina ganador
def ejecutar_combate():
    global fase_actual

    if partida_terminada:
        etiqueta_mensaje.config(text="La partida ya terminó.")
        return

    if fase_actual != "atacante":
        etiqueta_mensaje.config(text="Primero debe terminar la fase del defensor.")
        return

    if len(obtener_posiciones_unidades()) == 0:
        etiqueta_mensaje.config(text="El atacante debe colocar al menos una unidad antes de combatir.")
        return

    fase_actual = "combate"
    ganador = None

    for turno in range(1, LIMITE_TURNOS_COMBATE + 1):
        ejecutar_ataque_torres()
        ganador = verificar_ganador_ronda()

        if ganador is not None:
            break

        ejecutar_turno_unidades()
        ganador = verificar_ganador_ronda()

        if ganador is not None:
            break

    if ganador is None:
        ganador = "defensor"

    registrar_ganador_ronda(ganador)


# Función para manejar el clic sobre una casilla del mapa
# Entradas: fila y columna de la casilla presionada
# Salidas: ninguna, ejecuta acción según la fase actual
def manejar_click_casilla(fila, columna):
    if modo_venta:
        vender_objeto(fila, columna)
        return

    if fase_actual == "defensor":
        colocar_defensa(fila, columna)

    elif fase_actual == "atacante":
        colocar_unidad(fila, columna)

    else:
        etiqueta_mensaje.config(text="La fase actual no permite colocar objetos.")


# Función para terminar la fase del defensor
# Entradas: ninguna
# Salidas: ninguna, cambia la fase actual a atacante
def terminar_fase_defensor():
    global fase_actual
    global defensa_seleccionada
    global unidad_seleccionada
    global modo_venta

    fase_actual = "atacante"
    defensa_seleccionada = None
    unidad_seleccionada = None
    modo_venta = False

    etiqueta_mensaje.config(text="Fase del defensor terminada. Ahora sigue la fase atacante.")
    actualizar_estado_visual()


# Función para crear los botones de la cuadrícula del mapa
# Entradas: frame donde se colocará el mapa
# Salidas: ninguna, crea los botones en pantalla
def crear_botones_mapa(frame_mapa):
    global botones_mapa

    botones_mapa = []

    for fila in range(TAMANIO_MAPA):
        fila_botones = []

        for columna in range(TAMANIO_MAPA):
            boton = tk.Button(
                frame_mapa,
                text="",
                width=8,
                height=3,
                bg="white",
                relief="solid",
                command=lambda f=fila, c=columna: manejar_click_casilla(f, c)
            )

            boton.grid(row=fila, column=columna, padx=1, pady=1)
            fila_botones.append(boton)

        botones_mapa.append(fila_botones)

    actualizar_mapa_visual()

# Función para iniciar la partida con las facciones seleccionadas
# Entradas: ventana de selección, facción del defensor y facción del atacante
# Salidas: ninguna, valida facciones y abre el mapa del juego
def iniciar_partida_con_facciones(ventana_seleccion, seleccion_defensor, seleccion_atacante, etiqueta_error):
    global faccion_defensor_actual
    global faccion_atacante_actual

    nombre_faccion_defensor = seleccion_defensor.get()
    nombre_faccion_atacante = seleccion_atacante.get()

    faccion_defensor = obtener_faccion(nombre_faccion_defensor)
    faccion_atacante = obtener_faccion(nombre_faccion_atacante)

    if faccion_defensor is None or faccion_atacante is None:
        etiqueta_error.config(text="Debes seleccionar facciones válidas.")
        return

    if not validar_facciones(faccion_defensor, faccion_atacante):
        etiqueta_error.config(text="El defensor y el atacante no pueden usar la misma facción.")
        return

    faccion_defensor_actual = faccion_defensor
    faccion_atacante_actual = faccion_atacante

    reiniciar_estado_partida()

    ventana_seleccion.destroy()
    abrir_ventana_mapa()


# Función para abrir la pantalla de selección de facciones
# Entradas: ninguna
# Salidas: ninguna, muestra la ventana para elegir facciones
def abrir_ventana_seleccion_facciones():
    ventana_seleccion = tk.Tk()
    ventana_seleccion.title("Selección de facciones")
    ventana_seleccion.geometry("500x400")
    ventana_seleccion.resizable(False, False)

    titulo = tk.Label(
        ventana_seleccion,
        text="Selección de Facciones",
        font=("Arial", 18, "bold")
    )
    titulo.pack(pady=20)

    descripcion = tk.Label(
        ventana_seleccion,
        text="Elige una facción para cada jugador.\nNo pueden usar la misma facción.",
        font=("Arial", 11)
    )
    descripcion.pack(pady=5)

    nombres_facciones = list(FACCIONES.keys())

    seleccion_defensor = tk.StringVar(ventana_seleccion)
    seleccion_defensor.set(nombres_facciones[0])

    seleccion_atacante = tk.StringVar(ventana_seleccion)
    seleccion_atacante.set(nombres_facciones[2])

    frame_opciones = tk.Frame(ventana_seleccion)
    frame_opciones.pack(pady=20)

    etiqueta_defensor = tk.Label(
        frame_opciones,
        text="Facción del defensor:",
        font=("Arial", 11, "bold")
    )
    etiqueta_defensor.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    menu_defensor = tk.OptionMenu(
        frame_opciones,
        seleccion_defensor,
        *nombres_facciones
    )
    menu_defensor.config(width=18)
    menu_defensor.grid(row=0, column=1, padx=10, pady=10)

    etiqueta_atacante = tk.Label(
        frame_opciones,
        text="Facción del atacante:",
        font=("Arial", 11, "bold")
    )
    etiqueta_atacante.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    menu_atacante = tk.OptionMenu(
        frame_opciones,
        seleccion_atacante,
        *nombres_facciones
    )
    menu_atacante.config(width=18)
    menu_atacante.grid(row=1, column=1, padx=10, pady=10)

    etiqueta_error = tk.Label(
        ventana_seleccion,
        text="",
        fg="red",
        font=("Arial", 10)
    )
    etiqueta_error.pack(pady=5)

    boton_iniciar = tk.Button(
        ventana_seleccion,
        text="Iniciar partida",
        width=20,
        height=2,
        command=lambda: iniciar_partida_con_facciones(
            ventana_seleccion,
            seleccion_defensor,
            seleccion_atacante,
            etiqueta_error
        )
    )
    boton_iniciar.pack(pady=20)

    ventana_seleccion.mainloop()

# Función para abrir la ventana del mapa del juego
# Entradas: ninguna
# Salidas: ninguna, muestra la ventana del mapa
def abrir_ventana_mapa():
    global etiqueta_estado
    global etiqueta_mensaje

    ventana_juego = tk.Tk()
    ventana_juego.title("Defensa y Asalto de Base - Mapa")
    ventana_juego.geometry("1250x780")

    titulo = tk.Label(
        ventana_juego,
        text="Defensa y Asalto de Base",
        font=("Arial", 18, "bold")
    )
    titulo.pack(pady=10)

    informacion = tk.Label(
        ventana_juego,
        text=f"Defensor: {faccion_defensor_actual.nombre} | Atacante: {faccion_atacante_actual.nombre}"
    )
    informacion.pack()

    etiqueta_estado = tk.Label(
        ventana_juego,
        text=""
    )
    etiqueta_estado.pack(pady=5)

    contenedor_principal = tk.Frame(ventana_juego)
    contenedor_principal.pack(pady=10)

    panel_defensor = tk.LabelFrame(
        contenedor_principal,
        text="Fase defensor",
        padx=10,
        pady=10
    )
    panel_defensor.grid(row=0, column=0, padx=15, sticky="n")

    boton_muro = tk.Button(
        panel_defensor,
        text="Muro - $30",
        width=18,
        command=lambda: seleccionar_defensa("Muro")
    )
    boton_muro.pack(pady=5)

    boton_torre_basica = tk.Button(
        panel_defensor,
        text="Torre Básica - $50",
        width=18,
        command=lambda: seleccionar_defensa("Basica")
    )
    boton_torre_basica.pack(pady=5)

    boton_torre_pesada = tk.Button(
        panel_defensor,
        text="Torre Pesada - $90",
        width=18,
        command=lambda: seleccionar_defensa("Pesada")
    )
    boton_torre_pesada.pack(pady=5)

    boton_torre_magica = tk.Button(
        panel_defensor,
        text="Torre Mágica - $75",
        width=18,
        command=lambda: seleccionar_defensa("Magica")
    )
    boton_torre_magica.pack(pady=5)

    boton_vender_defensor = tk.Button(
        panel_defensor,
        text="Vender / quitar",
        width=18,
        command=activar_modo_venta
    )
    boton_vender_defensor.pack(pady=5)

    boton_cancelar_defensor = tk.Button(
        panel_defensor,
        text="Cancelar selección",
        width=18,
        command=cancelar_seleccion
    )
    boton_cancelar_defensor.pack(pady=5)

    boton_terminar = tk.Button(
        panel_defensor,
        text="Terminar fase defensor",
        width=18,
        command=terminar_fase_defensor
    )
    boton_terminar.pack(pady=15)

    panel_atacante = tk.LabelFrame(
        contenedor_principal,
        text="Fase atacante",
        padx=10,
        pady=10
    )
    panel_atacante.grid(row=0, column=2, padx=15, sticky="n")

    boton_soldado = tk.Button(
        panel_atacante,
        text="Soldado - $40",
        width=18,
        command=lambda: seleccionar_unidad("Soldado")
    )
    boton_soldado.pack(pady=5)

    boton_tanque = tk.Button(
        panel_atacante,
        text="Tanque - $90",
        width=18,
        command=lambda: seleccionar_unidad("Tanque")
    )
    boton_tanque.pack(pady=5)

    boton_rapida = tk.Button(
        panel_atacante,
        text="Unidad Rápida - $60",
        width=18,
        command=lambda: seleccionar_unidad("Rapida")
    )
    boton_rapida.pack(pady=5)

    boton_vender_atacante = tk.Button(
        panel_atacante,
        text="Vender / quitar",
        width=18,
        command=activar_modo_venta
    )
    boton_vender_atacante.pack(pady=5)

    boton_cancelar_atacante = tk.Button(
        panel_atacante,
        text="Cancelar selección",
        width=18,
        command=cancelar_seleccion
    )
    boton_cancelar_atacante.pack(pady=5)

    boton_combate = tk.Button(
        panel_atacante,
        text="Ejecutar combate",
        width=18,
        command=ejecutar_combate
    )
    boton_combate.pack(pady=15)

    global boton_siguiente_ronda

    boton_siguiente_ronda = tk.Button(
        panel_atacante,
        text="Siguiente ronda",
        width=18,
        state="disabled",
        command=preparar_siguiente_ronda
    )
    boton_siguiente_ronda.pack(pady=5)

    frame_mapa = tk.Frame(contenedor_principal)
    frame_mapa.grid(row=0, column=1)

    crear_botones_mapa(frame_mapa)

    etiqueta_mensaje = tk.Label(
        ventana_juego,
        text="Selecciona una defensa y luego presiona una casilla vacía.",
        font=("Arial", 10)
    )
    etiqueta_mensaje.pack(pady=10)

    actualizar_estado_visual()

    ventana_juego.mainloop()


abrir_ventana_seleccion_facciones()