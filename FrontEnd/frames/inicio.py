
import tkinter as tk
from tkinter import messagebox

from frames.autores import crear_autores
from frames.materiales import crear_materiales
from frames.usuarios import crear_usuario
from frames.personas import crear_personas


COLOR_FONDO = "#f2f4f6"
COLOR_MENU = "#65002d"
COLOR_MENU_ACTIVO = "#8a1748"
COLOR_BORDO = "#800033"
COLOR_BLANCO = "#ffffff"
COLOR_TEXTO = "#202020"


def crear_inicio(parent):
    frame = tk.Frame(parent, bg=COLOR_FONDO)

    # MENU LATERAL
    menu = tk.Frame(frame, bg=COLOR_MENU, width=135)
    menu.pack(side="left", fill="y")
    menu.pack_propagate(False)

    # AREA DE CONTENIDO
    contenido = tk.Frame(frame, bg=COLOR_FONDO)
    contenido.pack(
        side="right",
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    botones_menu = {}

    # LIMPIAR CONTENIDO
    def limpiar_contenido():
        for widget in contenido.winfo_children():
            widget.destroy()

    # MARCAR OPCION ACTIVA
    def marcar_activo(nombre):
        for texto, boton in botones_menu.items():
            color = (
                COLOR_MENU_ACTIVO
                if texto == nombre
                else COLOR_MENU
            )
            boton.config(bg=color)

    # MOSTRAR UNA VISTA
    def mostrar_vista(nombre, funcion):
        limpiar_contenido()
        marcar_activo(nombre)

        nuevo_frame = funcion(contenido)
        nuevo_frame.pack(fill="both", expand=True)

    # PANTALLA DE INICIO
    def mostrar_inicio_contenido():
        limpiar_contenido()
        marcar_activo("Inicio")

        encabezado = tk.Frame(
            contenido,
            bg=COLOR_BORDO,
            height=48
        )
        encabezado.pack(fill="x")
        encabezado.pack_propagate(False)

        tk.Label(
            encabezado,
            text="Inicio",
            font=("Arial", 15, "bold"),
            fg=COLOR_BLANCO,
            bg=COLOR_BORDO
        ).pack(side="left", padx=15)

        tk.Label(
            contenido,
            text="Bienvenido al Archivo Historico",
            font=("Arial", 19, "bold"),
            fg=COLOR_MENU,
            bg=COLOR_FONDO
        ).pack(pady=(15, 2))

        tk.Label(
            contenido,
            text="Desde este sistema podes administrar "
                 "la informacion historica.",
            font=("Arial", 10),
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO
        ).pack()

        tarjetas = tk.Frame(contenido, bg=COLOR_FONDO)
        tarjetas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=20
        )

        tarjetas_datos = [
            ("Autores", crear_autores),
            ("Materiales", crear_materiales),
            ("Personas", crear_personas),
            ("Usuarios", crear_usuario)
        ]

        for nombre, funcion in tarjetas_datos:
            tarjeta = tk.Frame(
                tarjetas,
                bg=COLOR_BLANCO,
                highlightbackground="#c8d0d8",
                highlightthickness=1
            )
            tarjeta.pack(
                side="left",
                fill="both",
                expand=True,
                padx=5
            )

            tk.Label(
                tarjeta,
                text=nombre,
                font=("Arial", 12, "bold"),
                fg=COLOR_MENU,
                bg=COLOR_BLANCO
            ).pack(pady=(25, 8))

            tk.Button(
                tarjeta,
                text="Administrar",
                font=("Arial", 10, "bold"),
                fg=COLOR_BLANCO,
                bg=COLOR_BORDO,
                activebackground=COLOR_MENU,
                activeforeground=COLOR_BLANCO,
                bd=0,
                cursor="hand2",
                command=lambda n=nombre, f=funcion:
                    mostrar_vista(n, f)
            ).pack(
                fill="x",
                padx=12,
                pady=(10, 15)
            )

    # ENCABEZADO DEL MENU
    tk.Label(
        menu,
        text="Archivo\nHistorico",
        font=("Arial", 11, "bold"),
        fg=COLOR_BLANCO,
        bg=COLOR_MENU,
        justify="left"
    ).pack(
        pady=(15, 25),
        padx=15,
        anchor="w"
    )

    # OPCIONES DEL MENU
    opciones = [
        ("Inicio", mostrar_inicio_contenido),
        (
            "Autores",
            lambda: mostrar_vista("Autores", crear_autores)
        ),
        (
            "Materiales",
            lambda: mostrar_vista("Materiales", crear_materiales)
        ),
        (
            "Personas",
            lambda: mostrar_vista("Personas", crear_personas)
        ),
        (
            "Usuarios",
            lambda: mostrar_vista("Usuarios", crear_usuario)
        )
    ]

    for nombre, comando in opciones:
        boton = tk.Button(
            menu,
            text=nombre,
            font=("Arial", 10, "bold"),
            fg=COLOR_BLANCO,
            bg=COLOR_MENU,
            activebackground=COLOR_MENU_ACTIVO,
            activeforeground=COLOR_BLANCO,
            bd=0,
            relief="flat",
            anchor="w",
            padx=15,
            cursor="hand2",
            command=comando
        )
        boton.pack(fill="x", ipady=8)
        botones_menu[nombre] = boton

    # SEPARADOR
    tk.Frame(
        menu,
        bg=COLOR_MENU_ACTIVO,
        height=1
    ).pack(
        fill="x",
        padx=10,
        pady=(35, 15)
    )

    # CERRAR SESION
    def cerrar_sesion():
        confirmar = messagebox.askyesno(
            "Cerrar sesion",
            "Deseas cerrar la sesion?"
        )

        if confirmar:
            ventana = parent.winfo_toplevel()
            ventana.destroy()

    tk.Button(
        menu,
        text="Cerrar sesion",
        font=("Arial", 10, "bold"),
        fg=COLOR_BLANCO,
        bg=COLOR_MENU,
        activebackground=COLOR_MENU_ACTIVO,
        activeforeground=COLOR_BLANCO,
        bd=0,
        anchor="w",
        padx=15,
        cursor="hand2",
        command=cerrar_sesion
    ).pack(fill="x", ipady=8)

    # MOSTRAR INICIO AL ABRIR
    mostrar_inicio_contenido()

    return frame
