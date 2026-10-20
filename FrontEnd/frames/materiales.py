import tkinter as tk
from tkinter import ttk, messagebox
import requests

API_BASE = "http://localhost:3000/api"
API_URL = f"{API_BASE}/materiales"
AUTORES_URL = f"{API_BASE}/autores"
PERSONAS_URL = f"{API_BASE}/personas"
CATEGORIAS_URL = f"{API_BASE}/categorias"
COLECCIONES_URL = f"{API_BASE}/colecciones"
TIPOS_URL = f"{API_BASE}/tipos-material"


def crear_materiales(parent):
    frame = tk.Frame(parent, bg="#f1f2f3")

    borde = "#64132e"
    bordo = "#7c1738"
    gris = "#666b70"
    fondo = "#f1f2f3"
    blanco = "#ffffff"
    texto = "#151515"

    material_seleccionado = {"id": None}
    materiales_cache = {}
    autores_map = {}
    personas_map = {}
    categorias_map = {}
    colecciones_map = {}
    tipos_map = {}

    style = ttk.Style()
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        "Material.Treeview",
        background=blanco,
        foreground=texto,
        rowheight=28,
        fieldbackground=blanco,
        font=("Arial", 10)
    )
    style.configure(
        "Material.Treeview.Heading",
        background=bordo,
        foreground=blanco,
        font=("Arial", 10, "bold")
    )

    encabezado = tk.Frame(frame, bg=borde, height=58)
    encabezado.pack(fill="x", padx=12, pady=(10, 12))
    encabezado.pack_propagate(False)

    tk.Label(
        encabezado,
        text="Gestión de Materiales",
        font=("Arial", 18, "bold"),
        bg=borde,
        fg=blanco
    ).pack(side="left", padx=18)

    formulario = tk.Frame(frame, bg=fondo)
    formulario.pack(fill="x", padx=18, pady=(0, 10))
    for columna in (1, 3):
        formulario.grid_columnconfigure(columna, weight=1)

    def label(texto_label, fila, columna):
        tk.Label(
            formulario,
            text=texto_label,
            font=("Arial", 10, "bold"),
            bg=fondo,
            fg=texto
        ).grid(row=fila, column=columna, sticky="w", padx=(0, 8), pady=5)

    def entry(fila, columna, ancho=25):
        campo = tk.Entry(
            formulario,
            width=ancho,
            font=("Arial", 10),
            bg=blanco,
            fg=texto,
            relief="solid",
            bd=1
        )
        campo.grid(row=fila, column=columna, sticky="ew", padx=(0, 18), pady=5)
        return campo

    def combo(fila, columna):
        campo = ttk.Combobox(formulario, state="readonly", font=("Arial", 10))
        campo.grid(row=fila, column=columna, sticky="ew", padx=(0, 18), pady=5)
        return campo

    label("Título:", 0, 0)
    entry_titulo = entry(0, 1)

    label("Año:", 0, 2)
    entry_anio = entry(0, 3, 12)

    label("Descripción:", 1, 0)
    entry_descripcion = entry(1, 1)

    label("Ubicación:", 1, 2)
    combo_ubicacion = ttk.Combobox(
        formulario,
        state="readonly",
        values=["Biblioteca", "Archivo", "Sala A", "Sala B", "Freire", "Depósito"],
        font=("Arial", 10)
    )
    combo_ubicacion.grid(row=1, column=3, sticky="ew", padx=(0, 18), pady=5)

    label("Autor:", 2, 0)
    combo_autor = combo(2, 1)

    label("Persona:", 2, 2)
    combo_persona = combo(2, 3)

    label("Categoría:", 3, 0)
    combo_categoria = combo(3, 1)

    label("Colección:", 3, 2)
    combo_coleccion = combo(3, 3)

    label("Tipo de material:", 4, 0)
    combo_tipo = combo(4, 1)

    botones = tk.Frame(frame, bg=fondo)
    botones.pack(fill="x", padx=18, pady=(0, 10))

    tabla_frame = tk.Frame(frame, bg=fondo)
    tabla_frame.pack(fill="both", expand=True, padx=18)

    columnas = (
        "id_material", "titulo", "anio", "descripcion", "ubicacion",
        "tipo_material", "autor", "persona", "categoria", "coleccion"
    )

    encabezados = {
        "id_material": "ID",
        "titulo": "Título",
        "anio": "Año",
        "descripcion": "Descripción",
        "ubicacion": "Ubicación",
        "tipo_material": "Tipo de material",
        "autor": "Autor",
        "persona": "Persona",
        "categoria": "Categoría",
        "coleccion": "Colección"
    }

    tabla = ttk.Treeview(
        tabla_frame,
        columns=columnas,
        show="headings",
        style="Material.Treeview"
    )

    for columna in columnas:
        tabla.heading(columna, text=encabezados[columna])
        tabla.column(columna, width=125, anchor="center")

    tabla.column("id_material", width=55)
    tabla.column("titulo", width=160)
    tabla.column("descripcion", width=180)
    tabla.column("tipo_material", width=150)

    scroll_y = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
    scroll_x = ttk.Scrollbar(tabla_frame, orient="horizontal", command=tabla.xview)
    tabla.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    tabla.pack(side="top", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")

    total_label = tk.Label(
        frame,
        text="Total de registros: 0",
        font=("Arial", 10, "bold"),
        bg=fondo,
        fg=borde
    )
    total_label.pack(anchor="w", padx=22, pady=8)

    def obtener_lista(url, mapa, combo_widget, campos_nombre, id_posibles):
        """Carga un catálogo en un combo y conserva el ID asociado a cada opción."""
        mapa.clear()
        try:
            respuesta = requests.get(url, timeout=5)
            respuesta.raise_for_status()
            registros = respuesta.json()
            if not isinstance(registros, list):
                raise ValueError("La API no devolvió una lista.")
        except (requests.exceptions.RequestException, ValueError) as error:
            combo_widget["values"] = []
            combo_widget.set("")
            messagebox.showwarning(
                "No se pudo cargar el catálogo",
                f"No se pudieron cargar los datos desde:\n{url}\n\n{error}"
            )
            return

        nombres = []
        for registro in registros:
            id_registro = next(
                (registro.get(campo) for campo in id_posibles if registro.get(campo) is not None),
                None
            )
            partes = [
                str(registro.get(campo) or "").strip()
                for campo in campos_nombre
                if str(registro.get(campo) or "").strip()
            ]
            nombre = " ".join(partes) or f"Registro {id_registro}"
            if id_registro is None:
                continue
            # El ID queda incluido en la etiqueta para evitar nombres duplicados ambiguos.
            etiqueta = f"{nombre} (ID: {id_registro})"
            mapa[etiqueta] = id_registro
            nombres.append(etiqueta)

        combo_widget["values"] = nombres

    def obtener_autores():
        obtener_lista(AUTORES_URL, autores_map, combo_autor,
                      ["nombre", "apellido"], ["id_autor", "id", "id_autores"])

    def obtener_personas():
        obtener_lista(PERSONAS_URL, personas_map, combo_persona,
                      ["nombre", "apellido"], ["id_persona", "id"])

    def obtener_categorias():
        obtener_lista(CATEGORIAS_URL, categorias_map, combo_categoria,
                      ["nombre"], ["id_categoria", "id"])

    def obtener_colecciones():
        obtener_lista(COLECCIONES_URL, colecciones_map, combo_coleccion,
                      ["nombre"], ["id_coleccion", "id"])

    def obtener_tipos():
        obtener_lista(TIPOS_URL, tipos_map, combo_tipo,
                      ["nombredeltipo", "nombre", "tipo"], ["id_tipo", "id"])

    def limpiar():
        material_seleccionado["id"] = None
        for campo in (
            entry_titulo, entry_anio, entry_descripcion
        ):
            campo.delete(0, tk.END)
        for campo in (
            combo_ubicacion, combo_autor, combo_persona,
            combo_categoria, combo_coleccion, combo_tipo
        ):
            campo.set("")
        tabla.selection_remove(tabla.selection())
        entry_titulo.focus()

    def datos_formulario():
        titulo = entry_titulo.get().strip()
        anio = entry_anio.get().strip()
        descripcion = entry_descripcion.get().strip()
        ubicacion = combo_ubicacion.get().strip()

        if not titulo or not anio or not ubicacion:
            messagebox.showwarning(
                "Campos incompletos",
                "Completá título, año y ubicación."
            )
            return None

        if not anio.isdigit():
            messagebox.showwarning("Dato inválido", "El año debe ser un número entero.")
            return None

        selecciones = [
            (combo_autor.get(), autores_map, "autor"),
            (combo_persona.get(), personas_map, "persona"),
            (combo_categoria.get(), categorias_map, "categoría"),
            (combo_coleccion.get(), colecciones_map, "colección"),
            (combo_tipo.get(), tipos_map, "tipo de material")
        ]
        for valor, mapa, nombre in selecciones:
            if valor not in mapa:
                messagebox.showwarning(
                    "Campos incompletos",
                    f"Seleccioná un elemento válido para {nombre}."
                )
                return None

        return {
            "titulo": titulo,
            "anio": int(anio),
            "descripcion": descripcion,
            "ubicacion": ubicacion,
            "id_tipo": int(tipos_map[combo_tipo.get()]),
            "id_autor": int(autores_map[combo_autor.get()]),
            "id_persona": int(personas_map[combo_persona.get()]),
            "id_categoria": int(categorias_map[combo_categoria.get()]),
            "id_coleccion": int(colecciones_map[combo_coleccion.get()])
        }

    def cargar_materiales(mostrar_error=True):
        try:
            respuesta = requests.get(API_URL, timeout=5)
            respuesta.raise_for_status()
            materiales = respuesta.json()
            if not isinstance(materiales, list):
                raise ValueError("La API no devolvió una lista.")
        except (requests.exceptions.RequestException, ValueError) as error:
            if mostrar_error:
                messagebox.showerror(
                    "Error de conexión",
                    f"No se pudieron cargar los materiales.\n\n{error}"
                )
            return

        tabla.delete(*tabla.get_children())
        materiales_cache.clear()

        for material in materiales:
            id_material = material.get("id_material")
            if id_material is None:
                continue
            materiales_cache[str(id_material)] = material
            valores = tuple(material.get(columna) or "" for columna in columnas)
            tabla.insert("", tk.END, values=valores)

        total_label.config(text=f"Total de registros: {len(materiales)}")

    def seleccionar_material(event=None):
        seleccion = tabla.selection()
        if not seleccion:
            return

        valores = tabla.item(seleccion[0], "values")
        if not valores:
            return

        id_material = str(valores[0])
        material = materiales_cache.get(id_material)
        if not material:
            return

        material_seleccionado["id"] = id_material

        entry_titulo.delete(0, tk.END)
        entry_titulo.insert(0, material.get("titulo") or "")

        entry_anio.delete(0, tk.END)
        entry_anio.insert(0, material.get("anio") or "")

        entry_descripcion.delete(0, tk.END)
        entry_descripcion.insert(0, material.get("descripcion") or "")

        combo_ubicacion.set(material.get("ubicacion") or "")

        def seleccionar_por_id(combo_widget, mapa, id_valor):
            for etiqueta, id_mapa in mapa.items():
                if str(id_mapa) == str(id_valor):
                    combo_widget.set(etiqueta)
                    return
            combo_widget.set("")

        seleccionar_por_id(combo_autor, autores_map, material.get("id_autor"))
        seleccionar_por_id(combo_persona, personas_map, material.get("id_persona"))
        seleccionar_por_id(combo_categoria, categorias_map, material.get("id_categoria"))
        seleccionar_por_id(combo_coleccion, colecciones_map, material.get("id_coleccion"))
        seleccionar_por_id(combo_tipo, tipos_map, material.get("id_tipo"))

    def agregar():
        datos = datos_formulario()
        if datos is None:
            return
        try:
            respuesta = requests.post(API_URL, json=datos, timeout=5)
            if respuesta.status_code == 201:
                messagebox.showinfo("Correcto", "Material agregado correctamente.")
                limpiar()
                cargar_materiales()
            else:
                messagebox.showerror("Error", respuesta.text)
        except requests.exceptions.RequestException as error:
            messagebox.showerror("Error de conexión", str(error))

    def modificar():
        id_material = material_seleccionado["id"]
        if not id_material:
            messagebox.showwarning("Modificar", "Seleccioná un material de la tabla.")
            return

        datos = datos_formulario()
        if datos is None:
            return
        try:
            respuesta = requests.put(f"{API_URL}/{id_material}", json=datos, timeout=5)
            if respuesta.status_code == 200:
                messagebox.showinfo("Correcto", "Material actualizado correctamente.")
                limpiar()
                cargar_materiales()
            else:
                messagebox.showerror("Error", respuesta.text)
        except requests.exceptions.RequestException as error:
            messagebox.showerror("Error de conexión", str(error))

    def eliminar():
        id_material = material_seleccionado["id"]
        if not id_material:
            messagebox.showwarning("Eliminar", "Seleccioná un material de la tabla.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Estás seguro de eliminar el material seleccionado?"
        )
        if not confirmar:
            return

        try:
            respuesta = requests.delete(f"{API_URL}/{id_material}", timeout=5)
            if respuesta.status_code == 200:
                messagebox.showinfo("Correcto", "Material eliminado correctamente.")
                limpiar()
                cargar_materiales()
            else:
                messagebox.showerror("Error", respuesta.text)
        except requests.exceptions.RequestException as error:
            messagebox.showerror("Error de conexión", str(error))

    def buscar():
        texto_busqueda = entry_busqueda.get().strip().lower()
        if not texto_busqueda:
            cargar_materiales()
            return

        for item in tabla.get_children():
            valores = tabla.item(item, "values")
            texto_fila = " ".join(str(valor).lower() for valor in valores)
            if texto_busqueda not in texto_fila:
                tabla.delete(item)

        total_label.config(text=f"Resultados encontrados: {len(tabla.get_children())}")

    busqueda_frame = tk.Frame(frame, bg=fondo)
    busqueda_frame.pack(fill="x", padx=18, pady=(0, 8))
    tk.Label(
        busqueda_frame,
        text="Buscar material:",
        font=("Arial", 10, "bold"),
        bg=fondo,
        fg=texto
    ).pack(side="left", padx=(0, 8))

    entry_busqueda = tk.Entry(busqueda_frame, font=("Arial", 10), relief="solid", bd=1)
    entry_busqueda.pack(side="left", fill="x", expand=True, padx=(0, 8))
    entry_busqueda.bind("<Return>", lambda event: buscar())

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
            cursor="hand2"
        ).pack(side="left", fill="x", expand=True, padx=4, ipady=7)

    crear_boton("Agregar", agregar, bordo)
    crear_boton("Modificar", modificar, gris)
    crear_boton("Eliminar", eliminar, gris)
    crear_boton("Buscar", buscar, gris)
    crear_boton("Limpiar", limpiar, bordo)
    crear_boton("Actualizar lista", cargar_materiales, bordo)

    tabla.bind("<<TreeviewSelect>>", seleccionar_material)

    # Cargar catálogos. Si alguna ruta no existe en el backend, ese desplegable quedará vacío.
    obtener_autores()
    obtener_personas()
    obtener_categorias()
    obtener_colecciones()
    obtener_tipos()
    cargar_materiales()

    return frame


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Gestión de materiales")
    root.geometry("1200x750")
    crear_materiales(root).pack(fill="both", expand=True)
    root.mainloop()
