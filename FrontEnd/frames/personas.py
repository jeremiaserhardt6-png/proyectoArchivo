
import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_URL = "http://localhost:3000/api/personas"


def crear_personas(parent):
    frame = tk.Frame(parent, bg="#f1f2f3")

    borde = "#64132e"
    bordo = "#7c1738"
    gris = "#666b70"
    fondo = "#f1f2f3"
    blanco = "#ffffff"
    texto = "#151515"

    persona_seleccionada = {"id": None}
    personas_cache = []

    style = ttk.Style()

    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        "Persona.Treeview",
        background=blanco,
        foreground=texto,
        rowheight=30,
        fieldbackground=blanco,
        font=("Arial", 10)
    )

    style.configure(
        "Persona.Treeview.Heading",
        background=bordo,
        foreground=blanco,
        font=("Arial", 10, "bold")
    )

    style.map(
        "Persona.Treeview",
        background=[("selected", "#d8b9c3")],
        foreground=[("selected", texto)]
    )

    # ENCABEZADO
    encabezado = tk.Frame(frame, bg=borde, height=58)
    encabezado.pack(fill="x", padx=12, pady=(10, 12))
    encabezado.pack_propagate(False)

    tk.Label(
        encabezado,
        text="Gestion de Personas",
        font=("Arial", 18, "bold"),
        bg=borde,
        fg=blanco
    ).pack(side="left", padx=18)

    # FORMULARIO
    formulario = tk.Frame(frame, bg=fondo)
    formulario.pack(fill="x", padx=18, pady=(0, 12))

    formulario.grid_columnconfigure(1, weight=1)
    formulario.grid_columnconfigure(3, weight=1)

    def crear_label(texto_label, fila, columna):
        tk.Label(
            formulario,
            text=texto_label,
            font=("Arial", 10, "bold"),
            bg=fondo,
            fg=texto
        ).grid(
            row=fila,
            column=columna,
            sticky="w",
            padx=(0, 8),
            pady=8
        )

    def crear_entry(fila, columna):
        campo = tk.Entry(
            formulario,
            font=("Arial", 10),
            bg=blanco,
            fg=texto,
            relief="solid",
            bd=1
        )
        campo.grid(
            row=fila,
            column=columna,
            sticky="ew",
            padx=(0, 18),
            pady=8,
            ipady=4
        )
        return campo

    crear_label("Nombre:", 0, 0)
    entry_nombre = crear_entry(0, 1)

    crear_label("Apellido:", 0, 2)
    entry_apellido = crear_entry(0, 3)

    crear_label("Telefono:", 1, 0)
    entry_telefono = crear_entry(1, 1)

    # BUSQUEDA
    crear_label("Buscar:", 1, 2)

    entry_busqueda = tk.Entry(
        formulario,
        font=("Arial", 10),
        bg=blanco,
        fg=texto,
        relief="solid",
        bd=1
    )
    entry_busqueda.grid(
        row=1,
        column=3,
        sticky="ew",
        padx=(0, 18),
        pady=8,
        ipady=4
    )

    # BOTONES
    botones = tk.Frame(frame, bg=fondo)
    botones.pack(fill="x", padx=18, pady=(0, 12))

    # TABLA
    tabla_frame = tk.Frame(frame, bg=fondo)
    tabla_frame.pack(fill="both", expand=True, padx=18)

    columnas = (
        "id_persona",
        "nombre",
        "apellido",
        "telefono"
    )

    tabla = ttk.Treeview(
        tabla_frame,
        columns=columnas,
        show="headings",
        style="Persona.Treeview"
    )

    encabezados = {
        "id_persona": "ID",
        "nombre": "Nombre",
        "apellido": "Apellido",
        "telefono": "Telefono"
    }

    tabla.heading("id_persona", text="ID")
    tabla.heading("nombre", text="Nombre")
    tabla.heading("apellido", text="Apellido")
    tabla.heading("telefono", text="Telefono")

    tabla.column("id_persona", width=70, anchor="center")
    tabla.column("nombre", width=180, anchor="center")
    tabla.column("apellido", width=180, anchor="center")
    tabla.column("telefono", width=160, anchor="center")

    scroll_y = ttk.Scrollbar(
        tabla_frame,
        orient="vertical",
        command=tabla.yview
    )

    tabla.configure(yscrollcommand=scroll_y.set)

    tabla.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    # TOTAL DE REGISTROS
    total_label = tk.Label(
        frame,
        text="Total de registros: 0",
        font=("Arial", 10, "bold"),
        bg=fondo,
        fg=borde
    )
    total_label.pack(anchor="w", padx=22, pady=8)

    # LIMPIAR FORMULARIO
    def limpiar():
        persona_seleccionada["id"] = None

        entry_nombre.delete(0, tk.END)
        entry_apellido.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)

        tabla.selection_remove(tabla.selection())
        entry_nombre.focus()

    # OBTENER DATOS DEL FORMULARIO
    def datos_formulario():
        nombre = entry_nombre.get().strip()
        apellido = entry_apellido.get().strip()
        telefono = entry_telefono.get().strip()

        if not nombre or not apellido:
            messagebox.showwarning(
                "Campos incompletos",
                "Complete el nombre y el apellido."
            )
            return None

        return {
            "nombre": nombre,
            "apellido": apellido,
            "telefono": telefono
        }

    # MOSTRAR PERSONAS EN LA TABLA
    def mostrar_personas(personas):
        tabla.delete(*tabla.get_children())

        for persona in personas:
            tabla.insert(
                "",
                tk.END,
                values=(
                    persona.get("id_persona", persona.get("id", "")),
                    persona.get("nombre", ""),
                    persona.get("apellido", ""),
                    persona.get("telefono") or ""
                )
            )

        total_label.config(
            text=f"Total de registros: {len(personas)}"
        )

    # LISTAR PERSONAS
    def cargar_personas():
        nonlocal personas_cache

        try:
            respuesta = requests.get(API_URL, timeout=5)
            respuesta.raise_for_status()

            personas = respuesta.json()

            if not isinstance(personas, list):
                raise ValueError("La API no devolvio una lista de personas.")

            personas_cache = personas
            mostrar_personas(personas_cache)

        except (requests.exceptions.RequestException, ValueError) as error:
            messagebox.showerror(
                "Error de conexion",
                f"No se pudieron cargar las personas.\n\n{error}"
            )

    # SELECCIONAR PERSONA DE LA TABLA
    def seleccionar_persona(event=None):
        seleccion = tabla.selection()

        if not seleccion:
            return

        valores = tabla.item(seleccion[0], "values")

        if not valores:
            return

        persona_seleccionada["id"] = valores[0]

        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, valores[1])

        entry_apellido.delete(0, tk.END)
        entry_apellido.insert(0, valores[2])

        entry_telefono.delete(0, tk.END)
        entry_telefono.insert(0, valores[3])

    # AGREGAR PERSONA
    def agregar():
        datos = datos_formulario()

        if datos is None:
            return

        try:
            respuesta = requests.post(
                API_URL,
                json=datos,
                timeout=5
            )

            if respuesta.status_code == 201:
                messagebox.showinfo(
                    "Correcto",
                    "Persona agregada correctamente."
                )
                limpiar()
                cargar_personas()
            else:
                messagebox.showerror(
                    "Error",
                    f"No se pudo agregar la persona.\n{respuesta.text}"
                )

        except requests.exceptions.RequestException as error:
            messagebox.showerror(
                "Error de conexion",
                str(error)
            )

    # MODIFICAR PERSONA
    def modificar():
        id_persona = persona_seleccionada["id"]

        if not id_persona:
            messagebox.showwarning(
                "Modificar",
                "Seleccione una persona de la tabla."
            )
            return

        datos = datos_formulario()

        if datos is None:
            return

        try:
            respuesta = requests.put(
                f"{API_URL}/{id_persona}",
                json=datos,
                timeout=5
            )

            if respuesta.status_code == 200:
                messagebox.showinfo(
                    "Correcto",
                    "Persona actualizada correctamente."
                )
                limpiar()
                cargar_personas()
            else:
                messagebox.showerror(
                    "Error",
                    f"No se pudo modificar la persona.\n{respuesta.text}"
                )

        except requests.exceptions.RequestException as error:
            messagebox.showerror(
                "Error de conexion",
                str(error)
            )

    # ELIMINAR PERSONA
    def eliminar():
        id_persona = persona_seleccionada["id"]

        if not id_persona:
            messagebox.showwarning(
                "Eliminar",
                "Seleccione una persona de la tabla."
            )
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminacion",
            "Esta seguro de eliminar la persona seleccionada?"
        )

        if not confirmar:
            return

        try:
            respuesta = requests.delete(
                f"{API_URL}/{id_persona}",
                timeout=5
            )

            if respuesta.status_code == 200:
                messagebox.showinfo(
                    "Correcto",
                    "Persona eliminada correctamente."
                )
                limpiar()
                cargar_personas()
            else:
                messagebox.showerror(
                    "Error",
                    f"No se pudo eliminar la persona.\n{respuesta.text}"
                )

        except requests.exceptions.RequestException as error:
            messagebox.showerror(
                "Error de conexion",
                str(error)
            )

    # BUSCAR PERSONAS
    def buscar():
        texto_busqueda = entry_busqueda.get().strip().lower()

        if not texto_busqueda:
            mostrar_personas(personas_cache)
            return

        filtradas = [
            persona for persona in personas_cache
            if texto_busqueda in " ".join(
                str(persona.get(campo) or "")
                for campo in (
                    "id_persona",
                    "nombre",
                    "apellido",
                    "telefono"
                )
            ).lower()
        ]

        mostrar_personas(filtradas)

    # BOTONES CON ESTILO
    def crear_boton(texto_boton, comando, color):
        tk.Button(
            botones,
            text=texto_boton,
            command=comando,
            font=("Arial", 10, "bold"),
            bg=color,
            fg=blanco,
            activebackground=borde,
            activeforeground=blanco,
            relief="flat",
            cursor="hand2",
            bd=0
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=4,
            ipady=7
        )

    crear_boton("Agregar", agregar, bordo)
    crear_boton("Modificar", modificar, gris)
    crear_boton("Eliminar", eliminar, gris)
    crear_boton("Buscar", buscar, gris)
    crear_boton("Limpiar", limpiar, bordo)
    crear_boton("Actualizar", cargar_personas, gris)

    tabla.bind("<<TreeviewSelect>>", seleccionar_persona)
    entry_busqueda.bind("<Return>", lambda event: buscar())

    cargar_personas()

    return frame
