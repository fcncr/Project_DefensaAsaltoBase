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

# Función para actualizar una victoria de un jugador según el rol utilizado.
# Entradas: nombre_usuario y rol.
# Salidas: True si se actualizó correctamente, False si el usuario no existe.
def actualizar_victoria(nombre_usuario, rol):
    usuarios = cargar_usuarios()

    if nombre_usuario not in usuarios:
        return False

    jugador = usuarios[nombre_usuario]
    jugador.sumar_victoria(rol)

    usuarios[nombre_usuario] = jugador
    guardar_usuarios(usuarios)

    return True


# Función para obtener el top 5 de jugadores según el rol indicado.
# Entradas: rol, puede ser "defensor" o "atacante".
# Salidas: lista con los mejores 5 jugadores.
def obtener_top_jugadores(rol):
    usuarios = cargar_usuarios()
    lista_jugadores = list(usuarios.values())

    if rol == "defensor":
        lista_jugadores.sort(
            key=lambda jugador: jugador.victorias_defensor,
            reverse=True
        )

    elif rol == "atacante":
        lista_jugadores.sort(
            key=lambda jugador: jugador.victorias_atacante,
            reverse=True
        )

    return lista_jugadores[:5]


# Función para abrir la ventana principal del sistema de usuarios.
# Desde esta ventana se puede registrar, iniciar sesión, ver ranking o salir.
def abrir_ventana_inicio():
    crear_archivo_usuarios()

    ventana_inicio = tk.Tk()
    ventana_inicio.title("Defensa y Asalto de Base - Inicio")
    ventana_inicio.geometry("620x500")
    ventana_inicio.resizable(False, False)
    ventana_inicio.config(bg=COLOR_FONDO_APP)

    titulo = tk.Label(
        ventana_inicio,
        text="Defensa y Asalto de Base",
        font=("Arial", 24, "bold"),
        bg=COLOR_FONDO_APP,
        fg=COLOR_TITULO
    )
    titulo.pack(pady=(35, 8))

    subtitulo = tk.Label(
        ventana_inicio,
        text="Sistema de jugadores",
        font=("Arial", 12, "bold"),
        bg=COLOR_FONDO_APP,
        fg=COLOR_TEXTO
    )
    subtitulo.pack(pady=(0, 18))

    panel = tk.Frame(
        ventana_inicio,
        bg=COLOR_PANEL,
        bd=1,
        relief="solid"
    )
    panel.pack(padx=70, pady=20, fill="both", expand=True)

    descripcion = tk.Label(
        panel,
        text="Registra jugadores, inicia una partida o consulta el ranking.",
        font=("Arial", 11),
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO,
        wraplength=380,
        justify="center"
    )
    descripcion.pack(pady=(30, 18))

    boton_registro = crear_boton_estilizado(
        panel,
        "Registrar usuario",
        lambda: abrir_ventana_registro(ventana_inicio),
        ancho=24,
        color_fondo=COLOR_BOTON_SECUNDARIO
    )
    boton_registro.pack(pady=8)

    boton_login = crear_boton_estilizado(
        panel,
        "Iniciar partida",
        lambda: abrir_ventana_login(ventana_inicio),
        ancho=24,
        color_fondo=COLOR_BOTON
    )
    boton_login.pack(pady=8)

    boton_ranking = crear_boton_estilizado(
        panel,
        "Ver ranking",
        lambda: abrir_ventana_ranking(ventana_inicio),
        ancho=24,
        color_fondo=COLOR_BOTON_SECUNDARIO
    )
    boton_ranking.pack(pady=8)

    boton_salir = crear_boton_estilizado(
        panel,
        "Salir",
        ventana_inicio.destroy,
        ancho=24,
        color_fondo=COLOR_BOTON_ALERTA
    )
    boton_salir.pack(pady=8)

    ventana_inicio.mainloop()


# Función para abrir la ventana de registro de usuarios.
# Entradas: ventana padre.
# Salidas: ninguna, permite registrar nuevos jugadores.
def abrir_ventana_registro(ventana_padre):
    ventana_registro = tk.Toplevel(ventana_padre)
    ventana_registro.title("Registro de usuario")
    ventana_registro.geometry("500x430")
    ventana_registro.resizable(False, False)
    ventana_registro.config(bg=COLOR_FONDO_APP)
    ventana_registro.grab_set()

    titulo = tk.Label(
        ventana_registro,
        text="Registrar jugador",
        font=("Arial", 20, "bold"),
        bg=COLOR_FONDO_APP,
        fg=COLOR_TITULO
    )
    titulo.pack(pady=(25, 8))

    subtitulo = tk.Label(
        ventana_registro,
        text="Crea una cuenta para guardar tus victorias.",
        font=("Arial", 11),
        bg=COLOR_FONDO_APP,
        fg=COLOR_TEXTO
    )
    subtitulo.pack(pady=(0, 15))

    panel = tk.Frame(
        ventana_registro,
        bg=COLOR_PANEL,
        bd=1,
        relief="solid"
    )
    panel.pack(padx=55, pady=15, fill="both", expand=True)

    etiqueta_usuario = tk.Label(
        panel,
        text="Nombre de usuario:",
        font=("Arial", 11, "bold"),
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO
    )
    etiqueta_usuario.pack(pady=(25, 5))

    entrada_usuario = tk.Entry(
        panel,
        width=30,
        font=("Arial", 11),
        bg=COLOR_ESTADO,
        fg=COLOR_TEXTO,
        relief="flat",
        bd=4
    )
    entrada_usuario.pack(pady=5)

    etiqueta_contrasena = tk.Label(
        panel,
        text="Contraseña:",
        font=("Arial", 11, "bold"),
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO
    )
    etiqueta_contrasena.pack(pady=(12, 5))

    entrada_contrasena = tk.Entry(
        panel,
        width=30,
        font=("Arial", 11),
        bg=COLOR_ESTADO,
        fg=COLOR_TEXTO,
        relief="flat",
        bd=4,
        show="*"
    )
    entrada_contrasena.pack(pady=5)

    etiqueta_confirmar = tk.Label(
        panel,
        text="Confirmar contraseña:",
        font=("Arial", 11, "bold"),
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO
    )
    etiqueta_confirmar.pack(pady=(12, 5))

    entrada_confirmar = tk.Entry(
        panel,
        width=30,
        font=("Arial", 11),
        bg=COLOR_ESTADO,
        fg=COLOR_TEXTO,
        relief="flat",
        bd=4,
        show="*"
    )
    entrada_confirmar.pack(pady=5)

    etiqueta_mensaje = tk.Label(
        panel,
        text="",
        font=("Arial", 10, "bold"),
        bg=COLOR_PANEL,
        fg="red",
        wraplength=350,
        justify="center"
    )
    etiqueta_mensaje.pack(pady=12)

    # Función interna para registrar al usuario.
    # Valida que las contraseñas coincidan y luego usa registrar_usuario().
    def accion_registrar():
        nombre_usuario = entrada_usuario.get()
        contrasena = entrada_contrasena.get()
        confirmar = entrada_confirmar.get()

        if contrasena != confirmar:
            etiqueta_mensaje.config(
                text="Las contraseñas no coinciden.",
                fg="red"
            )
            return

        registrado, mensaje = registrar_usuario(nombre_usuario, contrasena)

        if registrado:
            etiqueta_mensaje.config(
                text=mensaje,
                fg="green"
            )

            entrada_usuario.delete(0, tk.END)
            entrada_contrasena.delete(0, tk.END)
            entrada_confirmar.delete(0, tk.END)
            entrada_usuario.focus()

        else:
            etiqueta_mensaje.config(
                text=mensaje,
                fg="red"
            )

    frame_botones = tk.Frame(
        panel,
        bg=COLOR_PANEL
    )
    frame_botones.pack(pady=(5, 20))

    boton_registrar = crear_boton_estilizado(
        frame_botones,
        "Registrar",
        accion_registrar,
        ancho=15,
        color_fondo=COLOR_BOTON
    )
    boton_registrar.grid(row=0, column=0, padx=6)

    boton_cerrar = crear_boton_estilizado(
        frame_botones,
        "Volver",
        ventana_registro.destroy,
        ancho=15,
        color_fondo=COLOR_BOTON_SECUNDARIO
    )
    boton_cerrar.grid(row=0, column=1, padx=6)

    entrada_usuario.focus()
    # Función interna para registrar al usuario.
    def accion_registrar():
        nombre_usuario = entrada_usuario.get()
        contrasena = entrada_contrasena.get()
        confirmar = entrada_confirmar.get()

        if contrasena != confirmar:
            etiqueta_mensaje.config(
                text="Las contraseñas no coinciden.",
                fg="red"
            )
            return

        registrado, mensaje = registrar_usuario(nombre_usuario, contrasena)

        if registrado:
            etiqueta_mensaje.config(
                text=mensaje,
                fg="green"
            )

            entrada_usuario.delete(0, tk.END)
            entrada_contrasena.delete(0, tk.END)
            entrada_confirmar.delete(0, tk.END)

        else:
            etiqueta_mensaje.config(
                text=mensaje,
                fg="red"
            )

    boton_registrar = tk.Button(
        ventana_registro,
        text="Registrar",
        width=20,
        command=accion_registrar
    )
    boton_registrar.pack(pady=10)


# Función para abrir la ventana de inicio de sesión.
# Permite iniciar sesión con dos jugadores diferentes.
def abrir_ventana_login(ventana_inicio):
    ventana_login = tk.Toplevel(ventana_inicio)
    ventana_login.title("Inicio de sesión")
    ventana_login.geometry("520x430")
    ventana_login.resizable(False, False)

    titulo = tk.Label(
        ventana_login,
        text="Inicio de sesión de jugadores",
        font=("Arial", 15, "bold")
    )
    titulo.pack(pady=15)

    descripcion = tk.Label(
        ventana_login,
        text="Ambos jugadores deben iniciar sesión antes de comenzar."
    )
    descripcion.pack(pady=5)

    frame = tk.Frame(ventana_login)
    frame.pack(pady=15)

    # Jugador 1
    etiqueta_jugador_1 = tk.Label(
        frame,
        text="Jugador 1",
        font=("Arial", 11, "bold")
    )
    etiqueta_jugador_1.grid(row=0, column=0, columnspan=2, pady=8)

    tk.Label(frame, text="Usuario:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

    entrada_usuario_1 = tk.Entry(
        frame,
        width=25
    )
    entrada_usuario_1.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame, text="Contraseña:").grid(row=2, column=0, padx=5, pady=5, sticky="e")

    entrada_contrasena_1 = tk.Entry(
        frame,
        width=25,
        show="*"
    )
    entrada_contrasena_1.grid(row=2, column=1, padx=5, pady=5)

    # Jugador 2
    etiqueta_jugador_2 = tk.Label(
        frame,
        text="Jugador 2",
        font=("Arial", 11, "bold")
    )
    etiqueta_jugador_2.grid(row=3, column=0, columnspan=2, pady=15)

    tk.Label(frame, text="Usuario:").grid(row=4, column=0, padx=5, pady=5, sticky="e")

    entrada_usuario_2 = tk.Entry(
        frame,
        width=25
    )
    entrada_usuario_2.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(frame, text="Contraseña:").grid(row=5, column=0, padx=5, pady=5, sticky="e")

    entrada_contrasena_2 = tk.Entry(
        frame,
        width=25,
        show="*"
    )
    entrada_contrasena_2.grid(row=5, column=1, padx=5, pady=5)

    etiqueta_mensaje = tk.Label(
        ventana_login,
        text="",
        fg="red"
    )
    etiqueta_mensaje.pack(pady=10)

    # Función interna para validar los dos inicios de sesión.
    def accion_iniciar_partida():
        usuario_1 = entrada_usuario_1.get().strip()
        contrasena_1 = entrada_contrasena_1.get().strip()

        usuario_2 = entrada_usuario_2.get().strip()
        contrasena_2 = entrada_contrasena_2.get().strip()

        if usuario_1 == usuario_2:
            etiqueta_mensaje.config(
                text="Los jugadores deben ser usuarios diferentes.",
                fg="red"
            )
            return

        login_1, jugador_1, mensaje_1 = validar_login(usuario_1, contrasena_1)

        if not login_1:
            etiqueta_mensaje.config(
                text="Jugador 1: " + mensaje_1,
                fg="red"
            )
            return

        login_2, jugador_2, mensaje_2 = validar_login(usuario_2, contrasena_2)

        if not login_2:
            etiqueta_mensaje.config(
                text="Jugador 2: " + mensaje_2,
                fg="red"
            )
            return

        ventana_login.destroy()
        ventana_inicio.destroy()

        abrir_ventana_seleccion_facciones(
            jugador_1.nombre_usuario,
            jugador_2.nombre_usuario
        )

    boton_iniciar = tk.Button(
        ventana_login,
        text="Continuar",
        width=20,
        height=2,
        command=accion_iniciar_partida
    )
    boton_iniciar.pack(pady=10)


