import tkinter as tk
from tkinter import ttk, messagebox
import requests


# ============================================================
# CONFIGURACIÓN DE LA API
# ============================================================

API_URL = "http://localhost:3000/api/autores"


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def crear_autores(parent):

    # --------------------------------------------------------
    # COLORES
    # --------------------------------------------------------

    COLOR_BORDO = "#72002F"
    COLOR_BORDO_OSCURO = "#570024"
    COLOR_GRIS = "#68727A"
    COLOR_GRIS_CLARO = "#EEF1F3"
    COLOR_BLANCO = "#FFFFFF"
    COLOR_NEGRO = "#202020"

    # --------------------------------------------------------
    # FRAME PRINCIPAL
    # --------------------------------------------------------

    frame = tk.Frame(
        parent,
        bg=COLOR_GRIS_CLARO
    )

    frame.pack(
        fill="both",
        expand=True
    )

    # ========================================================
    # ENCABEZADO
    # ========================================================

    encabezado = tk.Frame(
        frame,
        bg=COLOR_BORDO_OSCURO,
        height=55
    )

    encabezado.pack(
        fill="x",
        padx=8,
        pady=(8, 0)
    )

    encabezado.pack_propagate(False)

    # Icono
    tk.Label(
        encabezado,
        text="✎",
        font=("Arial", 25, "bold"),
        bg=COLOR_BORDO_OSCURO,
        fg=COLOR_BLANCO
    ).pack(
        side="left",
        padx=(15, 10)
    )

    tk.Label(
        encabezado,
        text="Gestión de Autores",
        font=("Arial", 17, "bold"),
        bg=COLOR_BORDO_OSCURO,
        fg=COLOR_BLANCO
    ).pack(
        side="left"
    )

    tk.Label(
        encabezado,
        text="Administración de autores",
        font=("Arial", 9),
        bg=COLOR_BORDO_OSCURO,
        fg=COLOR_BLANCO
    ).pack(
        side="right",
        padx=15
    )

    # ========================================================
    # FORMULARIO
    # ========================================================

    formulario = tk.Frame(
        frame,
        bg=COLOR_GRIS_CLARO
    )

    formulario.pack(
        fill="x",
        padx=25,
        pady=15
    )

    # --------------------------------------------------------
    # ID AUTOR
    # --------------------------------------------------------

    tk.Label(
        formulario,
        text="ID Autor:",
        font=("Arial", 10, "bold"),
        bg=COLOR_GRIS_CLARO,
        fg=COLOR_NEGRO
    ).grid(
        row=0,
        column=0,
        sticky="w",
        padx=(0, 8),
        pady=5
    )

    entry_id = tk.Entry(
        formulario,
        font=("Arial", 10),
        relief="solid",
        bd=1
    )

    entry_id.grid(
        row=0,
        column=1,
        sticky="ew",
        padx=(0, 30),
        pady=5
    )

    # --------------------------------------------------------
    # NOMBRE
    # --------------------------------------------------------

    tk.Label(
        formulario,
        text="Nombre:",
        font=("Arial", 10, "bold"),
        bg=COLOR_GRIS_CLARO,
        fg=COLOR_NEGRO
    ).grid(
        row=0,
        column=2,
        sticky="w",
        padx=(0, 8),
        pady=5
    )

    entry_nombre = tk.Entry(
        formulario,
        font=("Arial", 10),
        relief="solid",
        bd=1
    )

    entry_nombre.grid(
        row=0,
        column=3,
        sticky="ew",
        pady=5
    )

    # --------------------------------------------------------
    # APELLIDO
    # --------------------------------------------------------

    tk.Label(
        formulario,
        text="Apellido:",
        font=("Arial", 10, "bold"),
        bg=COLOR_GRIS_CLARO,
        fg=COLOR_NEGRO
    ).grid(
        row=1,
        column=0,
        sticky="w",
        padx=(0, 8),
        pady=5
    )

    entry_apellido = tk.Entry(
        formulario,
        font=("Arial", 10),
        relief="solid",
        bd=1
    )

    entry_apellido.grid(
        row=1,
        column=1,
        columnspan=3,
        sticky="ew",
        pady=5
    )

    formulario.columnconfigure(1, weight=1)
    formulario.columnconfigure(3, weight=2)

    # ========================================================
    # FUNCIONES
    # ========================================================

    def limpiar():

        entry_id.delete(0, tk.END)
        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)

        entry_id.focus()

        # Quitar selección de la tabla
        for item in tabla.selection():
            tabla.selection_remove(item)

    # --------------------------------------------------------
    # CARGAR AUTORES
    # --------------------------------------------------------

    def cargar_autores():

        # Limpiar tabla
        for item in tabla.get_children():
            tabla.delete(item)

        try:

            respuesta = requests.get(
                API_URL,
                timeout=5
            )

            if respuesta.status_code != 200:

                messagebox.showerror(
                    "Error",
                    "No se pudieron cargar los autores."
                )

                return

            autores = respuesta.json()

            for autor in autores:

                tabla.insert(
                    "",
                    "end",
                    values=(
                        autor.get("id_autor", ""),
                        autor.get("nombre", ""),
                        autor.get("apellido", "")
                    )
                )

            actualizar_total()

        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con el servidor.\n\n"
                + str(error)
            )

    # --------------------------------------------------------
    # ACTUALIZAR TOTAL
    # --------------------------------------------------------

    def actualizar_total():

        cantidad = len(tabla.get_children())

        label_total.config(
            text=f"Total de registros: {cantidad}"
        )

    # --------------------------------------------------------
    # SELECCIONAR AUTOR
    # --------------------------------------------------------

    def seleccionar_autor(event):

        seleccion = tabla.selection()

        if not seleccion:
            return

        item = tabla.item(
            seleccion[0]
        )

        valores = item["values"]

        limpiar_campos = False

        entry_id.delete(0, tk.END)
        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)

        if len(valores) >= 3:

            entry_id.insert(
                0,
                valores[0]
            )

            entry_nombre.insert(
                0,
                valores[1]
            )

            entry_apellido.insert(
                0,
                valores[2]
            )

    # --------------------------------------------------------
    # AGREGAR AUTOR
    # --------------------------------------------------------

    def agregar():

        nombre = entry_nombre.get().strip()
        apellido = entry_apellido.get().strip()

        if nombre == "" or apellido == "":

            messagebox.showwarning(
                "Campos incompletos",
                "Completá el nombre y el apellido."
            )

            return

        datos = {
            "nombre": nombre,
            "apellido": apellido,

            # Tu ruta pide este campo.
            # Se envía None para que MySQL lo guarde como NULL.
            "fecha_nacimiento": None
        }

        try:

            respuesta = requests.post(
                API_URL,
                json=datos,
                timeout=5
            )

            if respuesta.status_code == 201:

                messagebox.showinfo(
                    "Éxito",
                    "Autor agregado correctamente."
                )

                limpiar()
                cargar_autores()

            else:

                try:
                    error = respuesta.json()
                    detalle = error.get(
                        "detalle",
                        "Error desconocido."
                    )
                except:
                    detalle = respuesta.text

                messagebox.showerror(
                    "Error",
                    f"No se pudo agregar el autor.\n\n{detalle}"
                )

        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con el servidor.\n\n"
                + str(error)
            )

    # --------------------------------------------------------
    # MODIFICAR AUTOR
    # --------------------------------------------------------

    def modificar():

        id_autor = entry_id.get().strip()
        nombre = entry_nombre.get().strip()
        apellido = entry_apellido.get().strip()

        if id_autor == "":

            messagebox.showwarning(
                "Seleccionar autor",
                "Seleccioná un autor de la tabla."
            )

            return

        if nombre == "" or apellido == "":

            messagebox.showwarning(
                "Campos incompletos",
                "Completá el nombre y el apellido."
            )

            return

        datos = {
            "nombre": nombre,
            "apellido": apellido,
            "fecha_nacimiento": None
        }

        try:

            respuesta = requests.put(
                f"{API_URL}/{id_autor}",
                json=datos,
                timeout=5
            )

            if respuesta.status_code == 200:

                messagebox.showinfo(
                    "Éxito",
                    "Autor actualizado correctamente."
                )

                limpiar()
                cargar_autores()

            elif respuesta.status_code == 404:

                messagebox.showwarning(
                    "No encontrado",
                    "El autor no existe."
                )

            else:

                try:
                    error = respuesta.json()
                    detalle = error.get(
                        "detalle",
                        "Error desconocido."
                    )
                except:
                    detalle = respuesta.text

                messagebox.showerror(
                    "Error",
                    f"No se pudo modificar el autor.\n\n{detalle}"
                )

        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con el servidor.\n\n"
                + str(error)
            )

    # --------------------------------------------------------
    # ELIMINAR AUTOR
    # --------------------------------------------------------

    def eliminar():

        id_autor = entry_id.get().strip()

        if id_autor == "":

            messagebox.showwarning(
                "Seleccionar autor",
                "Seleccioná un autor de la tabla."
            )

            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Estás seguro de eliminar este autor?"
        )

        if not confirmar:
            return

        try:

            respuesta = requests.delete(
                f"{API_URL}/{id_autor}",
                timeout=5
            )

            if respuesta.status_code == 200:

                messagebox.showinfo(
                    "Éxito",
                    "Autor eliminado correctamente."
                )

                limpiar()
                cargar_autores()

            elif respuesta.status_code == 404:

                messagebox.showwarning(
                    "No encontrado",
                    "El autor no existe."
                )

            else:

                try:
                    error = respuesta.json()
                    detalle = error.get(
                        "detalle",
                        "Error desconocido."
                    )
                except:
                    detalle = respuesta.text

                messagebox.showerror(
                    "Error",
                    f"No se pudo eliminar el autor.\n\n{detalle}"
                )

        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                "No se pudo conectar con el servidor.\n\n"
                + str(error)
            )

    # ========================================================
    # BOTONES
    # ========================================================

    botones = tk.Frame(
        frame,
        bg=COLOR_GRIS_CLARO
    )

    botones.pack(
        fill="x",
        padx=25,
        pady=(0, 12)
    )

    # --------------------------------------------------------
    # AGREGAR
    # --------------------------------------------------------

    btn_agregar = tk.Button(
        botones,
        text="✚   Agregar",
        font=("Arial", 10, "bold"),
        bg=COLOR_BORDO,
        fg=COLOR_BLANCO,
        activebackground=COLOR_BORDO_OSCURO,
        activeforeground=COLOR_BLANCO,
        relief="flat",
        cursor="hand2",
        command=agregar
    )

    btn_agregar.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(0, 8),
        ipady=7
    )

    # --------------------------------------------------------
    # MODIFICAR
    # --------------------------------------------------------

    btn_modificar = tk.Button(
        botones,
        text="✎   Modificar",
        font=("Arial", 10, "bold"),
        bg=COLOR_GRIS,
        fg=COLOR_BLANCO,
        activebackground="#515A60",
        activeforeground=COLOR_BLANCO,
        relief="flat",
        cursor="hand2",
        command=modificar
    )

    btn_modificar.pack(
        side="left",
        fill="x",
        expand=True,
        padx=8,
        ipady=7
    )

    # --------------------------------------------------------
    # ELIMINAR
    # --------------------------------------------------------

    btn_eliminar = tk.Button(
        botones,
        text="▣   Eliminar",
        font=("Arial", 10, "bold"),
        bg=COLOR_GRIS,
        fg=COLOR_BLANCO,
        activebackground="#515A60",
        activeforeground=COLOR_BLANCO,
        relief="flat",
        cursor="hand2",
        command=eliminar
    )

    btn_eliminar.pack(
        side="left",
        fill="x",
        expand=True,
        padx=8,
        ipady=7
    )

    # --------------------------------------------------------
    # LIMPIAR
    # --------------------------------------------------------

    btn_limpiar = tk.Button(
        botones,
        text="⟳   Limpiar",
        font=("Arial", 10, "bold"),
        bg=COLOR_GRIS,
        fg=COLOR_BLANCO,
        activebackground="#515A60",
        activeforeground=COLOR_BLANCO,
        relief="flat",
        cursor="hand2",
        command=limpiar
    )

    btn_limpiar.pack(
        side="left",
        fill="x",
        expand=True,
        padx=(8, 0),
        ipady=7
    )

    # ========================================================
    # TABLA
    # ========================================================

    tabla_frame = tk.Frame(
        frame,
        bg=COLOR_GRIS_CLARO
    )

    tabla_frame.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=(0, 5)
    )

    # --------------------------------------------------------
    # ESTILO DE TABLA
    # --------------------------------------------------------

    estilo = ttk.Style()

    try:
        estilo.theme_use("clam")
    except:
        pass

    estilo.configure(
        "Treeview",
        background=COLOR_BLANCO,
        foreground=COLOR_NEGRO,
        rowheight=32,
        fieldbackground=COLOR_BLANCO,
        font=("Arial", 10)
    )

    estilo.configure(
        "Treeview.Heading",
        background=COLOR_BORDO,
        foreground=COLOR_BLANCO,
        font=("Arial", 10, "bold"),
        relief="flat"
    )

    estilo.map(
        "Treeview",
        background=[
            ("selected", "#E8B8CC")
        ],
        foreground=[
            ("selected", COLOR_NEGRO)
        ]
    )

    # --------------------------------------------------------
    # SCROLLBAR
    # --------------------------------------------------------

    scrollbar = ttk.Scrollbar(
        tabla_frame,
        orient="vertical"
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # --------------------------------------------------------
    # TREEVIEW
    # --------------------------------------------------------

    tabla = ttk.Treeview(
        tabla_frame,
        columns=(
            "id",
            "nombre",
            "apellido"
        ),
        show="headings",
        yscrollcommand=scrollbar.set,
        selectmode="browse"
    )

    scrollbar.config(
        command=tabla.yview
    )

    # Encabezados

    tabla.heading(
        "id",
        text="Id_Autor"
    )

    tabla.heading(
        "nombre",
        text="Nombre"
    )

    tabla.heading(
        "apellido",
        text="Apellido"
    )

    # Anchos

    tabla.column(
        "id",
        width=150,
        anchor="w"
    )

    tabla.column(
        "nombre",
        width=250,
        anchor="w"
    )

    tabla.column(
        "apellido",
        width=250,
        anchor="w"
    )

    tabla.pack(
        fill="both",
        expand=True
    )

    # Cuando se hace click en una fila
    tabla.bind(
        "<<TreeviewSelect>>",
        seleccionar_autor
    )

    # ========================================================
    # TOTAL DE REGISTROS
    # ========================================================

    label_total = tk.Label(
        frame,
        text="Total de registros: 0",
        font=("Arial", 10, "bold"),
        bg=COLOR_GRIS_CLARO,
        fg=COLOR_BORDO
    )

    label_total.pack(
        anchor="w",
        padx=25,
        pady=(0, 12)
    )

    # ========================================================
    # CARGAR DATOS AL ABRIR
    # ========================================================

    cargar_autores()

    return frame