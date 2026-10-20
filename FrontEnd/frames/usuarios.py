import tkinter as tk
from tkinter import ttk, messagebox
import requests


API_URL = "http://localhost:3000/api/usuarios"


def crear_usuario(parent):
    borde = "#690D2D"
    fondo = "#E8EDF0"
    gris = "#59636B"
    blanco = "#FFFFFF"

    frame = tk.Frame(parent, bg=fondo)

    encabezado = tk.Frame(frame, bg=borde)
    encabezado.pack(fill="x", padx=10, pady=(8, 0))

    tk.Label(
        encabezado,
        text="Gestion de Usuarios",
        bg=borde,
        fg=blanco,
        font=("Arial", 15, "bold")
    ).pack(side="left", padx=12, pady=10)

    tk.Label(
        encabezado,
        text="Administracion de usuarios del sistema",
        bg=borde,
        fg=blanco,
        font=("Arial", 8)
    ).pack(side="right", padx=10)

    formulario = tk.Frame(frame, bg=fondo)
    formulario.pack(fill="x", padx=10, pady=8)

    tk.Label(
        formulario,
        text="ID Usuario:",
        bg=fondo,
        font=("Arial", 9, "bold")
    ).grid(row=0, column=0, sticky="w", padx=4, pady=5)

    entrada_id = ttk.Entry(formulario, width=22)
    entrada_id.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(
        formulario,
        text="Nombre de usuario:",
        bg=fondo,
        font=("Arial", 9, "bold")
    ).grid(row=0, column=2, sticky="w", padx=4, pady=5)

    entrada_nombre = ttk.Entry(formulario, width=23)
    entrada_nombre.grid(row=0, column=3, padx=5, pady=5)

    tk.Label(
        formulario,
        text="Contrasena:",
        bg=fondo,
        font=("Arial", 9, "bold")
    ).grid(row=1, column=0, sticky="w", padx=4, pady=5)

    entrada_contrasena = ttk.Entry(formulario, width=22, show="*")
    entrada_contrasena.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(
        formulario,
        text="Rol:",
        bg=fondo,
        font=("Arial", 9, "bold")
    ).grid(row=1, column=2, sticky="w", padx=4, pady=5)

    combo_rol = ttk.Combobox(
        formulario,
        values=["administrador", "maestra", "jardinero", "usuario"],
        state="readonly",
        width=20
    )
    combo_rol.set("Seleccione")
    combo_rol.grid(row=1, column=3, padx=5, pady=5)

    tk.Label(
        formulario,
        text="ID Persona:",
        bg=fondo,
        font=("Arial", 9, "bold")
    ).grid(row=2, column=0, sticky="w", padx=4, pady=5)

    entrada_persona = ttk.Entry(formulario, width=22)
    entrada_persona.grid(row=2, column=1, padx=5, pady=5)

    botones = tk.Frame(frame, bg=fondo)
    botones.pack(fill="x", padx=10, pady=(0, 8))

    columnas = (
        "id_usuario",
        "nombre_usuario",
        "contrasena",
        "rol",
        "id_persona"
    )

    tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=8)

    encabezados = {
        "id_usuario": "Id_Usuario",
        "nombre_usuario": "Nombre_Usuario",
        "contrasena": "Contrasena",
        "rol": "Rol",
        "id_persona": "Id_Persona"
    }

    anchos = {
        "id_usuario": 90,
        "nombre_usuario": 150,
        "contrasena": 120,
        "rol": 100,
        "id_persona": 90
    }

    for columna in columnas:
        tabla.heading(columna, text=encabezados[columna])
        tabla.column(columna, width=anchos[columna], anchor="w")

    estilo = ttk.Style()

    try:
        estilo.theme_use("clam")
    except tk.TclError:
        pass

    estilo.configure(
        "Usuarios.Treeview",
        background=blanco,
        fieldbackground=blanco,
        foreground="#222222",
        rowheight=27,
        font=("Arial", 9)
    )

    estilo.configure(
        "Usuarios.Treeview.Heading",
        background=borde,
        foreground=blanco,
        font=("Arial", 9, "bold")
    )

    tabla.configure(style="Usuarios.Treeview")
    tabla.pack(fill="both", expand=True, padx=10, pady=5)

    etiqueta_total = tk.Label(
        frame,
        text="Total de registros: 0",
        bg=fondo,
        fg=borde,
        font=("Arial", 9, "bold")
    )
    etiqueta_total.pack(anchor="w", padx=12, pady=5)

    def limpiar():
        entrada_id.delete(0, tk.END)
        entrada_nombre.delete(0, tk.END)
        entrada_contrasena.delete(0, tk.END)
        entrada_persona.delete(0, tk.END)
        combo_rol.set("Seleccione")
        tabla.selection_remove(tabla.selection())
        entrada_nombre.focus()

    def listar():
        try:
            respuesta = requests.get(API_URL, timeout=5)
            respuesta.raise_for_status()
            usuarios = respuesta.json()

            tabla.delete(*tabla.get_children())

            for usuario in usuarios:
                tabla.insert(
                    "",
                    tk.END,
                    values=(
                        usuario.get("id_usuario", ""),
                        usuario.get("nombre_usuario", ""),
                        "********",
                        usuario.get("rol", ""),
                        usuario.get("id_persona", "")
                    )
                )

            etiqueta_total.config(text=f"Total de registros: {len(usuarios)}")

        except requests.exceptions.RequestException as error:
            messagebox.showerror(
                "Error de conexion",
                f"No se pudieron cargar los usuarios.\n\n{error}"
            )

    def datos_formulario(incluir_contrasena=True):
        nombre = entrada_nombre.get().strip()
        contrasena = entrada_contrasena.get().strip()
        rol = combo_rol.get().strip()
        id_persona = entrada_persona.get().strip()

        if not nombre:
            messagebox.showwarning("Campos incompletos", "Ingrese el usuario.")
            return None

        if incluir_contrasena and not contrasena:
            messagebox.showwarning("Campos incompletos", "Ingrese la contrasena.")
            return None

        if not rol or rol == "Seleccione":
            messagebox.showwarning("Campos incompletos", "Seleccione el rol.")
            return None

        if not id_persona:
            messagebox.showwarning("Campos incompletos", "Ingrese el ID de persona.")
            return None

        return {
            "nombre_usuario": nombre,
            "contrasena": contrasena,
            "rol": rol,
            "id_persona": id_persona
        }

    def agregar():
        datos = datos_formulario()

        if datos is None:
            return

        try:
            respuesta = requests.post(API_URL, json=datos, timeout=5)

            if respuesta.status_code == 201:
                messagebox.showinfo("Exito", "Usuario agregado correctamente.")
                limpiar()
                listar()
            else:
                messagebox.showerror("Error", respuesta.text)

        except requests.exceptions.RequestException as error:
            messagebox.showerror("Error de conexion", str(error))

    def modificar():
        id_usuario = entrada_id.get().strip()

        if not id_usuario:
            messagebox.showwarning("Seleccionar usuario", "Seleccione un usuario de la tabla.")
            return

        datos = datos_formulario()

        if datos is None:
            return

        try:
            respuesta = requests.put(f"{API_URL}/{id_usuario}", json=datos, timeout=5)

            if respuesta.status_code == 200:
                messagebox.showinfo("Exito", "Usuario actualizado correctamente.")
                limpiar()
                listar()
            else:
                messagebox.showerror("Error", respuesta.text)

        except requests.exceptions.RequestException as error:
            messagebox.showerror("Error de conexion", str(error))

    def eliminar():
        id_usuario = entrada_id.get().strip()

        if not id_usuario:
            messagebox.showwarning("Seleccionar usuario", "Seleccione un usuario de la tabla.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminacion",
            "Esta seguro de eliminar este usuario?"
        )

        if not confirmar:
            return

        try:
            respuesta = requests.delete(f"{API_URL}/{id_usuario}", timeout=5)

            if respuesta.status_code == 200:
                messagebox.showinfo("Exito", "Usuario eliminado correctamente.")
                limpiar()
                listar()
            else:
                messagebox.showerror("Error", respuesta.text)

        except requests.exceptions.RequestException as error:
            messagebox.showerror("Error de conexion", str(error))

    def seleccionar_usuario(event=None):
        seleccion = tabla.selection()

        if not seleccion:
            return

        valores = tabla.item(seleccion[0], "values")

        if not valores:
            return

        entrada_id.delete(0, tk.END)
        entrada_nombre.delete(0, tk.END)
        entrada_contrasena.delete(0, tk.END)
        entrada_persona.delete(0, tk.END)

        entrada_id.insert(0, valores[0])
        entrada_nombre.insert(0, valores[1])
        combo_rol.set(valores[3])
        entrada_persona.insert(0, valores[4])

    def crear_boton(texto, comando, color):
        boton = tk.Button(
            botones,
            text=texto,
            command=comando,
            font=("Arial", 9, "bold"),
            bg=color,
            fg=blanco,
            activebackground=borde,
            activeforeground=blanco,
            relief="flat",
            cursor="hand2"
        )
        boton.pack(side="left", fill="x", expand=True, padx=4, ipady=6)

    crear_boton("Agregar", agregar, borde)
    crear_boton("Modificar", modificar, gris)
    crear_boton("Eliminar", eliminar, gris)
    crear_boton("Limpiar", limpiar, borde)

    tabla.bind("<<TreeviewSelect>>", seleccionar_usuario)
    listar()

    return frame
