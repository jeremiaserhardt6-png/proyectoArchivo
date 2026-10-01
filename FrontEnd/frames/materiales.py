import tkinter as tk
from tkinter import ttk, messagebox
import requests


# ============================================================
# CONFIGURACIÓN
# ============================================================

API_URL = "http://localhost:3000/api/materiales"

# Rutas de las tablas relacionadas.
# Cambialas si en tu backend tienen otro nombre.
URL_PERSONAS = "http://localhost:3000/api/personas"
URL_AUTORES = "http://localhost:3000/api/autores"
URL_CATEGORIAS = "http://localhost:3000/api/categorias"
URL_COLECCIONES = "http://localhost:3000/api/colecciones"


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def crear_materiales(parent):

    frame = tk.Frame(parent, bg="#f1f2f3")
    frame.pack(fill="both", expand=True)

    material_seleccionado = {"id": None}

    # --------------------------------------------------------
    # COLORES
    # --------------------------------------------------------

    BORDEAUX = "#7c1738"
    BORDEAUX_OSCURO = "#64132e"
    GRIS = "#666b70"
    FONDO = "#f1f2f3"
    BLANCO = "#ffffff"
    BORDE = "#aeb3b8"
    TEXTO = "#151515"

    # --------------------------------------------------------
    # ESTILOS
    # --------------------------------------------------------

    style = ttk.Style()

    try:
        style.theme_use("clam")
    except:
        pass

    style.configure(
        "Material.TCombobox",
        fieldbackground="white",
        background="white",
        foreground=TEXTO,
        bordercolor=BORDE,
        arrowcolor="#222222",
        padding=8
    )

    style.configure(
        "Material.Treeview",
        background="white",
        foreground="#151922",
        rowheight=54,
        fieldbackground="white",
        font=("Arial", 12)
    )

    style.configure(
        "Material.Treeview.Heading",
        background=BORDEAUX,
        foreground="white",
        font=("Arial", 12, "bold"),
        padding=10
    )

    style.map(
        "Material.Treeview",
        background=[
            ("selected", "#d8aebe")
        ],
        foreground=[
            ("selected", "#111111")
        ]
    )

    # --------------------------------------------------------
    # FUNCIONES AUXILIARES
    # --------------------------------------------------------

    def crear_entry(parent, width=30):
        return tk.Entry(
            parent,
            width=width,
            font=("Arial", 12),
            bg="white",
            fg=TEXTO,
            relief="solid",
            bd=1
        )

    def obtener_datos(url):
        try:
            respuesta = requests.get(url, timeout=5)

            if respuesta.status_code == 200:
                datos = respuesta.json()

                # Si el backend devuelve directamente una lista
                if isinstance(datos, list):
                    return datos

                # Por si devuelve {"datos": [...]}
                if isinstance(datos, dict):
                    return datos.get("datos", [])

            return []

        except requests.exceptions.RequestException:
            return []

    def limpiar_combobox(combo):
        combo["values"] = []

    # --------------------------------------------------------
    # CARGAR COMBOS
    # --------------------------------------------------------

    personas = obtener_datos(URL_PERSONAS)
    autores = obtener_datos(URL_AUTORES)
    categorias = obtener_datos(URL_CATEGORIAS)
    colecciones = obtener_datos(URL_COLECCIONES)

    # Diccionarios para relacionar nombre -> ID
    personas_map = {}
    autores_map = {}
    categorias_map = {}
    colecciones_map = {}

    # --------------------------------------------------------
    # ENCABEZADO
    # --------------------------------------------------------

    encabezado = tk.Frame(
        frame,
        bg=BORDEAUX_OSCURO,
        height=95
    )

    encabezado.pack(
        fill="x",
        padx=16,
        pady=(10, 15)
    )

    encabezado.pack_propagate(False)

    icono = tk.Label(
        encabezado,
        text="▣",
        font=("Arial", 42),
        bg=BORDEAUX_OSCURO,
        fg="white"
    )

    icono.pack(
        side="left",
        padx=(35, 20)
    )

    titulo = tk.Label(
        encabezado,
        text="Gestión de Materiales",
        font=("Arial", 28, "bold"),
        bg=BORDEAUX_OSCURO,
        fg="white"
    )

    titulo.pack(
        side="left"
    )

    # --------------------------------------------------------
    # FORMULARIO
    # --------------------------------------------------------

    formulario = tk.Frame(
        frame,
        bg=FONDO,
        highlightbackground=BORDE,
        highlightthickness=1
    )

    formulario.pack(
        fill="x",
        padx=18
    )

    # Configuración de columnas
    formulario.grid_columnconfigure(1, weight=1)
    formulario.grid_columnconfigure(3, weight=1)

    # --------------------------------------------------------
    # TÍTULO
    # --------------------------------------------------------

    tk.Label(
        formulario,
        text="Título:",
        font=("Arial", 14, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).grid(
        row=0,
        column=0,
        padx=(22, 10),
        pady=(22, 10),
        sticky="w"
    )

    entry_titulo = crear_entry(formulario)
    entry_titulo.grid(
        row=0,
        column=1,
        padx=5,
        pady=(22, 10),
        sticky="ew"
    )

    # --------------------------------------------------------
    # PERSONA
    # --------------------------------------------------------

    tk.Label(
        formulario,
        text="Persona:",
        font=("Arial", 14, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).grid(
        row=0,
        column=2,
        padx=(45, 10),
        pady=(22, 10),
        sticky="w"
    )

    combo_persona = ttk.Combobox(
        formulario,
        state="readonly",
        style="Material.TCombobox",
        font=("Arial", 12)
    )

    combo_persona.grid(
        row=0,
        column=3,
        padx=(0, 22),
        pady=(22, 10),
        sticky="ew"
    )

    # --------------------------------------------------------
    # AÑO
    # --------------------------------------------------------

    tk.Label(
        formulario,
        text="Año:",
        font=("Arial", 14, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).grid(
        row=1,
        column=0,
        padx=(22, 10),
        pady=10,
        sticky="w"
    )

    entry_anio = crear_entry(formulario, 15)
    entry_anio.grid(
        row=1,
        column=1,
        padx=5,
        pady=10,
        sticky="w"
    )

    # --------------------------------------------------------
    # DESCRIPCIÓN
    # --------------------------------------------------------

    tk.Label(
        formulario,
        text="Descripción:",
        font=("Arial", 14, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).grid(
        row=1,
        column=2,
        padx=(45, 10),
        pady=10,
        sticky="w"
    )

    entry_descripcion = crear_entry(formulario)
    entry_descripcion.grid(
        row=1,
        column=3,
        padx=(0, 22),
        pady=10,
        sticky="ew"
    )

    # --------------------------------------------------------
    # UBICACIÓN
    # --------------------------------------------------------

    tk.Label(
        formulario,
        text="Ubicación:",
        font=("Arial", 14, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).grid(
        row=2,
        column=0,
        padx=(22, 10),
        pady=10,
        sticky="w"
    )

    combo_ubicacion = ttk.Combobox(
        formulario,
        state="readonly",
        values=[
            "Biblioteca",
            "Archivo",
            "Sala A",
            "Sala B",
            "Freire",
            "Depósito"
        ],
        style="Material.TCombobox",
        font=("Arial", 12)
    )

    combo_ubicacion.grid(
        row=2,
        column=1,
        padx=5,
        pady=10,
        sticky="ew"
    )

    # --------------------------------------------------------
    # CATEGORÍA
    # --------------------------------------------------------

    tk.Label(
        formulario,
        text="Categoría:",
        font=("Arial", 14, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).grid(
        row=2,
        column=2,
        padx=(45, 10),
        pady=10,
        sticky="w"
    )

    combo_categoria = ttk.Combobox(
        formulario,
        state="readonly",
        style="Material.TCombobox",
        font=("Arial", 12)
    )

    combo_categoria.grid(
        row=2,
        column=3,
        padx=(0, 22),
        pady=10,
        sticky="ew"
    )

    # --------------------------------------------------------
    # AUTOR
    # --------------------------------------------------------

    tk.Label(
        formulario,
        text="Autor:",
        font=("Arial", 14, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).grid(
        row=3,
        column=0,
        padx=(22, 10),
        pady=10,
        sticky="w"
    )

    combo_autor = ttk.Combobox(
        formulario,
        state="readonly",
        style="Material.TCombobox",
        font=("Arial", 12)
    )

    combo_autor.grid(
        row=3,
        column=1,
        padx=5,
        pady=10,
        sticky="ew"
    )

    # --------------------------------------------------------
    # COLECCIÓN
    # --------------------------------------------------------

    tk.Label(
        formulario,
        text="Colección:",
        font=("Arial", 14, "bold"),
        bg=FONDO,
        fg=TEXTO
    ).grid(
        row=3,
        column=2,
        padx=(45, 10),
        pady=10,
        sticky="w"
    )

    combo_coleccion = ttk.Combobox(
        formulario,
        state="readonly",
        style="Material.TCombobox",
        font=("Arial", 12)
    )

    combo_coleccion.grid(
        row=3,
        column=3,
        padx=(0, 22),
        pady=10,
        sticky="ew"
    )

    # --------------------------------------------------------
    # BOTONES
    # --------------------------------------------------------

    botones = tk.Frame(
        formulario,
        bg=FONDO
    )

    botones.grid(
        row=4,
        column=0,
        columnspan=4,
        pady=(20, 25),
        padx=20,
        sticky="ew"
    )

    for i in range(5):
        botones.columnconfigure(i, weight=1)

    def boton(parent, texto, comando, color):
        return tk.Button(
            parent,
            text=texto,
            command=comando,
            font=("Arial", 13, "bold"),
            bg=color,
            fg="white",
            activebackground=BORDEAUX_OSCURO,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            height=2
        )

    # --------------------------------------------------------
    # TABLA
    # --------------------------------------------------------

    tabla_frame = tk.Frame(
        frame,
        bg=FONDO
    )

    tabla_frame.pack(
        fill="both",
        expand=True,
        padx=18,
        pady=(20, 0)
    )

    columnas = (
        "titulo",
        "anio",
        "descripcion",
        "ubicacion",
        "id_tipo",
        "id_autor",
        "id_persona",
        "id_categoria",
        "id_coleccion"
    )

    tabla = ttk.Treeview(
        tabla_frame,
        columns=columnas,
        show="headings",
        style="Material.Treeview"
    )

    nombres_columnas = {
        "titulo": "Título",
        "anio": "Año",
        "descripcion": "Descripción",
        "ubicacion": "Ubicación",
        "id_tipo": "Id_Tipo",
        "id_autor": "Id_Autor",
        "id_persona": "Id_Persona",
        "id_categoria": "Id_Categoria",
        "id_coleccion": "Id_Coleccion"
    }

    anchos = {
        "titulo": 150,
        "anio": 80,
        "descripcion": 190,
        "ubicacion": 130,
        "id_tipo": 90,
        "id_autor": 100,
        "id_persona": 110,
        "id_categoria": 120,
        "id_coleccion": 120
    }

    for columna in columnas:

        tabla.heading(
            columna,
            text=nombres_columnas[columna]
        )

        tabla.column(
            columna,
            width=anchos[columna],
            anchor="center"
        )

    scrollbar_y = ttk.Scrollbar(
        tabla_frame,
        orient="vertical",
        command=tabla.yview
    )

    scrollbar_x = ttk.Scrollbar(
        tabla_frame,
        orient="horizontal",
        command=tabla.xview
    )

    tabla.configure(
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set
    )

    tabla.pack(
        side="top",
        fill="both",
        expand=True
    )

    scrollbar_y.pack(
        side="right",
        fill="y"
    )

    scrollbar_x.pack(
        side="bottom",
        fill="x"
    )

    # --------------------------------------------------------
    # TOTAL
    # --------------------------------------------------------

    total_label = tk.Label(
        frame,
        text="Total de registros: 0",
        font=("Arial", 14, "bold"),
        bg=FONDO,
        fg=BORDEAUX_OSCURO
    )

    total_label.pack(
        anchor="w",
        padx=30,
        pady=15
    )

    # ========================================================
    # CARGAR COMBOS
    # ========================================================

    def cargar_combos():

        # PERSONAS
        personas_map.clear()
        personas_nombres = []

        for persona in personas:

            id_persona = (
                persona.get("id_persona")
                or persona.get("id")
            )

            nombre = (
                persona.get("nombre")
                or persona.get("nombre_completo")
                or persona.get("apellido")
                or f"Persona {id_persona}"
            )

            personas_map[nombre] = id_persona
            personas_nombres.append(nombre)

        combo_persona["values"] = personas_nombres

        # AUTORES
        autores_map.clear()
        autores_nombres = []

        for autor in autores:

            id_autor = (
                autor.get("id_autor")
                or autor.get("id")
            )

            nombre = (
                autor.get("nombre")
                or autor.get("nombre_completo")
                or autor.get("apellido")
                or f"Autor {id_autor}"
            )

            autores_map[nombre] = id_autor
            autores_nombres.append(nombre)

        combo_autor["values"] = autores_nombres

        # CATEGORÍAS
        categorias_map.clear()
        categorias_nombres = []

        for categoria in categorias:

            id_categoria = (
                categoria.get("id_categoria")
                or categoria.get("id")
            )

            nombre = (
                categoria.get("nombre")
                or categoria.get("categoria")
                or categoria.get("descripcion")
                or f"Categoría {id_categoria}"
            )

            categorias_map[nombre] = id_categoria
            categorias_nombres.append(nombre)

        combo_categoria["values"] = categorias_nombres

        # COLECCIONES
        colecciones_map.clear()
        colecciones_nombres = []

        for coleccion in colecciones:

            id_coleccion = (
                coleccion.get("id_coleccion")
                or coleccion.get("id")
            )

            nombre = (
                coleccion.get("nombre")
                or coleccion.get("coleccion")
                or coleccion.get("descripcion")
                or f"Colección {id_coleccion}"
            )

            colecciones_map[nombre] = id_coleccion
            colecciones_nombres.append(nombre)

        combo_coleccion["values"] = colecciones_nombres

    cargar_combos()

    # ========================================================
    # OBTENER MATERIALES
    # ========================================================

    materiales = []

    def cargar_materiales():

        nonlocal materiales

        try:

            respuesta = requests.get(
                API_URL,
                timeout=5
            )

            if respuesta.status_code != 200:

                messagebox.showerror(
                    "Error",
                    "No se pudieron cargar los materiales."
                )

                return

            materiales = respuesta.json()

            mostrar_materiales(materiales)

        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                f"No se pudo conectar con el backend.\n\n{error}"
            )

    # ========================================================
    # MOSTRAR TABLA
    # ========================================================

    def mostrar_materiales(lista):

        for item in tabla.get_children():
            tabla.delete(item)

        for material in lista:

            tabla.insert(
                "",
                "end",
                values=(
                    material.get("titulo", ""),
                    material.get("anio", ""),
                    material.get("descripcion", ""),
                    material.get("ubicacion", ""),
                    material.get("id_tipo", ""),
                    material.get("id_autor", ""),
                    material.get("id_persona", ""),
                    material.get("id_categoria", ""),
                    material.get("id_coleccion", "")
                )
            )

        total_label.config(
            text=f"Total de registros: {len(lista)}"
        )

    # ========================================================
    # LIMPIAR CAMPOS
    # ========================================================

    def limpiar():

        nonlocal material_seleccionado

        entry_titulo.delete(0, tk.END)
        entry_anio.delete(0, tk.END)
        entry_descripcion.delete(0, tk.END)

        combo_ubicacion.set("")
        combo_persona.set("")
        combo_categoria.set("")
        combo_autor.set("")
        combo_coleccion.set("")

        material_seleccionado["id"] = None

        tabla.selection_remove(
            tabla.selection()
        )

    # ========================================================
    # AGREGAR
    # ========================================================

    def agregar():

        titulo = entry_titulo.get().strip()
        anio = entry_anio.get().strip()
        descripcion = entry_descripcion.get().strip()
        ubicacion = combo_ubicacion.get()

        persona = combo_persona.get()
        autor = combo_autor.get()
        categoria = combo_categoria.get()
        coleccion = combo_coleccion.get()

        if not titulo:
            messagebox.showwarning(
                "Falta información",
                "Ingresá el título del material."
            )
            return

        if not anio:
            messagebox.showwarning(
                "Falta información",
                "Ingresá el año."
            )
            return

        if not ubicacion:
            messagebox.showwarning(
                "Falta información",
                "Seleccioná una ubicación."
            )
            return

        if persona not in personas_map:
            messagebox.showwarning(
                "Falta información",
                "Seleccioná una persona."
            )
            return

        if autor not in autores_map:
            messagebox.showwarning(
                "Falta información",
                "Seleccioná un autor."
            )
            return

        if categoria not in categorias_map:
            messagebox.showwarning(
                "Falta información",
                "Seleccioná una categoría."
            )
            return

        if coleccion not in colecciones_map:
            messagebox.showwarning(
                "Falta información",
                "Seleccioná una colección."
            )
            return

        datos = {
            "titulo": titulo,
            "anio": int(anio),
            "descripcion": descripcion,
            "ubicacion": ubicacion,

            # Cambialo si manejás tipos desde otro combo.
            "id_tipo": 1,

            "id_autor": autores_map[autor],
            "id_persona": personas_map[persona],
            "id_categoria": categorias_map[categoria],
            "id_coleccion": colecciones_map[coleccion]
        }

        try:

            respuesta = requests.post(
                API_URL,
                json=datos,
                timeout=5
            )

            if respuesta.status_code == 201:

                messagebox.showinfo(
                    "Correcto",
                    "Material agregado correctamente."
                )

                limpiar()
                cargar_materiales()

            else:

                try:
                    error = respuesta.json()
                    mensaje = error.get(
                        "detalle",
                        error.get("error", "Error desconocido")
                    )
                except:
                    mensaje = respuesta.text

                messagebox.showerror(
                    "Error",
                    mensaje
                )

        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                str(error)
            )

    # ========================================================
    # SELECCIONAR FILA
    # ========================================================

    def seleccionar_material(event=None):

        seleccion = tabla.selection()

        if not seleccion:
            return

        item = tabla.item(
            seleccion[0]
        )

        valores = item["values"]

        if not valores:
            return

        # Buscar el material completo para obtener id_material
        titulo = valores[0]

        material = None

        for m in materiales:

            if (
                str(m.get("titulo", "")) == str(titulo)
                and str(m.get("anio", "")) == str(valores[1])
            ):
                material = m
                break

        if not material:
            return

        material_seleccionado["id"] = (
            material.get("id_material")
            or material.get("id")
        )

        # Campos
        entry_titulo.delete(0, tk.END)
        entry_titulo.insert(
            0,
            material.get("titulo", "")
        )

        entry_anio.delete(0, tk.END)
        entry_anio.insert(
            0,
            material.get("anio", "")
        )

        entry_descripcion.delete(0, tk.END)
        entry_descripcion.insert(
            0,
            material.get("descripcion", "")
        )

        combo_ubicacion.set(
            material.get("ubicacion", "")
        )

        # Buscar nombre por ID
        id_persona = material.get("id_persona")
        id_autor = material.get("id_autor")
        id_categoria = material.get("id_categoria")
        id_coleccion = material.get("id_coleccion")

        for nombre, id_ in personas_map.items():
            if str(id_) == str(id_persona):
                combo_persona.set(nombre)
                break

        for nombre, id_ in autores_map.items():
            if str(id_) == str(id_autor):
                combo_autor.set(nombre)
                break

        for nombre, id_ in categorias_map.items():
            if str(id_) == str(id_categoria):
                combo_categoria.set(nombre)
                break

        for nombre, id_ in colecciones_map.items():
            if str(id_) == str(id_coleccion):
                combo_coleccion.set(nombre)
                break

    tabla.bind(
        "<<TreeviewSelect>>",
        seleccionar_material
    )

    # ========================================================
    # MODIFICAR
    # ========================================================

    def modificar():

        id_material = material_seleccionado["id"]

        if not id_material:

            messagebox.showwarning(
                "Modificar",
                "Seleccioná un material de la tabla."
            )

            return

        titulo = entry_titulo.get().strip()
        anio = entry_anio.get().strip()
        descripcion = entry_descripcion.get().strip()
        ubicacion = combo_ubicacion.get()

        persona = combo_persona.get()
        autor = combo_autor.get()
        categoria = combo_categoria.get()
        coleccion = combo_coleccion.get()

        if not titulo or not anio:
            messagebox.showwarning(
                "Falta información",
                "Completá título y año."
            )
            return

        datos = {
            "titulo": titulo,
            "anio": int(anio),
            "descripcion": descripcion,
            "ubicacion": ubicacion,
            "id_tipo": 1,
            "id_autor": autores_map.get(autor),
            "id_persona": personas_map.get(persona),
            "id_categoria": categorias_map.get(categoria),
            "id_coleccion": colecciones_map.get(coleccion)
        }

        try:

            respuesta = requests.put(
                f"{API_URL}/{id_material}",
                json=datos,
                timeout=5
            )

            if respuesta.status_code == 200:

                messagebox.showinfo(
                    "Correcto",
                    "Material actualizado correctamente."
                )

                limpiar()
                cargar_materiales()

            else:

                try:
                    error = respuesta.json()
                    mensaje = error.get(
                        "detalle",
                        error.get("error", "Error desconocido")
                    )
                except:
                    mensaje = respuesta.text

                messagebox.showerror(
                    "Error",
                    mensaje
                )

        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                str(error)
            )

    # ========================================================
    # ELIMINAR
    # ========================================================

    def eliminar():

        id_material = material_seleccionado["id"]

        if not id_material:

            messagebox.showwarning(
                "Eliminar",
                "Seleccioná un material de la tabla."
            )

            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Querés eliminar el material seleccionado?"
        )

        if not confirmar:
            return

        try:

            respuesta = requests.delete(
                f"{API_URL}/{id_material}",
                timeout=5
            )

            if respuesta.status_code == 200:

                messagebox.showinfo(
                    "Correcto",
                    "Material eliminado correctamente."
                )

                limpiar()
                cargar_materiales()

            else:

                try:
                    error = respuesta.json()
                    mensaje = error.get(
                        "detalle",
                        error.get("error", "Error desconocido")
                    )
                except:
                    mensaje = respuesta.text

                messagebox.showerror(
                    "Error",
                    mensaje
                )

        except requests.exceptions.RequestException as error:

            messagebox.showerror(
                "Error de conexión",
                str(error)
            )

    # ========================================================
    # BUSCAR
    # ========================================================

    def buscar():

        texto = entry_titulo.get().strip().lower()

        if not texto:

            mostrar_materiales(materiales)

            return

        filtrados = []

        for material in materiales:

            titulo = str(
                material.get("titulo", "")
            ).lower()

            descripcion = str(
                material.get("descripcion", "")
            ).lower()

            ubicacion = str(
                material.get("ubicacion", "")
            ).lower()

            if (
                texto in titulo
                or texto in descripcion
                or texto in ubicacion
            ):

                filtrados.append(material)

        mostrar_materiales(filtrados)

    # ========================================================
    # BOTONES
    # ========================================================

    boton(
        botones,
        "＋  Agregar",
        agregar,
        BORDEAUX
    ).grid(
        row=0,
        column=0,
        padx=8,
        sticky="ew"
    )

    boton(
        botones,
        "✎  Modificar",
        modificar,
        GRIS
    ).grid(
        row=0,
        column=1,
        padx=8,
        sticky="ew"
    )

    boton(
        botones,
        "▣  Eliminar",
        eliminar,
        GRIS
    ).grid(
        row=0,
        column=2,
        padx=8,
        sticky="ew"
    )

    boton(
        botones,
        "⌕  Buscar",
        buscar,
        GRIS
    ).grid(
        row=0,
        column=3,
        padx=8,
        sticky="ew"
    )

    boton(
        botones,
        "↻  Limpiar",
        limpiar,
        BORDEAUX
    ).grid(
        row=0,
        column=4,
        padx=8,
        sticky="ew"
    )

    # --------------------------------------------------------
    # CARGAR DATOS INICIALES
    # --------------------------------------------------------

    cargar_materiales()

    return frame