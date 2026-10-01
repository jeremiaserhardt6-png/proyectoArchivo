import tkinter as tk


def crear_inicio(parent):
    # Frame principal
    frame = tk.Frame(parent, bg="#f2f4f6")
    frame.pack(fill="both", expand=True)

    # =========================
    # BARRA LATERAL
    # =========================
    menu = tk.Frame(
        frame,
        bg="#65002d",
        width=135
    )
    menu.pack(side="left", fill="y")
    menu.pack_propagate(False)

    # Título del sistema
    titulo_menu = tk.Label(
        menu,
        text="📜  Archivo\nHistórico",
        font=("Arial", 11, "bold"),
        fg="white",
        bg="#65002d",
        justify="left"
    )
    titulo_menu.pack(pady=(15, 25), padx=15, anchor="w")

    # Opciones del menú
    opciones = [
        ("⌂", "Inicio"),
        ("✎", "Autores"),
        ("▮", "Materiales"),
        ("●", "Personas"),
        ("♟", "Usuarios")
    ]

    for icono, texto in opciones:
        boton = tk.Button(
            menu,
            text=f"{icono}   {texto}",
            font=("Arial", 10, "bold"),
            fg="white",
            bg="#65002d",
            activebackground="#8a1748",
            activeforeground="white",
            bd=0,
            relief="flat",
            anchor="w",
            padx=15
        )
        boton.pack(fill="x", ipady=8)

    # Separador
    tk.Frame(
        menu,
        bg="#8a1748",
        height=1
    ).pack(fill="x", padx=10, pady=(35, 15))

    # Cerrar sesión
    cerrar = tk.Button(
        menu,
        text="↪   Cerrar sesión",
        font=("Arial", 10, "bold"),
        fg="white",
        bg="#65002d",
        activebackground="#8a1748",
        activeforeground="white",
        bd=0,
        anchor="w",
        padx=15
    )
    cerrar.pack(fill="x", ipady=8)

    # =========================
    # CONTENIDO PRINCIPAL
    # =========================
    contenido = tk.Frame(
        frame,
        bg="#f2f4f6"
    )
    contenido.pack(
        side="right",
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    # Encabezado
    encabezado = tk.Frame(
        contenido,
        bg="#800033",
        height=48
    )
    encabezado.pack(fill="x")
    encabezado.pack_propagate(False)

    tk.Label(
        encabezado,
        text="⌂",
        font=("Arial", 23, "bold"),
        fg="white",
        bg="#800033"
    ).pack(side="left", padx=(15, 10))

    tk.Label(
        encabezado,
        text="Inicio",
        font=("Arial", 15, "bold"),
        fg="white",
        bg="#800033"
    ).pack(side="left")

    # =========================
    # BIENVENIDA
    # =========================
    bienvenida = tk.Label(
        contenido,
        text="Bienvenido al Archivo Histórico",
        font=("Arial", 19, "bold"),
        fg="#65002d",
        bg="#f2f4f6"
    )
    bienvenida.pack(pady=(15, 2))

    descripcion = tk.Label(
        contenido,
        text="Desde este sistema podés administrar la información histórica.",
        font=("Arial", 10),
        fg="#202020",
        bg="#f2f4f6"
    )
    descripcion.pack()

    # =========================
    # TARJETAS
    # =========================
    tarjetas = tk.Frame(
        contenido,
        bg="#f2f4f6"
    )
    tarjetas.pack(
        fill="both",
        expand=True,
        padx=15,
        pady=20
    )

    datos = [
        ("✎", "Autores"),
        ("▮", "Materiales"),
        ("●", "Personas"),
        ("♟", "Usuarios")
    ]

    for icono, nombre in datos:

        tarjeta = tk.Frame(
            tarjetas,
            bg="white",
            highlightbackground="#c8d0d8",
            highlightthickness=1
        )

        tarjeta.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        # Ícono
        tk.Label(
            tarjeta,
            text=icono,
            font=("Arial", 30, "bold"),
            fg="#5f6870",
            bg="white"
        ).pack(pady=(15, 2))

        # Nombre
        tk.Label(
            tarjeta,
            text=nombre,
            font=("Arial", 12, "bold"),
            fg="#65002d",
            bg="white"
        ).pack(pady=2)

        # Botón
        tk.Button(
            tarjeta,
            text="Administrar",
            font=("Arial", 10, "bold"),
            fg="white",
            bg="#800033",
            activebackground="#65002d",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=5
        ).pack(
            fill="x",
            padx=12,
            pady=(10, 15)
        )

    return frame