# Función para abrir la ventana de ranking.
# Muestra top 5 de defensores y top 5 de atacantes.
def abrir_ventana_ranking(ventana_padre):
    ventana_ranking = tk.Toplevel(ventana_padre)
    ventana_ranking.title("Ranking de jugadores")
    ventana_ranking.geometry("620x430")
    ventana_ranking.resizable(False, False)

    titulo = tk.Label(
        ventana_ranking,
        text="Ranking de jugadores",
        font=("Arial", 16, "bold")
    )
    titulo.pack(pady=15)

    frame_rankings = tk.Frame(ventana_ranking)
    frame_rankings.pack(pady=10)

    # Ranking defensores
    frame_defensores = tk.LabelFrame(
        frame_rankings,
        text="Top 5 defensores",
        padx=15,
        pady=10
    )
    frame_defensores.grid(row=0, column=0, padx=15, sticky="n")

    top_defensores = obtener_top_jugadores("defensor")

    if len(top_defensores) == 0:
        tk.Label(
            frame_defensores,
            text="No hay jugadores registrados."
        ).pack()

    else:
        posicion = 1

        for jugador in top_defensores:
            texto = f"{posicion}. {jugador.nombre_usuario} - {jugador.victorias_defensor} victorias"

            tk.Label(
                frame_defensores,
                text=texto,
                anchor="w",
                width=30
            ).pack(pady=3)

            posicion += 1

    # Ranking atacantes
    frame_atacantes = tk.LabelFrame(
        frame_rankings,
        text="Top 5 atacantes",
        padx=15,
        pady=10
    )
    frame_atacantes.grid(row=0, column=1, padx=15, sticky="n")

    top_atacantes = obtener_top_jugadores("atacante")

    if len(top_atacantes) == 0:
        tk.Label(
            frame_atacantes,
            text="No hay jugadores registrados."
        ).pack()

    else:
        posicion = 1

        for jugador in top_atacantes:
            texto = f"{posicion}. {jugador.nombre_usuario} - {jugador.victorias_atacante} victorias"

            tk.Label(
                frame_atacantes,
                text=texto,
                anchor="w",
                width=30
            ).pack(pady=3)

            posicion += 1

    boton_cerrar = tk.Button(
        ventana_ranking,
        text="Cerrar",
        width=15,
        command=ventana_ranking.destroy
    )
    boton_cerrar.pack(pady=20)































































































































































































































































































































































































































































































































































































































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

COLOR_FONDO_APP = "#EDE7DD"
COLOR_PANEL = "#F8F5F0"
COLOR_BORDE = "#C7B8A3"
COLOR_CASILLA_VACIA = "#F4EFE6"
COLOR_CASILLA_BORDE = "#B8A98F"
COLOR_TEXTO_CLARO = "white"
COLOR_TEXTO_OSCURO = "#2F2A24"
COLOR_TEXTO = "#2F2A24"
COLOR_TITULO = "#5A4A3A"
COLOR_BOTON = "#8C6A43"
COLOR_BOTON_TEXTO = "white"
COLOR_BOTON_SECUNDARIO = "#A78A6A"
COLOR_BOTON_ALERTA = "#7A3E2B"
COLOR_ESTADO = "#DDD2C2"

# Nombres temporales de jugadores
NOMBRE_JUGADOR_DEFENSOR = "Jugador DefensorN"
NOMBRE_JUGADOR_ATACANTE = "Jugador AtacanteN"

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
    # Función para inicializar una torre defensiva
    # Entradas: nombre, costo, vida, daño, alcance, habilidad y turnos de habilidad
    # Salidas: objeto Torre inicializado
    def __init__(self, nombre, costo, vida, danio, alcance, habilidad, turnos_habilidad):
        self.nombre = nombre
        self.costo = costo
        self.vida = vida
        self.danio = danio
        self.alcance = alcance
        self.habilidad = habilidad
        self.turnos_habilidad = turnos_habilidad
        self.contador_turnos = 0

    # Función para verificar si la torre sigue viva
    # Entradas: ninguna
    # Salidas: True si la vida es mayor a 0, False si no
    def esta_viva(self):
        return self.vida > 0

    # Función para reducir la vida de la torre
    # Entradas: cantidad de daño recibido
    # Salidas: ninguna, actualiza la vida de la torre
    def recibir_danio(self, cantidad):
        self.vida -= cantidad

        if self.vida < 0:
            self.vida = 0

    # Función para aumentar el contador de turnos de la torre
    # Entradas: ninguna
    # Salidas: ninguna, suma un turno al contador
    def avanzar_turno_habilidad(self):
        self.contador_turnos += 1

    # Función para verificar si la habilidad de la torre está lista
    # Entradas: ninguna
    # Salidas: True si la habilidad puede activarse, False si no
    def habilidad_lista(self):
        return self.contador_turnos >= self.turnos_habilidad

    # Función para reiniciar el contador de habilidad de la torre
    # Entradas: ninguna
    # Salidas: ninguna, reinicia el contador de turnos
    def reiniciar_habilidad(self):
        self.contador_turnos = 0

#Clase Unidad
class Unidad:
    # Función para inicializar una unidad atacante
    # Entradas: nombre, costo, vida, daño, velocidad, habilidad y turnos de habilidad
    # Salidas: objeto Unidad inicializado
    def __init__(self, nombre, costo, vida, danio, velocidad, habilidad, turnos_habilidad):
        self.nombre = nombre
        self.costo = costo
        self.vida = vida
        self.danio = danio
        self.velocidad = velocidad
        self.habilidad = habilidad
        self.turnos_habilidad = turnos_habilidad
        self.contador_turnos = 0

        self.turnos_congelada = 0
        self.escudo_activo = False
        self.turnos_escudo = 0
        self.velocidad_extra_temporal = 0

    # Función para verificar si la unidad sigue viva
    # Entradas: ninguna
    # Salidas: True si la vida es mayor a 0, False si no
    def esta_viva(self):
        return self.vida > 0

    # Función para reducir la vida de la unidad
    # Entradas: cantidad de daño recibido
    # Salidas: ninguna, actualiza la vida de la unidad
    def recibir_danio(self, cantidad):
        if self.escudo_activo:
            cantidad = cantidad // 2

        self.vida -= cantidad

        if self.vida < 0:
            self.vida = 0

    # Función para aumentar el contador de turnos de la unidad
    # Entradas: ninguna
    # Salidas: ninguna, suma un turno al contador
    def avanzar_turno_habilidad(self):
        self.contador_turnos += 1

    # Función para verificar si la habilidad de la unidad está lista
    # Entradas: ninguna
    # Salidas: True si la habilidad puede activarse, False si no
    def habilidad_lista(self):
        return self.contador_turnos >= self.turnos_habilidad

    # Función para reiniciar el contador de habilidad de la unidad
    # Entradas: ninguna
    # Salidas: ninguna, reinicia el contador de turnos
    def reiniciar_habilidad(self):
        self.contador_turnos = 0

    # Función para verificar si la unidad está congelada
    # Entradas: ninguna
    # Salidas: True si tiene turnos de congelamiento, False si no
    def esta_congelada(self):
        return self.turnos_congelada > 0

    # Función para reducir los efectos temporales de la unidad
    # Entradas: ninguna
    # Salidas: ninguna, reduce congelamiento, escudo y velocidad extra
    def actualizar_efectos_temporales(self):
        if self.turnos_congelada > 0:
            self.turnos_congelada -= 1

        if self.turnos_escudo > 0:
            self.turnos_escudo -= 1

            if self.turnos_escudo == 0:
                self.escudo_activo = False

        self.velocidad_extra_temporal = 0

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

# Función para contar cuántas defensas tiene colocadas el defensor
# Entradas: ninguna
# Salidas: cantidad de torres y muros colocados en el mapa
def contar_defensas_colocadas():
    cantidad = 0

    for fila in range(TAMANIO_MAPA):
        for columna in range(TAMANIO_MAPA):
            objeto = mapa_juego[fila][columna]

            if isinstance(objeto, Torre) or isinstance(objeto, Muro):
                cantidad += 1

    return cantidad


# Función para contar cuántas unidades tiene colocadas el atacante
# Entradas: ninguna
# Salidas: cantidad de unidades colocadas en el mapa
def contar_unidades_colocadas():
    cantidad = 0

    for fila in range(TAMANIO_MAPA):
        for columna in range(TAMANIO_MAPA):
            objeto = mapa_juego[fila][columna]

            if isinstance(objeto, Unidad):
                cantidad += 1

    return cantidad

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
    global combate_en_progreso
    global turno_combate_actual
    global efectos_combate_pendientes

    mapa_juego, base_central_actual = crear_mapa_inicial()

    dinero_defensor = DINERO_INICIAL_DEFENSOR
    dinero_atacante = DINERO_INICIAL_ATACANTE
    combate_en_progreso = False
    turno_combate_actual = 1
    numero_ronda = 1
    rondas_ganadas_defensor = 0
    rondas_ganadas_atacante = 0
    partida_terminada = False
    efectos_combate_pendientes = []
    limpiar_efectos_combate()
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
turno_combate_actual = 1
combate_en_progreso = False
VELOCIDAD_ANIMACION_COMBATE = 1000
efectos_combate_pendientes = []
DURACION_EFECTO_DISPARO = 900

etiqueta_estado = None
etiqueta_mensaje = None
etiqueta_info_defensor = None
etiqueta_info_atacante = None

boton_siguiente_ronda = None
boton_reiniciar_ronda = None
boton_salir = None
ventana_juego_actual = None

boton_vender_defensor = None
boton_vender_atacante = None

botones_defensor = []
botones_atacante = []

# -------------------------
# Interfaz gráfica del mapa
# -------------------------

botones_mapa = []
canvas_mapa = None
TAMANIO_CASILLA = 58
MARGEN_DIBUJO = 6

# Función para obtener el texto visual de una casilla
# Entradas: objeto guardado en una casilla
# Salidas: texto decorado que se mostrará en el botón
def obtener_texto_casilla(objeto):
    if objeto is None:
        return ""

    if isinstance(objeto, BaseCentral):
        return f"🏰\nBASE\n{objeto.vida}HP"

    if isinstance(objeto, Muro):
        return f"🧱\nMURO\n{objeto.vida}HP"

    if isinstance(objeto, Torre):
        if objeto.nombre == "Torre Básica":
            return f"🏹\nBÁSICA\n{objeto.vida}HP"

        elif objeto.nombre == "Torre Pesada":
            return f"🛡\nPESADA\n{objeto.vida}HP"

        elif objeto.nombre == "Torre Mágica":
            return f"🔮\nMÁGICA\n{objeto.vida}HP"

        else:
            return f"🗼\nTORRE\n{objeto.vida}HP"

    if isinstance(objeto, Unidad):
        if objeto.nombre == "Soldado":
            return f"⚔\nSOLDADO\n{objeto.vida}HP"

        elif objeto.nombre == "Tanque":
            return f"🚜\nTANQUE\n{objeto.vida}HP"

        elif objeto.nombre == "Unidad Rápida":
            return f"🏃\nRÁPIDA\n{objeto.vida}HP"

        else:
            return f"👤\nUNIDAD\n{objeto.vida}HP"

    return "?"


# Función para obtener el color visual de una casilla
# Entradas: objeto guardado en una casilla
# Salidas: color de fondo que se usará en el botón
def obtener_color_casilla(objeto):
    if objeto is None:
        return COLOR_CASILLA_VACIA

    if isinstance(objeto, BaseCentral):
        return faccion_defensor_actual.color_base

    if isinstance(objeto, Torre):
        return faccion_defensor_actual.color_torre

    if isinstance(objeto, Muro):
        return "#8E8578"

    if isinstance(objeto, Unidad):
        return faccion_atacante_actual.color_unidad

    return COLOR_CASILLA_VACIA

# Función para cambiar el estado de una lista de botones
# Entradas: lista de botones y estado deseado
# Salidas: ninguna, activa o desactiva los botones
def cambiar_estado_botones(lista_botones, estado):
    for boton in lista_botones:
        if boton is not None:
            boton.config(state=estado)


# Función para obtener el texto del objeto seleccionado actualmente
# Entradas: ninguna
# Salidas: texto con la selección actual del jugador
def obtener_texto_seleccion_actual():
    if modo_venta:
        return "Modo vender/quitar"

    if fase_actual == "defensor" and defensa_seleccionada is not None:
        return f"Defensa: {defensa_seleccionada}"

    if fase_actual == "atacante" and unidad_seleccionada is not None:
        return f"Unidad: {unidad_seleccionada}"

    return "Ninguno"


# Función para actualizar los botones según la fase actual
# Entradas: ninguna
# Salidas: ninguna, activa o desactiva botones según la fase
def actualizar_botones_por_fase():
    if partida_terminada:
        cambiar_estado_botones(botones_defensor, "disabled")
        cambiar_estado_botones(botones_atacante, "disabled")

        if boton_siguiente_ronda is not None:
            boton_siguiente_ronda.config(state="disabled")

        if boton_reiniciar_ronda is not None:
            boton_reiniciar_ronda.config(state="disabled")

        if boton_salir is not None:
            boton_salir.config(state="normal")

        return

    if fase_actual == "defensor":
        cambiar_estado_botones(botones_defensor, "normal")
        cambiar_estado_botones(botones_atacante, "disabled")

        if boton_siguiente_ronda is not None:
            boton_siguiente_ronda.config(state="disabled")

        if boton_reiniciar_ronda is not None:
            boton_reiniciar_ronda.config(state="normal")

    elif fase_actual == "atacante":
        cambiar_estado_botones(botones_defensor, "disabled")
        cambiar_estado_botones(botones_atacante, "normal")

        if boton_siguiente_ronda is not None:
            boton_siguiente_ronda.config(state="disabled")

        if boton_reiniciar_ronda is not None:
            boton_reiniciar_ronda.config(state="normal")

    elif fase_actual == "combate":
        cambiar_estado_botones(botones_defensor, "disabled")
        cambiar_estado_botones(botones_atacante, "disabled")

        if boton_siguiente_ronda is not None:
            boton_siguiente_ronda.config(state="disabled")

        if boton_reiniciar_ronda is not None:
            boton_reiniciar_ronda.config(state="disabled")

    elif fase_actual == "fin_ronda":
        cambiar_estado_botones(botones_defensor, "disabled")
        cambiar_estado_botones(botones_atacante, "disabled")

        if boton_siguiente_ronda is not None:
            boton_siguiente_ronda.config(state="normal")

        if boton_reiniciar_ronda is not None:
            boton_reiniciar_ronda.config(state="disabled")

# Función para crear un botón con estilo visual uniforme
# Entradas: contenedor, texto, comando, ancho y color de fondo
# Salidas: botón creado con estilo
def crear_boton_estilizado(contenedor, texto, comando, ancho=18, color_fondo=COLOR_BOTON):
    boton = tk.Button(
        contenedor,
        text=texto,
        command=comando,
        width=ancho,
        height=2,
        bg=color_fondo,
        fg=COLOR_BOTON_TEXTO,
        activebackground=color_fondo,
        activeforeground=COLOR_BOTON_TEXTO,
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Arial", 10, "bold")
    )
    return boton


# Función para reiniciar la ronda actual sin borrar el marcador
# Entradas: ninguna
# Salidas: ninguna, reinicia el mapa y vuelve a fase defensor
def reiniciar_ronda_actual():
    global mapa_juego
    global base_central_actual
    global dinero_defensor
    global dinero_atacante
    global fase_actual
    global defensa_seleccionada
    global unidad_seleccionada
    global modo_venta
    global combate_en_progreso
    global turno_combate_actual
    global efectos_combate_pendientes


    if partida_terminada:
        etiqueta_mensaje.config(text="La partida ya terminó. No se puede reiniciar la ronda.")
        return

    mapa_juego, base_central_actual = crear_mapa_inicial()

    dinero_defensor = DINERO_INICIAL_DEFENSOR + ((numero_ronda - 1) * BONO_DINERO_POR_RONDA)
    dinero_atacante = DINERO_INICIAL_ATACANTE + ((numero_ronda - 1) * BONO_DINERO_POR_RONDA)

    combate_en_progreso = False
    turno_combate_actual = 1
    efectos_combate_pendientes = []
    limpiar_efectos_combate()

    fase_actual = "defensor"
    defensa_seleccionada = None
    unidad_seleccionada = None
    modo_venta = False

    etiqueta_mensaje.config(text=f"La ronda {numero_ronda} fue reiniciada.")
    actualizar_mapa_visual()

# Función para cerrar la partida actual y volver a selección de facciones
# Entradas: ventana emergente de resultado
# Salidas: ninguna, reinicia referencias visuales y abre selección de facciones
def jugar_otra_partida(ventana_resultado):
    global ventana_juego_actual
    global etiqueta_estado
    global etiqueta_mensaje
    global etiqueta_info_defensor
    global etiqueta_info_atacante
    global boton_siguiente_ronda
    global boton_reiniciar_ronda
    global boton_salir
    global botones_defensor
    global botones_atacante
    global botones_mapa
    global canvas_mapa
    global efectos_combate_pendientes
    global combate_en_progreso
    global turno_combate_actual
    global boton_vender_defensor
    global boton_vender_atacante

    boton_vender_defensor = None
    boton_vender_atacante = None

    if ventana_resultado is not None:
        ventana_resultado.destroy()

    if ventana_juego_actual is not None:
        ventana_juego_actual.destroy()

    ventana_juego_actual = None
    canvas_mapa = None
    efectos_combate_pendientes = []
    combate_en_progreso = False
    turno_combate_actual = 1
    etiqueta_estado = None
    etiqueta_mensaje = None
    etiqueta_info_defensor = None
    etiqueta_info_atacante = None

    boton_siguiente_ronda = None
    boton_reiniciar_ronda = None
    boton_salir = None

    botones_defensor = []
    botones_atacante = []
    botones_mapa = []

    reiniciar_estado_partida()
    abrir_ventana_seleccion_facciones(
    NOMBRE_JUGADOR_DEFENSOR,
    NOMBRE_JUGADOR_ATACANTE
)


# Función para mostrar una ventana bonita con el resultado final de la partida
# Entradas: ganador de la partida y mensaje principal
# Salidas: ninguna, muestra una ventana emergente final
def mostrar_resultado_partida(ganador, mensaje_resultado):
    ventana_resultado = tk.Toplevel(ventana_juego_actual)
    ventana_resultado.title("Resultado final")
    ventana_resultado.geometry("540x360")
    ventana_resultado.resizable(False, False)
    ventana_resultado.config(bg=COLOR_FONDO_APP)
    ventana_resultado.grab_set()

    if ganador == "defensor":
        titulo_resultado = "El Defensor ganó la partida"
    elif ganador == "atacante":
        titulo_resultado = "El Atacante ganó la partida"
    else:
        titulo_resultado = "Partida finalizada"

    titulo = tk.Label(
        ventana_resultado,
        text=titulo_resultado,
        font=("Arial", 20, "bold"),
        bg=COLOR_FONDO_APP,
        fg=COLOR_TITULO
    )
    titulo.pack(pady=(25, 10))

    texto_resultado = tk.Label(
        ventana_resultado,
        text=mensaje_resultado,
        font=("Arial", 12),
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO,
        wraplength=450,
        justify="center",
        padx=20,
        pady=20,
        relief="solid",
        bd=1
    )
    texto_resultado.pack(pady=10, padx=30, fill="x")

    instruccion = tk.Label(
        ventana_resultado,
        text="La partida terminó.\nPuedes jugar otra partida para volver a seleccionar facciones e iniciar desde cero.",
        font=("Arial", 10),
        bg=COLOR_FONDO_APP,
        fg=COLOR_TEXTO,
        justify="center"
    )
    instruccion.pack(pady=8)

    frame_botones = tk.Frame(
        ventana_resultado,
        bg=COLOR_FONDO_APP
    )
    frame_botones.pack(pady=15)

    boton_cerrar = crear_boton_estilizado(
        frame_botones,
        "Cerrar",
        ventana_resultado.destroy,
        ancho=15,
        color_fondo=COLOR_BOTON_SECUNDARIO
    )
    boton_cerrar.grid(row=0, column=0, padx=8)

    boton_nueva_partida = crear_boton_estilizado(
        frame_botones,
        "Jugar otra partida",
        lambda: jugar_otra_partida(ventana_resultado),
        ancho=18,
        color_fondo=COLOR_BOTON
    )
    boton_nueva_partida.grid(row=0, column=1, padx=8)


# Función para cerrar la ventana del juego actual
# Entradas: ninguna
# Salidas: ninguna, cierra la ventana principal del juego
def salir_del_juego():
    if ventana_juego_actual is not None:
        ventana_juego_actual.destroy()


# Función para actualizar el texto de estado de la partida
# Entradas: ninguna
# Salidas: ninguna, actualiza etiquetas de estado e información
def actualizar_estado_visual():
    if etiqueta_estado is not None:
        seleccion_actual = obtener_texto_seleccion_actual()

        etiqueta_estado.config(
            text=f"Ronda: {numero_ronda}   |   Fase: {fase_actual.upper()}   |   "
                 f"Marcador: Defensor {rondas_ganadas_defensor} - Atacante {rondas_ganadas_atacante}\n"
                 f"Vida base: {base_central_actual.vida}   |   Seleccionado: {seleccion_actual}",
            bg=COLOR_ESTADO,
            fg=COLOR_TEXTO
        )

    if etiqueta_info_defensor is not None:
        etiqueta_info_defensor.config(
            text=f"Jugador: {NOMBRE_JUGADOR_DEFENSOR}\n"
                 f"Facción: {faccion_defensor_actual.nombre}\n"
                 f"Dinero: ${dinero_defensor}\n"
                 f"Defensas colocadas: {contar_defensas_colocadas()}",
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO
        )

    if etiqueta_info_atacante is not None:
        etiqueta_info_atacante.config(
            text=f"Jugador: {NOMBRE_JUGADOR_ATACANTE}\n"
                 f"Facción: {faccion_atacante_actual.nombre}\n"
                 f"Dinero: ${dinero_atacante}\n"
                 f"Unidades colocadas: {contar_unidades_colocadas()}",
            bg=COLOR_PANEL,
            fg=COLOR_TEXTO
        )

    actualizar_botones_por_fase()



# Función para obtener el color del texto de una casilla
# Entradas: objeto guardado en una casilla
# Salidas: color del texto que se mostrará en el botón
def obtener_color_texto_casilla(objeto):
    color_fondo = obtener_color_casilla(objeto)

    if color_es_oscuro(color_fondo):
        return COLOR_TEXTO_CLARO

    return COLOR_TEXTO_OSCURO

# Función para revisar si un color hexadecimal es oscuro
# Entradas: color hexadecimal
# Salidas: True si el color es oscuro, False si es claro
def color_es_oscuro(color_hex):
    if not isinstance(color_hex, str):
        return False

    if not color_hex.startswith("#"):
        return False

    if len(color_hex) != 7:
        return False

    rojo = int(color_hex[1:3], 16)
    verde = int(color_hex[3:5], 16)
    azul = int(color_hex[5:7], 16)

    brillo = (rojo * 299 + verde * 587 + azul * 114) / 1000

    return brillo < 130


# Función para obtener el color del texto de una casilla
# Entradas: objeto guardado en una casilla
# Salidas: color del texto que se mostrará en el botón
def obtener_color_texto_casilla(objeto):
    color_fondo = obtener_color_casilla(objeto)

    if color_es_oscuro(color_fondo):
        return COLOR_TEXTO_CLARO

    return COLOR_TEXTO_OSCURO


# Función para obtener coordenadas visuales de una casilla
# Entradas: fila y columna de la matriz
# Salidas: coordenadas x1, y1, x2, y2 para dibujar en Canvas
def obtener_coordenadas_casilla(fila, columna):
    x1 = columna * TAMANIO_CASILLA
    y1 = fila * TAMANIO_CASILLA
    x2 = x1 + TAMANIO_CASILLA
    y2 = y1 + TAMANIO_CASILLA

    return x1, y1, x2, y2

# Función para obtener el centro visual de una casilla
# Entradas: fila y columna de la casilla
# Salidas: coordenadas x, y del centro de la casilla
def obtener_centro_casilla(fila, columna):
    x1, y1, x2, y2 = obtener_coordenadas_casilla(fila, columna)

    centro_x = (x1 + x2) // 2
    centro_y = (y1 + y2) // 2

    return centro_x, centro_y


# Función para guardar un efecto visual de disparo de torre
# Entradas: posición de torre, posición de objetivo y nombre de torre
# Salidas: ninguna, agrega el efecto a la lista pendiente
def agregar_efecto_disparo_torre(fila_torre, columna_torre, fila_objetivo, columna_objetivo, nombre_torre):
    efecto = {
        "tipo": "disparo_torre",
        "fila_torre": fila_torre,
        "columna_torre": columna_torre,
        "fila_objetivo": fila_objetivo,
        "columna_objetivo": columna_objetivo,
        "nombre_torre": nombre_torre
    }

    efectos_combate_pendientes.append(efecto)

# Función para dibujar un efecto de ataque de unidad
# Entradas: datos del efecto de ataque
# Salidas: ninguna, dibuja una marca de impacto sobre el objetivo
def dibujar_efecto_ataque_unidad(efecto):
    fila_unidad = efecto["fila_unidad"]
    columna_unidad = efecto["columna_unidad"]
    fila_objetivo = efecto["fila_objetivo"]
    columna_objetivo = efecto["columna_objetivo"]
    nombre_unidad = efecto["nombre_unidad"]
    objetivo_original = efecto["objetivo"]

    if not posicion_en_rango(fila_objetivo, columna_objetivo):
        return

    objetivo_actual = mapa_juego[fila_objetivo][columna_objetivo]

    if objetivo_actual is not objetivo_original:
        return
    
    x_inicio, y_inicio = obtener_centro_casilla(fila_unidad, columna_unidad)
    x_fin, y_fin = obtener_centro_casilla(fila_objetivo, columna_objetivo)

    color_efecto = "#C0392B"
    grosor_efecto = 3

    if nombre_unidad == "Tanque":
        color_efecto = "#2F2A24"
        grosor_efecto = 5

    elif nombre_unidad == "Unidad Rápida":
        color_efecto = "#D98C24"
        grosor_efecto = 3

    canvas_mapa.create_line(
        x_inicio,
        y_inicio,
        x_fin,
        y_fin,
        fill=color_efecto,
        width=grosor_efecto,
        tags="efecto_combate"
    )

    canvas_mapa.create_line(
        x_fin - 10,
        y_fin - 10,
        x_fin + 10,
        y_fin + 10,
        fill=color_efecto,
        width=grosor_efecto,
        tags="efecto_combate"
    )

    canvas_mapa.create_line(
        x_fin + 10,
        y_fin - 10,
        x_fin - 10,
        y_fin + 10,
        fill=color_efecto,
        width=grosor_efecto,
        tags="efecto_combate"
    )

    canvas_mapa.create_oval(
        x_fin - 13,
        y_fin - 13,
        x_fin + 13,
        y_fin + 13,
        outline=color_efecto,
        width=2,
        tags="efecto_combate"
    )


# Función para dibujar un efecto visual de habilidad
# Entradas: datos del efecto de habilidad
# Salidas: ninguna, dibuja el efecto sobre la casilla
def dibujar_efecto_habilidad(efecto):
    tipo_habilidad = efecto["tipo_habilidad"]
    fila = efecto["fila"]
    columna = efecto["columna"]

    x, y = obtener_centro_casilla(fila, columna)

    if tipo_habilidad == "congelar":
        canvas_mapa.create_oval(
            x - 20,
            y - 20,
            x + 20,
            y + 20,
            outline="#4DB6E2",
            width=4,
            tags="efecto_combate"
        )

        canvas_mapa.create_text(
            x,
            y,
            text="❄",
            font=("Arial", 22, "bold"),
            fill="#4DB6E2",
            tags="efecto_combate"
        )

    elif tipo_habilidad == "escudo":
        canvas_mapa.create_oval(
            x - 23,
            y - 23,
            x + 23,
            y + 23,
            outline="#3498DB",
            width=4,
            tags="efecto_combate"
        )

        canvas_mapa.create_text(
            x,
            y,
            text="🛡",
            font=("Arial", 18, "bold"),
            fill="#3498DB",
            tags="efecto_combate"
        )

    elif tipo_habilidad == "velocidad":
        canvas_mapa.create_line(
            x - 24,
            y - 12,
            x + 10,
            y - 12,
            fill="#F39C12",
            width=3,
            tags="efecto_combate"
        )

        canvas_mapa.create_line(
            x - 28,
            y,
            x + 14,
            y,
            fill="#F39C12",
            width=3,
            tags="efecto_combate"
        )

        canvas_mapa.create_line(
            x - 24,
            y + 12,
            x + 10,
            y + 12,
            fill="#F39C12",
            width=3,
            tags="efecto_combate"
        )

    elif tipo_habilidad == "ataque_doble":
        canvas_mapa.create_text(
            x,
            y - 10,
            text="x2",
            font=("Arial", 18, "bold"),
            fill="#C0392B",
            tags="efecto_combate"
        )

        canvas_mapa.create_oval(
            x - 18,
            y - 18,
            x + 18,
            y + 18,
            outline="#C0392B",
            width=3,
            tags="efecto_combate"
        )

# Función para guardar un efecto visual de ataque de unidad
# Entradas: posición de unidad, posición del objetivo, nombre de unidad y objetivo atacado
# Salidas: ninguna, agrega el efecto a la lista pendiente
def agregar_efecto_ataque_unidad(fila_unidad, columna_unidad, fila_objetivo, columna_objetivo, nombre_unidad, objetivo):
    efecto = {
        "tipo": "ataque_unidad",
        "fila_unidad": fila_unidad,
        "columna_unidad": columna_unidad,
        "fila_objetivo": fila_objetivo,
        "columna_objetivo": columna_objetivo,
        "nombre_unidad": nombre_unidad,
        "objetivo": objetivo
    }

    efectos_combate_pendientes.append(efecto)

# Función para guardar un efecto visual de habilidad
# Entradas: tipo de habilidad, fila y columna del objetivo
# Salidas: ninguna, agrega el efecto a la lista pendiente
def agregar_efecto_habilidad(tipo_habilidad, fila, columna):
    efecto = {
        "tipo": "habilidad",
        "tipo_habilidad": tipo_habilidad,
        "fila": fila,
        "columna": columna
    }

    efectos_combate_pendientes.append(efecto)

# Función para guardar un efecto visual ligado a una unidad
# Entradas: tipo de habilidad y objeto unidad
# Salidas: ninguna, agrega el efecto para dibujarlo en la posición actual de la unidad
def agregar_efecto_habilidad_unidad(tipo_habilidad, unidad):
    efecto = {
        "tipo": "habilidad_unidad",
        "tipo_habilidad": tipo_habilidad,
        "unidad": unidad
    }

    efectos_combate_pendientes.append(efecto)

# Función para dibujar una habilidad sobre la posición actual de una unidad
# Entradas: datos del efecto con referencia a la unidad
# Salidas: ninguna, dibuja el efecto si la unidad sigue viva en el mapa
def dibujar_efecto_habilidad_unidad(efecto):
    unidad = efecto["unidad"]
    tipo_habilidad = efecto["tipo_habilidad"]

    posicion_unidad = buscar_posicion_unidad_objeto(unidad)

    if posicion_unidad is None:
        return

    fila_unidad, columna_unidad = posicion_unidad

    efecto_actualizado = {
        "tipo_habilidad": tipo_habilidad,
        "fila": fila_unidad,
        "columna": columna_unidad
    }

    dibujar_efecto_habilidad(efecto_actualizado)


# Función para limpiar los efectos visuales del combate
# Entradas: ninguna
# Salidas: ninguna, elimina efectos si el Canvas existe
def limpiar_efectos_combate():
    global canvas_mapa

    if canvas_mapa is None:
        return

    try:
        if canvas_mapa.winfo_exists():
            canvas_mapa.delete("efecto_combate")

    except tk.TclError:
        canvas_mapa = None


# Función para dibujar un efecto de disparo según el tipo de torre
# Entradas: datos del efecto de disparo
# Salidas: ninguna, dibuja línea y golpe visual
def dibujar_efecto_disparo_torre(efecto):
    fila_torre = efecto["fila_torre"]
    columna_torre = efecto["columna_torre"]
    fila_objetivo = efecto["fila_objetivo"]
    columna_objetivo = efecto["columna_objetivo"]
    nombre_torre = efecto["nombre_torre"]

    x_inicio, y_inicio = obtener_centro_casilla(fila_torre, columna_torre)
    x_fin, y_fin = obtener_centro_casilla(fila_objetivo, columna_objetivo)

    color_disparo = "#7A3E2B"
    grosor_disparo = 3
    estilo_linea = None

    if nombre_torre == "Torre Pesada":
        color_disparo = "#2F2A24"
        grosor_disparo = 5

    elif nombre_torre == "Torre Mágica":
        color_disparo = "#8A4FFF"
        grosor_disparo = 4
        estilo_linea = (4, 2)

    canvas_mapa.create_line(
        x_inicio,
        y_inicio,
        x_fin,
        y_fin,
        fill=color_disparo,
        width=grosor_disparo,
        dash=estilo_linea,
        tags="efecto_combate"
    )

    canvas_mapa.create_oval(
        x_fin - 9,
        y_fin - 9,
        x_fin + 9,
        y_fin + 9,
        outline=color_disparo,
        width=3,
        tags="efecto_combate"
    )

    canvas_mapa.create_oval(
        x_fin - 4,
        y_fin - 4,
        x_fin + 4,
        y_fin + 4,
        fill=color_disparo,
        outline=color_disparo,
        tags="efecto_combate"
    )


# Función para dibujar todos los efectos visuales pendientes del combate
# Entradas: ninguna
# Salidas: ninguna, dibuja efectos y los limpia después de un tiempo
def dibujar_efectos_combate_pendientes():
    global efectos_combate_pendientes

    if canvas_mapa is None:
        efectos_combate_pendientes = []
        return

    limpiar_efectos_combate()

    for efecto in efectos_combate_pendientes:
        if efecto["tipo"] == "disparo_torre":
            dibujar_efecto_disparo_torre(efecto)

        elif efecto["tipo"] == "ataque_unidad":
            dibujar_efecto_ataque_unidad(efecto)

        elif efecto["tipo"] == "habilidad":
            dibujar_efecto_habilidad(efecto)

        elif efecto["tipo"] == "habilidad_unidad":
            dibujar_efecto_habilidad_unidad(efecto)

    efectos_combate_pendientes = []

    if ventana_juego_actual is not None:
        ventana_juego_actual.after(DURACION_EFECTO_DISPARO, limpiar_efectos_combate)

# Función para obtener el identificador visual de una casilla
# Entradas: fila y columna de la matriz
# Salidas: texto usado como tag dentro del Canvas
def obtener_tag_casilla(fila, columna):
    return f"casilla_{fila}_{columna}"


# Función para dibujar una casilla vacía del mapa
# Entradas: fila y columna de la casilla
# Salidas: ninguna, dibuja el fondo y borde de la casilla
def dibujar_casilla_canvas(fila, columna):
    tag_casilla = obtener_tag_casilla(fila, columna)
    x1, y1, x2, y2 = obtener_coordenadas_casilla(fila, columna)

    if (fila + columna) % 2 == 0:
        color_fondo = "#F4EFE6"
    else:
        color_fondo = "#EFE7DA"

    canvas_mapa.create_rectangle(
        x1,
        y1,
        x2,
        y2,
        fill=color_fondo,
        outline=COLOR_CASILLA_BORDE,
        width=1,
        tags=tag_casilla
    )


# Función para obtener la vida máxima de un objeto del juego
# Entradas: objeto del mapa
# Salidas: vida máxima registrada del objeto
def obtener_vida_maxima_objeto(objeto):
    if hasattr(objeto, "vida_maxima"):
        return objeto.vida_maxima

    objeto.vida_maxima = objeto.vida
    return objeto.vida_maxima


# Función para dibujar una barra de vida en una casilla
# Entradas: objeto del juego, coordenadas de casilla y tag visual
# Salidas: ninguna, dibuja barra de vida en Canvas
def dibujar_vida_canvas(objeto, x1, y1, x2, y2, tag_casilla):
    vida_maxima = obtener_vida_maxima_objeto(objeto)

    if vida_maxima <= 0:
        return

    porcentaje_vida = objeto.vida / vida_maxima
    porcentaje_vida = max(0, min(1, porcentaje_vida))

    ancho_total = (x2 - x1) - 14
    ancho_vida = ancho_total * porcentaje_vida

    color_vida = "#2ECC71"

    if porcentaje_vida <= 0.5:
        color_vida = "#F1C40F"

    if porcentaje_vida <= 0.25:
        color_vida = "#E74C3C"

    y_barra_1 = y2 - 9
    y_barra_2 = y2 - 4

    canvas_mapa.create_rectangle(
        x1 + 7,
        y_barra_1,
        x2 - 7,
        y_barra_2,
        fill="#D9D1C2",
        outline=COLOR_TEXTO_OSCURO,
        width=1,
        tags=tag_casilla
    )

    if ancho_vida > 0:
        canvas_mapa.create_rectangle(
            x1 + 7,
            y_barra_1,
            x1 + 7 + ancho_vida,
            y_barra_2,
            fill=color_vida,
            outline="",
            tags=tag_casilla
        )

    canvas_mapa.create_text(
        (x1 + x2) // 2,
        y2 - 14,
        text=str(objeto.vida),
        font=("Arial", 6, "bold"),
        fill=COLOR_TEXTO_OSCURO,
        tags=tag_casilla
    )


# Función para dibujar la base central
# Entradas: objeto base, fila y columna
# Salidas: ninguna, dibuja la base como castillo
def dibujar_base_canvas(objeto, fila, columna):
    tag_casilla = obtener_tag_casilla(fila, columna)
    x1, y1, x2, y2 = obtener_coordenadas_casilla(fila, columna)
    color_base = faccion_defensor_actual.color_base

    canvas_mapa.create_rectangle(
        x1 + 14,
        y1 + 26,
        x2 - 14,
        y2 - 18,
        fill=color_base,
        outline=COLOR_TEXTO_OSCURO,
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_rectangle(
        x1 + 16,
        y1 + 16,
        x1 + 26,
        y1 + 30,
        fill=color_base,
        outline=COLOR_TEXTO_OSCURO,
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_rectangle(
        x1 + 34,
        y1 + 16,
        x1 + 44,
        y1 + 30,
        fill=color_base,
        outline=COLOR_TEXTO_OSCURO,
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_rectangle(
        x2 - 26,
        y1 + 16,
        x2 - 16,
        y1 + 30,
        fill=color_base,
        outline=COLOR_TEXTO_OSCURO,
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_rectangle(
        x1 + 27,
        y1 + 38,
        x2 - 27,
        y2 - 18,
        fill="#5A3E2B",
        outline=COLOR_TEXTO_OSCURO,
        width=1,
        tags=tag_casilla
    )

    canvas_mapa.create_text(
        (x1 + x2) // 2,
        y1 + 8,
        text="BASE",
        font=("Arial", 7, "bold"),
        fill=COLOR_TEXTO_OSCURO,
        tags=tag_casilla
    )

    dibujar_vida_canvas(objeto, x1, y1, x2, y2, tag_casilla)


# Función para dibujar un muro
# Entradas: objeto muro, fila y columna
# Salidas: ninguna, dibuja el muro con bloques
def dibujar_muro_canvas(objeto, fila, columna):
    tag_casilla = obtener_tag_casilla(fila, columna)
    x1, y1, x2, y2 = obtener_coordenadas_casilla(fila, columna)

    canvas_mapa.create_rectangle(
        x1 + 10,
        y1 + 18,
        x2 - 10,
        y2 - 20,
        fill="#8E8578",
        outline=COLOR_TEXTO_OSCURO,
        width=2,
        tags=tag_casilla
    )

    for i in range(3):
        y_linea = y1 + 25 + (i * 10)
        canvas_mapa.create_line(
            x1 + 10,
            y_linea,
            x2 - 10,
            y_linea,
            fill=COLOR_TEXTO_OSCURO,
            width=1,
            tags=tag_casilla
        )

    canvas_mapa.create_line(
        x1 + 28,
        y1 + 18,
        x1 + 28,
        y2 - 20,
        fill=COLOR_TEXTO_OSCURO,
        width=1,
        tags=tag_casilla
    )

    canvas_mapa.create_line(
        x1 + 44,
        y1 + 18,
        x1 + 44,
        y2 - 20,
        fill=COLOR_TEXTO_OSCURO,
        width=1,
        tags=tag_casilla
    )

    canvas_mapa.create_text(
        (x1 + x2) // 2,
        y1 + 9,
        text="MURO",
        font=("Arial", 7, "bold"),
        fill=COLOR_TEXTO_OSCURO,
        tags=tag_casilla
    )

    dibujar_vida_canvas(objeto, x1, y1, x2, y2, tag_casilla)


# Función para dibujar una torre básica
# Entradas: objeto torre, fila y columna
# Salidas: ninguna, dibuja la torre básica
def dibujar_torre_basica_canvas(objeto, fila, columna):
    tag_casilla = obtener_tag_casilla(fila, columna)
    x1, y1, x2, y2 = obtener_coordenadas_casilla(fila, columna)
    color_torre = faccion_defensor_actual.color_torre

    canvas_mapa.create_polygon(
        x1 + 18,
        y1 + 25,
        (x1 + x2) // 2,
        y1 + 10,
        x2 - 18,
        y1 + 25,
        fill="#7A3E2B",
        outline=COLOR_TEXTO_OSCURO,
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_rectangle(
        x1 + 22,
        y1 + 25,
        x2 - 22,
        y2 - 19,
        fill=color_torre,
        outline=COLOR_TEXTO_OSCURO,
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_oval(
        x1 + 29,
        y1 + 33,
        x2 - 29,
        y1 + 44,
        fill="#F8F5F0",
        outline=COLOR_TEXTO_OSCURO,
        width=1,
        tags=tag_casilla
    )

    canvas_mapa.create_text(
        (x1 + x2) // 2,
        y1 + 8,
        text="BÁSICA",
        font=("Arial", 7, "bold"),
        fill=COLOR_TEXTO_OSCURO,
        tags=tag_casilla
    )

    dibujar_vida_canvas(objeto, x1, y1, x2, y2, tag_casilla)


# Función para dibujar una torre pesada
# Entradas: objeto torre, fila y columna
# Salidas: ninguna, dibuja la torre pesada
def dibujar_torre_pesada_canvas(objeto, fila, columna):
    tag_casilla = obtener_tag_casilla(fila, columna)
    x1, y1, x2, y2 = obtener_coordenadas_casilla(fila, columna)
    color_torre = faccion_defensor_actual.color_torre

    canvas_mapa.create_rectangle(
        x1 + 17,
        y1 + 17,
        x2 - 17,
        y2 - 19,
        fill=color_torre,
        outline=COLOR_TEXTO_OSCURO,
        width=3,
        tags=tag_casilla
    )

    canvas_mapa.create_rectangle(
        x1 + 22,
        y1 + 10,
        x2 - 22,
        y1 + 22,
        fill="#5A4A3A",
        outline=COLOR_TEXTO_OSCURO,
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_oval(
        x1 + 25,
        y1 + 29,
        x2 - 25,
        y1 + 47,
        fill="#D9D1C2",
        outline=COLOR_TEXTO_OSCURO,
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_text(
        (x1 + x2) // 2,
        y1 + 8,
        text="PESADA",
        font=("Arial", 7, "bold"),
        fill=COLOR_TEXTO_OSCURO,
        tags=tag_casilla
    )

    dibujar_vida_canvas(objeto, x1, y1, x2, y2, tag_casilla)


# Función para dibujar una torre mágica
# Entradas: objeto torre, fila y columna
# Salidas: ninguna, dibuja la torre mágica
def dibujar_torre_magica_canvas(objeto, fila, columna):
    tag_casilla = obtener_tag_casilla(fila, columna)
    x1, y1, x2, y2 = obtener_coordenadas_casilla(fila, columna)
    color_torre = faccion_defensor_actual.color_torre

    canvas_mapa.create_rectangle(
        x1 + 24,
        y1 + 24,
        x2 - 24,
        y2 - 19,
        fill=color_torre,
        outline=COLOR_TEXTO_OSCURO,
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_polygon(
        (x1 + x2) // 2,
        y1 + 8,
        x1 + 20,
        y1 + 26,
        (x1 + x2) // 2,
        y1 + 44,
        x2 - 20,
        y1 + 26,
        fill="#8A4FFF",
        outline=COLOR_TEXTO_OSCURO,
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_text(
        (x1 + x2) // 2,
        y1 + 8,
        text="✦",
        font=("Arial", 9, "bold"),
        fill="#F8F5F0",
        tags=tag_casilla
    )

    canvas_mapa.create_text(
        (x1 + x2) // 2,
        y1 + 51,
        text="MÁGICA",
        font=("Arial", 7, "bold"),
        fill=COLOR_TEXTO_OSCURO,
        tags=tag_casilla
    )

    dibujar_vida_canvas(objeto, x1, y1, x2, y2, tag_casilla)


# Función para dibujar una unidad soldado con diseño más detallado
# Entradas: objeto unidad, fila y columna
# Salidas: ninguna, dibuja el soldado con armadura, escudo y espada
def dibujar_soldado_canvas(objeto, fila, columna):
    tag_casilla = obtener_tag_casilla(fila, columna)
    x1, y1, x2, y2 = obtener_coordenadas_casilla(fila, columna)
    color_unidad = faccion_atacante_actual.color_unidad

    centro_x = (x1 + x2) // 2

    canvas_mapa.create_oval(
        x1 + 18,
        y1 + 42,
        x2 - 18,
        y1 + 48,
        fill="#B8A98F",
        outline="",
        tags=tag_casilla
    )

    canvas_mapa.create_polygon(
        centro_x - 9,
        y1 + 20,
        centro_x + 9,
        y1 + 20,
        centro_x + 14,
        y1 + 39,
        centro_x,
        y1 + 46,
        centro_x - 14,
        y1 + 39,
        fill=color_unidad,
        outline=COLOR_TEXTO_OSCURO,
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_rectangle(
        centro_x - 8,
        y1 + 23,
        centro_x + 8,
        y1 + 27,
        fill="#D9D1C2",
        outline=COLOR_TEXTO_OSCURO,
        width=1,
        tags=tag_casilla
    )

    canvas_mapa.create_oval(
        centro_x - 9,
        y1 + 8,
        centro_x + 9,
        y1 + 24,
        fill="#D9D1C2",
        outline=COLOR_TEXTO_OSCURO,
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_arc(
        centro_x - 11,
        y1 + 5,
        centro_x + 11,
        y1 + 23,
        start=0,
        extent=180,
        fill="#5A4A3A",
        outline=COLOR_TEXTO_OSCURO,
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_line(
        centro_x - 5,
        y1 + 15,
        centro_x - 2,
        y1 + 15,
        fill=COLOR_TEXTO_OSCURO,
        width=1,
        tags=tag_casilla
    )

    canvas_mapa.create_line(
        centro_x + 2,
        y1 + 15,
        centro_x + 5,
        y1 + 15,
        fill=COLOR_TEXTO_OSCURO,
        width=1,
        tags=tag_casilla
    )

    canvas_mapa.create_polygon(
        centro_x - 17,
        y1 + 24,
        centro_x - 27,
        y1 + 28,
        centro_x - 24,
        y1 + 43,
        centro_x - 14,
        y1 + 39,
        fill="#C0C0C0",
        outline=COLOR_TEXTO_OSCURO,
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_line(
        centro_x + 12,
        y1 + 24,
        centro_x + 27,
        y1 + 12,
        fill="#C0C0C0",
        width=4,
        tags=tag_casilla
    )

    canvas_mapa.create_line(
        centro_x + 14,
        y1 + 24,
        centro_x + 29,
        y1 + 12,
        fill=COLOR_TEXTO_OSCURO,
        width=1,
        tags=tag_casilla
    )

    canvas_mapa.create_polygon(
        centro_x + 27,
        y1 + 12,
        centro_x + 31,
        y1 + 5,
        centro_x + 23,
        y1 + 9,
        fill="#EDE7DD",
        outline=COLOR_TEXTO_OSCURO,
        width=1,
        tags=tag_casilla
    )

    canvas_mapa.create_line(
        centro_x - 6,
        y1 + 45,
        centro_x - 13,
        y1 + 52,
        fill=COLOR_TEXTO_OSCURO,
        width=3,
        tags=tag_casilla
    )

    canvas_mapa.create_line(
        centro_x + 6,
        y1 + 45,
        centro_x + 13,
        y1 + 52,
        fill=COLOR_TEXTO_OSCURO,
        width=3,
        tags=tag_casilla
    )

    dibujar_vida_canvas(objeto, x1, y1, x2, y2, tag_casilla)


# Función para dibujar una unidad tanque
# Entradas: objeto unidad, fila y columna
# Salidas: ninguna, dibuja el tanque
def dibujar_tanque_canvas(objeto, fila, columna):
    tag_casilla = obtener_tag_casilla(fila, columna)
    x1, y1, x2, y2 = obtener_coordenadas_casilla(fila, columna)
    color_unidad = faccion_atacante_actual.color_unidad

    canvas_mapa.create_rectangle(
        x1 + 13,
        y1 + 30,
        x2 - 13,
        y1 + 45,
        fill="#3D3D3D",
        outline=COLOR_TEXTO_OSCURO,
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_rectangle(
        x1 + 19,
        y1 + 20,
        x2 - 22,
        y1 + 35,
        fill=color_unidad,
        outline=COLOR_TEXTO_OSCURO,
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_line(
        x2 - 23,
        y1 + 26,
        x2 - 8,
        y1 + 21,
        fill=COLOR_TEXTO_OSCURO,
        width=4,
        tags=tag_casilla
    )

    canvas_mapa.create_oval(
        x1 + 17,
        y1 + 38,
        x1 + 25,
        y1 + 46,
        fill="#1F1F1F",
        tags=tag_casilla
    )

    canvas_mapa.create_oval(
        x2 - 25,
        y1 + 38,
        x2 - 17,
        y1 + 46,
        fill="#1F1F1F",
        tags=tag_casilla
    )

    canvas_mapa.create_text(
        (x1 + x2) // 2,
        y1 + 53,
        text="TANQUE",
        font=("Arial", 7, "bold"),
        fill=COLOR_TEXTO_OSCURO,
        tags=tag_casilla
    )

    dibujar_vida_canvas(objeto, x1, y1, x2, y2, tag_casilla)


# Función para dibujar una unidad rápida con diseño dinámico
# Entradas: objeto unidad, fila y columna
# Salidas: ninguna, dibuja la unidad rápida en pose de movimiento
def dibujar_unidad_rapida_canvas(objeto, fila, columna):
    tag_casilla = obtener_tag_casilla(fila, columna)
    x1, y1, x2, y2 = obtener_coordenadas_casilla(fila, columna)
    color_unidad = faccion_atacante_actual.color_unidad

    centro_x = (x1 + x2) // 2

    canvas_mapa.create_oval(
        x1 + 14,
        y1 + 43,
        x2 - 12,
        y1 + 49,
        fill="#B8A98F",
        outline="",
        tags=tag_casilla
    )

    canvas_mapa.create_line(
        x1 + 5,
        y1 + 13,
        x1 + 24,
        y1 + 13,
        fill="#A78A6A",
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_line(
        x1 + 3,
        y1 + 24,
        x1 + 24,
        y1 + 24,
        fill="#A78A6A",
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_line(
        x1 + 7,
        y1 + 35,
        x1 + 25,
        y1 + 35,
        fill="#A78A6A",
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_polygon(
        centro_x - 5,
        y1 + 22,
        centro_x - 23,
        y1 + 31,
        centro_x - 13,
        y1 + 40,
        centro_x + 6,
        y1 + 30,
        fill="#7A3E2B",
        outline=COLOR_TEXTO_OSCURO,
        width=1,
        tags=tag_casilla
    )

    canvas_mapa.create_oval(
        centro_x + 1,
        y1 + 7,
        centro_x + 18,
        y1 + 22,
        fill=color_unidad,
        outline=COLOR_TEXTO_OSCURO,
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_arc(
        centro_x,
        y1 + 5,
        centro_x + 20,
        y1 + 22,
        start=0,
        extent=180,
        fill="#5A4A3A",
        outline=COLOR_TEXTO_OSCURO,
        width=1,
        tags=tag_casilla
    )

    canvas_mapa.create_polygon(
        centro_x + 2,
        y1 + 24,
        centro_x + 17,
        y1 + 21,
        centro_x + 20,
        y1 + 35,
        centro_x + 6,
        y1 + 39,
        fill=color_unidad,
        outline=COLOR_TEXTO_OSCURO,
        width=2,
        tags=tag_casilla
    )

    canvas_mapa.create_line(
        centro_x + 5,
        y1 + 26,
        centro_x - 9,
        y1 + 19,
        fill=COLOR_TEXTO_OSCURO,
        width=3,
        tags=tag_casilla
    )

    canvas_mapa.create_line(
        centro_x + 15,
        y1 + 27,
        centro_x + 28,
        y1 + 20,
        fill=COLOR_TEXTO_OSCURO,
        width=3,
        tags=tag_casilla
    )

    canvas_mapa.create_line(
        centro_x + 8,
        y1 + 39,
        centro_x - 5,
        y1 + 51,
        fill=COLOR_TEXTO_OSCURO,
        width=3,
        tags=tag_casilla
    )

    canvas_mapa.create_line(
        centro_x + 15,
        y1 + 38,
        centro_x + 28,
        y1 + 48,
        fill=COLOR_TEXTO_OSCURO,
        width=3,
        tags=tag_casilla
    )

    canvas_mapa.create_line(
        centro_x - 8,
        y1 + 51,
        centro_x + 1,
        y1 + 51,
        fill="#5A4A3A",
        width=3,
        tags=tag_casilla
    )

    canvas_mapa.create_line(
        centro_x + 25,
        y1 + 48,
        centro_x + 34,
        y1 + 48,
        fill="#5A4A3A",
        width=3,
        tags=tag_casilla
    )

    canvas_mapa.create_polygon(
        centro_x + 18,
        y1 + 21,
        centro_x + 28,
        y1 + 15,
        centro_x + 24,
        y1 + 24,
        fill="#C0C0C0",
        outline=COLOR_TEXTO_OSCURO,
        width=1,
        tags=tag_casilla
    )

    dibujar_vida_canvas(objeto, x1, y1, x2, y2, tag_casilla)


# Función para dibujar cualquier objeto del juego en Canvas
# Entradas: objeto del juego, fila y columna
# Salidas: ninguna, dibuja la figura correspondiente
def dibujar_objeto_canvas(objeto, fila, columna):
    if objeto is None:
        return

    if isinstance(objeto, BaseCentral):
        dibujar_base_canvas(objeto, fila, columna)

    elif isinstance(objeto, Muro):
        dibujar_muro_canvas(objeto, fila, columna)

    elif isinstance(objeto, Torre):
        if objeto.nombre == "Torre Básica":
            dibujar_torre_basica_canvas(objeto, fila, columna)

        elif objeto.nombre == "Torre Pesada":
            dibujar_torre_pesada_canvas(objeto, fila, columna)

        elif objeto.nombre == "Torre Mágica":
            dibujar_torre_magica_canvas(objeto, fila, columna)

    elif isinstance(objeto, Unidad):
        if objeto.nombre == "Soldado":
            dibujar_soldado_canvas(objeto, fila, columna)

        elif objeto.nombre == "Tanque":
            dibujar_tanque_canvas(objeto, fila, columna)

        elif objeto.nombre == "Unidad Rápida":
            dibujar_unidad_rapida_canvas(objeto, fila, columna)


# Función para actualizar visualmente una casilla del mapa
# Entradas: fila y columna de la casilla
# Salidas: ninguna, redibuja la casilla en el Canvas
def actualizar_boton_casilla(fila, columna):
    if canvas_mapa is None:
        return

    tag_casilla = obtener_tag_casilla(fila, columna)

    canvas_mapa.delete(tag_casilla)

    dibujar_casilla_canvas(fila, columna)
    dibujar_objeto_canvas(mapa_juego[fila][columna], fila, columna)


# Función para actualizar todo el mapa visual
# Entradas: ninguna
# Salidas: ninguna, redibuja el mapa completo en el Canvas
def actualizar_mapa_visual():
    if canvas_mapa is not None:
        canvas_mapa.delete("all")

        for fila in range(TAMANIO_MAPA):
            for columna in range(TAMANIO_MAPA):
                dibujar_casilla_canvas(fila, columna)
                dibujar_objeto_canvas(mapa_juego[fila][columna], fila, columna)

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
    actualizar_estado_visual()


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

    if partida_terminada:
        etiqueta_mensaje.config(text="La partida ya terminó. No puedes colocar más defensas.")
        return

    if fase_actual != "defensor":
        etiqueta_mensaje.config(text="Solo puedes colocar defensas durante la fase del defensor.")
        return
    
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
    actualizar_estado_visual()

# Función para colocar una unidad atacante en el mapa
# Entradas: fila y columna donde se desea colocar
# Salidas: ninguna, coloca la unidad si cumple las condiciones
def colocar_unidad(fila, columna):
    global dinero_atacante

    if partida_terminada:
        etiqueta_mensaje.config(text="La partida ya terminó. No puedes colocar más unidades.")
        return

    if fase_actual != "atacante":
        etiqueta_mensaje.config(text="Solo puedes colocar unidades durante la fase del atacante.")
        return
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


# Función para activar el modo venta
# Entradas: ninguna
# Salidas: ninguna, deja activo el modo venta hasta cancelar o seleccionar otra acción
def activar_modo_venta():
    global modo_venta
    global defensa_seleccionada
    global unidad_seleccionada

    if partida_terminada:
        return

    if fase_actual != "defensor" and fase_actual != "atacante":
        return

    modo_venta = True
    defensa_seleccionada = None
    unidad_seleccionada = None

    actualizar_estado_visual()


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
    actualizar_estado_visual()


# Función para vender o quitar un objeto del mapa
# Entradas: fila y columna donde se hizo clic
# Salidas: ninguna, elimina el objeto si se puede vender
def vender_objeto(fila, columna):
    global dinero_defensor
    global dinero_atacante
    global modo_venta

    if not posicion_en_rango(fila, columna):
        return

    if partida_terminada:
        etiqueta_mensaje.config(text="La partida ya terminó. No puedes vender objetos.")
        return

    if fase_actual != "defensor" and fase_actual != "atacante":
        etiqueta_mensaje.config(text="Solo puedes vender antes de iniciar el combate.")
        return

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

# Función para ejecutar el ataque de una torre aplicando su habilidad especial
# Entradas: torre, fila de la torre y columna de la torre
# Salidas: ninguna, aplica daño o efectos a una unidad enemiga
def ejecutar_ataque_torre_con_habilidad(torre, fila_torre, columna_torre):
    torre.avanzar_turno_habilidad()

    posicion_objetivo = buscar_unidad_en_alcance(torre, fila_torre, columna_torre)

    if posicion_objetivo is None:
        return
    

    fila_unidad, columna_unidad = posicion_objetivo
    unidad = mapa_juego[fila_unidad][columna_unidad]

    agregar_efecto_disparo_torre(
    fila_torre,
    columna_torre,
    fila_unidad,
    columna_unidad,
    torre.nombre
    )

    if not isinstance(unidad, Unidad):
        return

    if torre.habilidad_lista():

        if torre.nombre == "Torre Básica":
            unidad.recibir_danio(torre.danio)
            unidad.recibir_danio(torre.danio)

            registrar_evento_combate(
                f"Habilidad activada: {torre.nombre} usó Disparo doble contra {unidad.nombre}."
            )

        elif torre.nombre == "Torre Pesada":
            danio_extra = torre.danio * 2
            unidad.recibir_danio(danio_extra)

            registrar_evento_combate(
                f"Habilidad activada: {torre.nombre} hizo daño extra contra {unidad.nombre}."
            )

        elif torre.nombre == "Torre Mágica":
            unidad.recibir_danio(torre.danio)
            unidad.turnos_congelada = 1
            agregar_efecto_habilidad("congelar", fila_unidad, columna_unidad)

            registrar_evento_combate(
                f"Habilidad activada: {torre.nombre} congeló a {unidad.nombre} por 1 turno."
            )

        else:
            unidad.recibir_danio(torre.danio)

        torre.reiniciar_habilidad()

    else:
        unidad.recibir_danio(torre.danio)

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

# Función para actualizar los escudos temporales de las unidades
# Entradas: ninguna
# Salidas: ninguna, reduce duración del escudo y lo desactiva si termina
def actualizar_escudos_unidades():
    posiciones_unidades = obtener_posiciones_unidades()

    for fila, columna in posiciones_unidades:
        unidad = mapa_juego[fila][columna]

        if isinstance(unidad, Unidad) and unidad.turnos_escudo > 0:
            unidad.turnos_escudo -= 1

            if unidad.turnos_escudo == 0:
                unidad.escudo_activo = False
                registrar_evento_combate(f"El escudo de {unidad.nombre} terminó.")


# Función para hacer que las torres ataquen a las unidades
# Entradas: ninguna
# Salidas: ninguna, aplica daño y habilidades a unidades dentro del alcance
def ejecutar_ataque_torres():
    posiciones_torres = obtener_posiciones_torres()

    for fila_torre, columna_torre in posiciones_torres:
        torre = mapa_juego[fila_torre][columna_torre]

        if isinstance(torre, Torre):
            ejecutar_ataque_torre_con_habilidad(torre, fila_torre, columna_torre)

    eliminar_unidades_derrotadas()
    actualizar_escudos_unidades()

# Función para registrar eventos importantes del combate
# Entradas: mensaje descriptivo del evento
# Salidas: ninguna, muestra el evento en consola y en la interfaz
def registrar_evento_combate(mensaje):
    #print(mensaje)

    if etiqueta_mensaje is not None:
        etiqueta_mensaje.config(text=mensaje)


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

# Función para preparar la habilidad de una unidad antes de actuar
# Entradas: unidad atacante
# Salidas: ninguna, activa habilidad si corresponde
def preparar_habilidad_unidad(unidad):
    unidad.avanzar_turno_habilidad()

    if unidad.nombre == "Tanque" and unidad.habilidad_lista():
        unidad.escudo_activo = True
        unidad.turnos_escudo = 1
        agregar_efecto_habilidad_unidad("escudo", unidad)

        unidad.reiniciar_habilidad()


        registrar_evento_combate(
            f"Habilidad activada: {unidad.nombre} activó Escudo temporal."
        )

    elif unidad.nombre == "Unidad Rápida" and unidad.habilidad_lista():
        unidad.velocidad_extra_temporal = 1
        agregar_efecto_habilidad_unidad("velocidad", unidad)

        unidad.reiniciar_habilidad()

        registrar_evento_combate(
            f"Habilidad activada: {unidad.nombre} activó Aumento de velocidad."
        )


# Función para obtener cuántas veces ataca una unidad
# Entradas: unidad atacante
# Salidas: cantidad de ataques que realizará
def obtener_cantidad_ataques_unidad(unidad):
    if unidad.nombre == "Soldado" and unidad.habilidad_lista():
        unidad.reiniciar_habilidad()

        registrar_evento_combate(
            f"Habilidad activada: {unidad.nombre} usó Ataque doble."
        )

        agregar_efecto_habilidad_unidad("ataque_doble", unidad)

        return 2

    return 1

# Función para buscar la posición actual de una unidad específica
# Entradas: objeto unidad que se desea buscar
# Salidas: tupla con fila y columna, o None si no existe en el mapa
def buscar_posicion_unidad_objeto(unidad_buscada):
    for fila in range(TAMANIO_MAPA):
        for columna in range(TAMANIO_MAPA):
            objeto = mapa_juego[fila][columna]

            if objeto is unidad_buscada:
                return fila, columna

    return None

# Función para hacer que una unidad ataque un objetivo
# Entradas: unidad, objetivo, fila del objetivo y columna del objetivo
# Salidas: ninguna, aplica daño al objetivo
def unidad_ataca_objetivo(unidad, objetivo, fila_objetivo, columna_objetivo):
    posicion_unidad = buscar_posicion_unidad_objeto(unidad)

    if posicion_unidad is not None:
        fila_unidad, columna_unidad = posicion_unidad

        agregar_efecto_ataque_unidad(
            fila_unidad,
            columna_unidad,
            fila_objetivo,
            columna_objetivo,
            unidad.nombre,
            objetivo
        )

    cantidad_ataques = obtener_cantidad_ataques_unidad(unidad)
    

    for ataque in range(cantidad_ataques):
        if isinstance(objetivo, BaseCentral):
            objetivo.recibir_danio(unidad.danio)

            if not objetivo.esta_viva():
                return

        elif isinstance(objetivo, Muro):
            objetivo.recibir_danio(unidad.danio)

            if not objetivo.esta_vivo():
                mapa_juego[fila_objetivo][columna_objetivo] = None
                return

        elif isinstance(objetivo, Torre):
            objetivo.recibir_danio(unidad.danio)

            if not objetivo.esta_viva():
                mapa_juego[fila_objetivo][columna_objetivo] = None
                return

# Función para mover una unidad o atacar un obstáculo cercano
# Entradas: fila y columna de la unidad
# Salidas: ninguna, mueve o ataca según la casilla siguiente
def mover_o_atacar_unidad(fila, columna):
    unidad = mapa_juego[fila][columna]

    if not isinstance(unidad, Unidad):
        return

    if unidad.esta_congelada():
        registrar_evento_combate(
            f"{unidad.nombre} está congelada y pierde su turno."
        )

        unidad.actualizar_efectos_temporales()
        return

    preparar_habilidad_unidad(unidad)

    velocidad_turno = unidad.velocidad + unidad.velocidad_extra_temporal
    unidad.velocidad_extra_temporal = 0

    for movimiento in range(velocidad_turno):
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
                unidad_ataca_objetivo(unidad, objetivo, nueva_fila, nueva_columna)
                accion_realizada = True
                return

            if isinstance(objetivo, Muro) or isinstance(objetivo, Torre):
                unidad_ataca_objetivo(unidad, objetivo, nueva_fila, nueva_columna)
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

        actualizar_victoria(NOMBRE_JUGADOR_DEFENSOR, "defensor")

        mensaje += " El defensor ganó la partida completa."

    elif rondas_ganadas_atacante >= RONDAS_PARA_GANAR:
        partida_terminada = True

        actualizar_victoria(NOMBRE_JUGADOR_ATACANTE, "atacante")

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

    if partida_terminada:
        mostrar_resultado_partida(ganador, mensaje)


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
    global combate_en_progreso
    global turno_combate_actual
    global efectos_combate_pendientes

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
    efectos_combate_pendientes = []
    limpiar_efectos_combate()

    fase_actual = "defensor"
    defensa_seleccionada = None
    unidad_seleccionada = None
    modo_venta = False
    combate_en_progreso = False
    turno_combate_actual = 1

    if boton_siguiente_ronda is not None:
        boton_siguiente_ronda.config(state="disabled")

    etiqueta_mensaje.config(
        text=f"Inicia la ronda {numero_ronda}. El defensor debe colocar sus defensas."
    )

    actualizar_mapa_visual()

# Función para iniciar el combate animado
# Entradas: ninguna
# Salidas: ninguna, valida condiciones e inicia el combate por turnos visibles
def ejecutar_combate():
    global fase_actual
    global combate_en_progreso
    global turno_combate_actual

    if partida_terminada:
        etiqueta_mensaje.config(text="La partida ya terminó.")
        return

    if fase_actual != "atacante":
        etiqueta_mensaje.config(text="Solo puedes ejecutar combate después de la fase atacante.")
        return

    if contar_unidades_colocadas() == 0:
        etiqueta_mensaje.config(text="Debes colocar al menos una unidad atacante antes de combatir.")
        return

    fase_actual = "combate"
    combate_en_progreso = True
    turno_combate_actual = 1

    registrar_evento_combate("El combate ha iniciado.")
    actualizar_mapa_visual()

    if ventana_juego_actual is not None:
        ventana_juego_actual.after(VELOCIDAD_ANIMACION_COMBATE, ejecutar_turno_torres_animado)

# Función para ejecutar visualmente la fase de ataque de torres
# Entradas: ninguna
# Salidas: ninguna, ejecuta ataques de torres y programa la fase de unidades
def ejecutar_turno_torres_animado():
    global combate_en_progreso

    if not combate_en_progreso:
        return

    if partida_terminada:
        combate_en_progreso = False
        return

    registrar_evento_combate(f"Turno {turno_combate_actual}: las torres atacan.")

    ejecutar_ataque_torres()
    actualizar_mapa_visual()
    dibujar_efectos_combate_pendientes()

    ganador = verificar_ganador_ronda()

    if ganador is not None:
        finalizar_combate_animado(ganador)
        return

    if ventana_juego_actual is not None:
        ventana_juego_actual.after(VELOCIDAD_ANIMACION_COMBATE, ejecutar_turno_unidades_animado)

# Función para ejecutar visualmente la fase de movimiento y ataque de unidades
# Entradas: ninguna
# Salidas: ninguna, mueve unidades, actualiza mapa y programa el siguiente turno
def ejecutar_turno_unidades_animado():
    global turno_combate_actual
    global combate_en_progreso

    if not combate_en_progreso:
        return

    if partida_terminada:
        combate_en_progreso = False
        return

    registrar_evento_combate(f"Turno {turno_combate_actual}: las unidades avanzan y atacan.")

    ejecutar_turno_unidades()
    actualizar_mapa_visual()

    ganador = verificar_ganador_ronda()

    if ganador is not None:
        finalizar_combate_animado(ganador)
        return

    turno_combate_actual += 1

    if turno_combate_actual > LIMITE_TURNOS_COMBATE:
        registrar_evento_combate("El defensor resistió todos los turnos del combate.")
        finalizar_combate_animado("defensor")
        return

    if ventana_juego_actual is not None:
        ventana_juego_actual.after(VELOCIDAD_ANIMACION_COMBATE, ejecutar_turno_torres_animado)

# Función para finalizar el combate animado y registrar el ganador de ronda
# Entradas: ganador de la ronda
# Salidas: ninguna, detiene la animación y registra el resultado
def finalizar_combate_animado(ganador):
    global combate_en_progreso

    combate_en_progreso = False

    actualizar_mapa_visual()
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

# Función para manejar clics sobre el mapa dibujado en Canvas
# Entradas: evento del mouse generado por Tkinter
# Salidas: ninguna, convierte el clic en fila y columna del mapa
def manejar_click_canvas(evento):
    fila = evento.y // TAMANIO_CASILLA
    columna = evento.x // TAMANIO_CASILLA

    if posicion_en_rango(fila, columna):
        manejar_click_casilla(fila, columna)

# Función para terminar la fase del defensor
# Entradas: ninguna
# Salidas: ninguna, cambia la fase actual a atacante
# Función para terminar la fase del defensor
# Entradas: ninguna
# Salidas: ninguna, cambia la fase actual a atacante si hay defensas colocadas
def terminar_fase_defensor():
    global fase_actual
    global defensa_seleccionada
    global unidad_seleccionada
    global modo_venta

    if partida_terminada:
        etiqueta_mensaje.config(text="La partida ya terminó.")
        return

    if fase_actual != "defensor":
        etiqueta_mensaje.config(text="Solo puedes terminar la fase durante el turno del defensor.")
        return

    if contar_defensas_colocadas() == 0:
        etiqueta_mensaje.config(text="Debes colocar al menos una torre o muro antes de pasar al atacante.")
        return

    fase_actual = "atacante"
    defensa_seleccionada = None
    unidad_seleccionada = None
    modo_venta = False

    etiqueta_mensaje.config(text="Fase del defensor terminada. Ahora sigue la fase atacante.")
    actualizar_estado_visual()


# Función para crear el mapa visual usando Canvas
# Entradas: frame donde se mostrará el mapa
# Salidas: ninguna, crea el canvas interactivo del mapa
def crear_botones_mapa(frame_mapa):
    global canvas_mapa
    global botones_mapa

    ancho_canvas = TAMANIO_MAPA * TAMANIO_CASILLA
    alto_canvas = TAMANIO_MAPA * TAMANIO_CASILLA

    botones_mapa = []

    canvas_mapa = tk.Canvas(
        frame_mapa,
        width=ancho_canvas,
        height=alto_canvas,
        bg=COLOR_FONDO_APP,
        highlightthickness=0
    )
    canvas_mapa.grid(row=0, column=0, padx=8, pady=8)

    canvas_mapa.bind("<Button-1>", manejar_click_canvas)

    actualizar_mapa_visual()

# Función para iniciar la partida con jugadores, roles y facciones seleccionadas
# Entradas: ventana, jugadores, roles, facciones y etiqueta de error
# Salidas: ninguna, valida datos y abre el mapa del juego
def iniciar_partida_con_roles_y_facciones(
    ventana_seleccion,
    jugador_1,
    jugador_2,
    seleccion_defensor,
    seleccion_atacante,
    seleccion_faccion_defensor,
    seleccion_faccion_atacante,
    etiqueta_error
):
    global faccion_defensor_actual
    global faccion_atacante_actual
    global NOMBRE_JUGADOR_DEFENSOR
    global NOMBRE_JUGADOR_ATACANTE

    nombre_defensor = seleccion_defensor.get()
    nombre_atacante = seleccion_atacante.get()

    nombre_faccion_defensor = seleccion_faccion_defensor.get()
    nombre_faccion_atacante = seleccion_faccion_atacante.get()

    if nombre_defensor == nombre_atacante:
        etiqueta_error.config(text="Un mismo jugador no puede ser defensor y atacante.")
        return

    faccion_defensor = obtener_faccion(nombre_faccion_defensor)
    faccion_atacante = obtener_faccion(nombre_faccion_atacante)

    if faccion_defensor is None or faccion_atacante is None:
        etiqueta_error.config(text="Debes seleccionar facciones válidas.")
        return

    if not validar_facciones(faccion_defensor, faccion_atacante):
        etiqueta_error.config(text="El defensor y el atacante no pueden usar la misma facción.")
        return

    NOMBRE_JUGADOR_DEFENSOR = nombre_defensor
    NOMBRE_JUGADOR_ATACANTE = nombre_atacante

    faccion_defensor_actual = faccion_defensor
    faccion_atacante_actual = faccion_atacante

    reiniciar_estado_partida()

    ventana_seleccion.destroy()
    abrir_ventana_mapa()


# Función para abrir la pantalla de selección de roles y facciones
# Entradas: nombre del jugador 1 y nombre del jugador 2
# Salidas: ninguna, muestra ventana para elegir roles y facciones
def abrir_ventana_seleccion_facciones(jugador_1="Jugador 1", jugador_2="Jugador 2"):
    ventana_seleccion = tk.Tk()
    ventana_seleccion.title("Selección de roles y facciones")
    ventana_seleccion.geometry("760x600")
    ventana_seleccion.resizable(False, False)
    ventana_seleccion.config(bg=COLOR_FONDO_APP)

    titulo = tk.Label(
        ventana_seleccion,
        text="Preparar Partida",
        font=("Arial", 22, "bold"),
        bg=COLOR_FONDO_APP,
        fg=COLOR_TITULO
    )
    titulo.pack(pady=(25, 8))

    descripcion = tk.Label(
        ventana_seleccion,
        text="Seleccionen los roles y facciones antes de iniciar la batalla.",
        font=("Arial", 11),
        bg=COLOR_FONDO_APP,
        fg=COLOR_TEXTO
    )
    descripcion.pack(pady=(0, 18))

    frame_principal = tk.Frame(
        ventana_seleccion,
        bg=COLOR_FONDO_APP
    )
    frame_principal.pack(padx=25, pady=10, fill="both", expand=True)

    panel_jugadores = tk.Frame(
        frame_principal,
        bg=COLOR_PANEL,
        bd=1,
        relief="solid"
    )
    panel_jugadores.grid(row=0, column=0, padx=12, pady=10, sticky="nsew")

    panel_configuracion = tk.Frame(
        frame_principal,
        bg=COLOR_PANEL,
        bd=1,
        relief="solid"
    )
    panel_configuracion.grid(row=0, column=1, padx=12, pady=10, sticky="nsew")

    titulo_jugadores = tk.Label(
        panel_jugadores,
        text="Jugadores",
        font=("Arial", 16, "bold"),
        bg=COLOR_PANEL,
        fg=COLOR_TITULO
    )
    titulo_jugadores.pack(pady=(18, 12))

    tarjeta_jugador_1 = tk.Label(
        panel_jugadores,
        text=f"Jugador 1\n{jugador_1}",
        font=("Arial", 12, "bold"),
        bg=COLOR_ESTADO,
        fg=COLOR_TEXTO,
        width=22,
        height=4,
        relief="solid",
        bd=1
    )
    tarjeta_jugador_1.pack(pady=10, padx=25)

    tarjeta_jugador_2 = tk.Label(
        panel_jugadores,
        text=f"Jugador 2\n{jugador_2}",
        font=("Arial", 12, "bold"),
        bg=COLOR_ESTADO,
        fg=COLOR_TEXTO,
        width=22,
        height=4,
        relief="solid",
        bd=1
    )
    tarjeta_jugador_2.pack(pady=10, padx=25)

    nota = tk.Label(
        panel_jugadores,
        text="Cada jugador debe tener un rol distinto.",
        font=("Arial", 10),
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO,
        wraplength=220,
        justify="center"
    )
    nota.pack(pady=15)

    titulo_configuracion = tk.Label(
        panel_configuracion,
        text="Roles y Facciones",
        font=("Arial", 16, "bold"),
        bg=COLOR_PANEL,
        fg=COLOR_TITULO
    )
    titulo_configuracion.pack(pady=(18, 15))

    nombres_jugadores = [jugador_1, jugador_2]
    nombres_facciones = list(FACCIONES.keys())

    seleccion_defensor = tk.StringVar(ventana_seleccion)
    seleccion_defensor.set(jugador_1)

    seleccion_atacante = tk.StringVar(ventana_seleccion)
    seleccion_atacante.set(jugador_2)

    seleccion_faccion_defensor = tk.StringVar(ventana_seleccion)
    seleccion_faccion_defensor.set(nombres_facciones[0])

    seleccion_faccion_atacante = tk.StringVar(ventana_seleccion)
    seleccion_faccion_atacante.set(nombres_facciones[2])

    frame_formulario = tk.Frame(
        panel_configuracion,
        bg=COLOR_PANEL
    )
    frame_formulario.pack(padx=20, pady=5)

    etiqueta_defensor = tk.Label(
        frame_formulario,
        text="Defensor:",
        font=("Arial", 11, "bold"),
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO
    )
    etiqueta_defensor.grid(row=0, column=0, padx=8, pady=8, sticky="e")

    menu_defensor = tk.OptionMenu(
        frame_formulario,
        seleccion_defensor,
        *nombres_jugadores
    )
    menu_defensor.config(width=18, bg=COLOR_ESTADO, fg=COLOR_TEXTO, relief="flat")
    menu_defensor.grid(row=0, column=1, padx=8, pady=8)

    etiqueta_faccion_defensor = tk.Label(
        frame_formulario,
        text="Facción defensor:",
        font=("Arial", 11, "bold"),
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO
    )
    etiqueta_faccion_defensor.grid(row=1, column=0, padx=8, pady=8, sticky="e")

    menu_faccion_defensor = tk.OptionMenu(
        frame_formulario,
        seleccion_faccion_defensor,
        *nombres_facciones
    )
    menu_faccion_defensor.config(width=18, bg=COLOR_ESTADO, fg=COLOR_TEXTO, relief="flat")
    menu_faccion_defensor.grid(row=1, column=1, padx=8, pady=8)

    separador = tk.Frame(
        panel_configuracion,
        bg=COLOR_BORDE,
        height=1
    )
    separador.pack(fill="x", padx=35, pady=12)

    etiqueta_atacante = tk.Label(
        frame_formulario,
        text="Atacante:",
        font=("Arial", 11, "bold"),
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO
    )
    etiqueta_atacante.grid(row=2, column=0, padx=8, pady=8, sticky="e")

    menu_atacante = tk.OptionMenu(
        frame_formulario,
        seleccion_atacante,
        *nombres_jugadores
    )
    menu_atacante.config(width=18, bg=COLOR_ESTADO, fg=COLOR_TEXTO, relief="flat")
    menu_atacante.grid(row=2, column=1, padx=8, pady=8)

    etiqueta_faccion_atacante = tk.Label(
        frame_formulario,
        text="Facción atacante:",
        font=("Arial", 11, "bold"),
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO
    )
    etiqueta_faccion_atacante.grid(row=3, column=0, padx=8, pady=8, sticky="e")

    menu_faccion_atacante = tk.OptionMenu(
        frame_formulario,
        seleccion_faccion_atacante,
        *nombres_facciones
    )
    menu_faccion_atacante.config(width=18, bg=COLOR_ESTADO, fg=COLOR_TEXTO, relief="flat")
    menu_faccion_atacante.grid(row=3, column=1, padx=8, pady=8)

    etiqueta_error = tk.Label(
        ventana_seleccion,
        text="",
        fg="red",
        bg=COLOR_FONDO_APP,
        font=("Arial", 10, "bold")
    )
    etiqueta_error.pack(pady=5)

    boton_iniciar = crear_boton_estilizado(
        ventana_seleccion,
        "Iniciar partida",
        lambda: iniciar_partida_con_roles_y_facciones(
            ventana_seleccion,
            jugador_1,
            jugador_2,
            seleccion_defensor,
            seleccion_atacante,
            seleccion_faccion_defensor,
            seleccion_faccion_atacante,
            etiqueta_error
        ),
        ancho=24,
        color_fondo=COLOR_BOTON
    )
    boton_iniciar.pack(pady=18)

    ventana_seleccion.mainloop()

# Función para abrir la ventana del mapa del juego
# Entradas: ninguna
# Salidas: ninguna, muestra la ventana del mapa con diseño mejorado
def abrir_ventana_mapa():
    global etiqueta_estado
    global etiqueta_mensaje
    global etiqueta_info_defensor
    global etiqueta_info_atacante
    global boton_siguiente_ronda
    global boton_reiniciar_ronda
    global boton_salir
    global botones_defensor
    global botones_atacante
    global ventana_juego_actual
    global boton_vender_defensor
    global boton_vender_atacante

    botones_defensor = []
    botones_atacante = []

    ventana_juego_actual = tk.Tk()
    ventana_juego_actual.title("Defensa y Asalto de Base")
    ventana_juego_actual.geometry("1450x850")
    ventana_juego_actual.config(bg=COLOR_FONDO_APP)

    titulo = tk.Label(
        ventana_juego_actual,
        text="Defensa y Asalto de Base",
        font=("Arial", 22, "bold"),
        bg=COLOR_FONDO_APP,
        fg=COLOR_TITULO
    )
    titulo.pack(pady=15)

    etiqueta_estado = tk.Label(
        ventana_juego_actual,
        text="",
        font=("Arial", 11, "bold"),
        bg=COLOR_ESTADO,
        fg=COLOR_TEXTO,
        padx=15,
        pady=10,
        relief="solid",
        bd=1
    )
    etiqueta_estado.pack(pady=5, padx=25, fill="x")

    contenedor_principal = tk.Frame(
        ventana_juego_actual,
        bg=COLOR_FONDO_APP
    )
    contenedor_principal.pack(pady=15, padx=20, fill="both", expand=True)

    contenedor_principal.grid_columnconfigure(0, weight=1)
    contenedor_principal.grid_columnconfigure(1, weight=2)
    contenedor_principal.grid_columnconfigure(2, weight=1)

    # Panel defensor
    panel_defensor = tk.Frame(
        contenedor_principal,
        bg=COLOR_PANEL,
        bd=1,
        relief="solid"
    )
    panel_defensor.grid(row=0, column=0, sticky="ns", padx=12)

    titulo_defensor = tk.Label(
        panel_defensor,
        text=NOMBRE_JUGADOR_DEFENSOR,
        font=("Arial", 16, "bold"),
        bg=COLOR_PANEL,
        fg=COLOR_TITULO
    )
    titulo_defensor.pack(pady=(15, 5))

    subtitulo_defensor = tk.Label(
        panel_defensor,
        text="Panel del Defensor",
        font=("Arial", 11),
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO
    )
    subtitulo_defensor.pack(pady=(0, 10))

    boton_muro = crear_boton_estilizado(
        panel_defensor,
        "Muro - $30",
        lambda: seleccionar_defensa("Muro")
    )
    boton_muro.pack(pady=6, padx=20)

    boton_torre_basica = crear_boton_estilizado(
        panel_defensor,
        "Torre Básica - $50",
        lambda: seleccionar_defensa("Basica")
    )
    boton_torre_basica.pack(pady=6, padx=20)

    boton_torre_pesada = crear_boton_estilizado(
        panel_defensor,
        "Torre Pesada - $90",
        lambda: seleccionar_defensa("Pesada")
    )
    boton_torre_pesada.pack(pady=6, padx=20)

    boton_torre_magica = crear_boton_estilizado(
        panel_defensor,
        "Torre Mágica - $75",
        lambda: seleccionar_defensa("Magica")
    )
    boton_torre_magica.pack(pady=6, padx=20)

    boton_vender_defensor = crear_boton_estilizado(
        panel_defensor,
        "Vender / Quitar",
        activar_modo_venta,
        color_fondo=COLOR_BOTON_SECUNDARIO
    )
    boton_vender_defensor.pack(pady=6, padx=20)

    boton_cancelar_defensor = crear_boton_estilizado(
        panel_defensor,
        "Cancelar selección",
        cancelar_seleccion,
        color_fondo=COLOR_BOTON_SECUNDARIO
    )
    boton_cancelar_defensor.pack(pady=6, padx=20)

    boton_terminar = crear_boton_estilizado(
        panel_defensor,
        "Terminar fase",
        terminar_fase_defensor
    )
    boton_terminar.pack(pady=10, padx=20)

    etiqueta_info_defensor = tk.Label(
        panel_defensor,
        text="",
        justify="left",
        font=("Arial", 11),
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO,
        padx=12,
        pady=12
    )
    etiqueta_info_defensor.pack(pady=15)

    botones_defensor = [
        boton_muro,
        boton_torre_basica,
        boton_torre_pesada,
        boton_torre_magica,
        boton_vender_defensor,
        boton_cancelar_defensor,
        boton_terminar
    ]

    # Panel central
    panel_central = tk.Frame(
        contenedor_principal,
        bg=COLOR_FONDO_APP
    )
    panel_central.grid(row=0, column=1, sticky="n")

    frame_mapa = tk.Frame(
        panel_central,
        bg=COLOR_PANEL,
        bd=1,
        relief="solid"
    )
    frame_mapa.pack(pady=10)

    crear_botones_mapa(frame_mapa)

    panel_acciones = tk.Frame(
        panel_central,
        bg=COLOR_FONDO_APP
    )
    panel_acciones.pack(pady=18)

    boton_combate = crear_boton_estilizado(
        panel_acciones,
        "Ejecutar combate",
        ejecutar_combate,
        ancho=18
    )
    boton_combate.grid(row=0, column=0, padx=8, pady=5)

    boton_siguiente_ronda = crear_boton_estilizado(
        panel_acciones,
        "Siguiente ronda",
        preparar_siguiente_ronda,
        ancho=18,
        color_fondo=COLOR_BOTON_SECUNDARIO
    )
    boton_siguiente_ronda.grid(row=0, column=1, padx=8, pady=5)

    boton_reiniciar_ronda = crear_boton_estilizado(
        panel_acciones,
        "Reiniciar ronda",
        reiniciar_ronda_actual,
        ancho=18,
        color_fondo=COLOR_BOTON_SECUNDARIO
    )
    boton_reiniciar_ronda.grid(row=0, column=2, padx=8, pady=5)

    boton_salir = crear_boton_estilizado(
        panel_acciones,
        "Salir",
        salir_del_juego,
        ancho=18,
        color_fondo=COLOR_BOTON_ALERTA
    )
    boton_salir.grid(row=0, column=3, padx=8, pady=5)

    etiqueta_mensaje = tk.Label(
        panel_central,
        text="Selecciona una opción para comenzar.",
        font=("Arial", 11),
        bg=COLOR_FONDO_APP,
        fg=COLOR_TEXTO,
        wraplength=700,
        justify="center"
    )
    #etiqueta_mensaje.pack(pady=10)

    # Panel atacante
    panel_atacante = tk.Frame(
        contenedor_principal,
        bg=COLOR_PANEL,
        bd=1,
        relief="solid"
    )
    panel_atacante.grid(row=0, column=2, sticky="ns", padx=12)

    titulo_atacante = tk.Label(
        panel_atacante,
        text=NOMBRE_JUGADOR_ATACANTE,
        font=("Arial", 16, "bold"),
        bg=COLOR_PANEL,
        fg=COLOR_TITULO
    )
    titulo_atacante.pack(pady=(15, 5))

    subtitulo_atacante = tk.Label(
        panel_atacante,
        text="Panel del Atacante",
        font=("Arial", 11),
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO
    )
    subtitulo_atacante.pack(pady=(0, 10))

    boton_soldado = crear_boton_estilizado(
        panel_atacante,
        "Soldado - $40",
        lambda: seleccionar_unidad("Soldado")
    )
    boton_soldado.pack(pady=6, padx=20)

    boton_tanque = crear_boton_estilizado(
        panel_atacante,
        "Tanque - $90",
        lambda: seleccionar_unidad("Tanque")
    )
    boton_tanque.pack(pady=6, padx=20)

    boton_rapida = crear_boton_estilizado(
        panel_atacante,
        "Unidad Rápida - $60",
        lambda: seleccionar_unidad("Rapida")
    )
    boton_rapida.pack(pady=6, padx=20)

    boton_vender_atacante = crear_boton_estilizado(
        panel_atacante,
        "Vender / Quitar",
        activar_modo_venta,
        color_fondo=COLOR_BOTON_SECUNDARIO
    )
    boton_vender_atacante.pack(pady=6, padx=20)

    boton_cancelar_atacante = crear_boton_estilizado(
        panel_atacante,
        "Cancelar selección",
        cancelar_seleccion,
        color_fondo=COLOR_BOTON_SECUNDARIO
    )
    boton_cancelar_atacante.pack(pady=6, padx=20)

    etiqueta_info_atacante = tk.Label(
        panel_atacante,
        text="",
        justify="left",
        font=("Arial", 11),
        bg=COLOR_PANEL,
        fg=COLOR_TEXTO,
        padx=12,
        pady=12
    )
    etiqueta_info_atacante.pack(pady=15)

    botones_atacante = [
        boton_soldado,
        boton_tanque,
        boton_rapida,
        boton_vender_atacante,
        boton_cancelar_atacante,
        boton_combate
    ]

    actualizar_estado_visual()
    actualizar_botones_por_fase()

    ventana_juego_actual.mainloop()


crear_archivo_usuarios()
abrir_ventana_inicio()

