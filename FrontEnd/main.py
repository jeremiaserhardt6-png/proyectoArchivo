import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests

from frames.inicio import crear_inicio


# ============================================================
# FUNCIONES
# ============================================================

def mostrar_inicio():
    global contenedor

    # Eliminar todos los widgets de la ventana
    for widget in ventana.winfo_children():
        widget.destroy()

    # Crear contenedor principal
    contenedor = tk.Frame(
        ventana,
        bg="#eef1f5"
    )

    contenedor.pack(
        fill="both",
        expand=True
    )

    # Crear pantalla de inicio
    frame_inicio = crear_inicio(contenedor)

    frame_inicio.pack(
        fill="both",
        expand=True
    )


def iniciar_sesion():
    usuario = entrada_usuario.get().strip()
    contraseña = entrada_password.get()

    # Verificar campos vacíos
    if usuario == "" or usuario == "Usuario":
        messagebox.showwarning(
            "Campos vacíos",
            "Ingrese su usuario."
        )
        entrada_usuario.focus()
        return

    if contraseña == "" or contraseña == "Contraseña":
        messagebox.showwarning(
            "Campos vacíos",
            "Ingrese su contraseña."
        )
        entrada_password.focus()
        return

    datos = {
        "nombre_usuario": usuario,
        "contrasena": contraseña
    }

    try:
        respuesta = requests.post(
            "http://localhost:3000/api/login",
            json=datos,
            timeout=5
        )

        if respuesta.status_code == 200:

            messagebox.showinfo(
                "Inicio de sesión",
                "¡Bienvenido!"
            )

            mostrar_inicio()

        elif respuesta.status_code == 401:

            messagebox.showerror(
                "Error",
                "Usuario o contraseña incorrectos."
            )

        else:

            messagebox.showerror(
                "Error",
                f"Ocurrió un error al iniciar sesión.\n"
                f"Código: {respuesta.status_code}"
            )

    except requests.exceptions.ConnectionError:

        messagebox.showerror(
            "Error de conexión",
            "No se pudo conectar con el servidor.\n\n"
            "Verifique que el servidor esté ejecutándose."
        )

    except requests.exceptions.Timeout:

        messagebox.showerror(
            "Tiempo agotado",
            "El servidor tardó demasiado en responder."
        )

    except requests.exceptions.RequestException as error:

        messagebox.showerror(
            "Error",
            f"Ocurrió un error:\n{error}"
        )


# ============================================================
# VENTANA PRINCIPAL
# ============================================================

ventana = tk.Tk()

ventana.title("Archivo Histórico")
ventana.geometry("800x500")
ventana.resizable(False, False)
ventana.configure(bg="#f5f6f8")


# ============================================================
# COLORES
# ============================================================

BORDO = "#800033"
BLANCO = "#ffffff"
GRIS = "#f5f6f8"
GRIS_TEXTO = "#8a96a3"


# ============================================================
# CONTENEDOR PRINCIPAL
# ============================================================

contenedor = tk.Frame(
    ventana,
    bg=BLANCO
)

contenedor.pack(
    fill="both",
    expand=True,
    padx=5,
    pady=5
)


# ============================================================
# PANEL IZQUIERDO
# ============================================================

panel_izquierdo = tk.Frame(
    contenedor,
    bg="#3b2727",
    width=260,
    height=490
)

panel_izquierdo.pack(
    side="left",
    fill="y"
)

panel_izquierdo.pack_propagate(False)


# ============================================================
# IMAGEN DEL PANEL IZQUIERDO
# ============================================================

try:

    imagen = Image.open("login.png")

    # Recortar la parte izquierda de la imagen
    imagen = imagen.crop(
        (0, 0, 260, 322)
    )

    # Redimensionar
    imagen = imagen.resize(
        (260, 490),
        Image.Resampling.LANCZOS
    )

    imagen_fondo = ImageTk.PhotoImage(imagen)

    etiqueta_imagen = tk.Label(
        panel_izquierdo,
        image=imagen_fondo,
        bd=0
    )

    etiqueta_imagen.image = imagen_fondo

    etiqueta_imagen.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )

except Exception:

    tk.Label(
        panel_izquierdo,
        text="📜\n\nARCHIVO\nHISTÓRICO",
        font=("Arial", 22, "bold"),
        fg=BLANCO,
        bg="#3b2727"
    ).place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )


# ============================================================
# PANEL DERECHO
# ============================================================

panel_derecho = tk.Frame(
    contenedor,
    bg=GRIS
)

panel_derecho.pack(
    side="right",
    fill="both",
    expand=True
)


# ============================================================
# TÍTULO
# ============================================================

titulo = tk.Label(
    panel_derecho,
    text="Iniciar Sesión",
    font=("Arial", 20, "bold"),
    fg=BORDO,
    bg=GRIS
)

titulo.pack(
    pady=(75, 20)
)


# ============================================================
# CAMPO USUARIO
# ============================================================

usuario_frame = tk.Frame(
    panel_derecho,
    bg=BLANCO,
    highlightbackground="#b8c1ca",
    highlightthickness=1
)

usuario_frame.pack(
    padx=85,
    fill="x",
    ipady=7
)


tk.Label(
    usuario_frame,
    text="♟",
    font=("Arial", 15),
    fg="#111111",
    bg=BLANCO
).pack(
    side="left",
    padx=12
)


entrada_usuario = tk.Entry(
    usuario_frame,
    font=("Arial", 12),
    fg="#111111",
    bg=BLANCO,
    bd=0
)

entrada_usuario.pack(
    side="left",
    fill="x",
    expand=True,
    padx=5
)


# Placeholder del usuario
entrada_usuario.insert(
    0,
    "Usuario"
)

entrada_usuario.config(
    fg=GRIS_TEXTO
)


def limpiar_usuario(event):
    if entrada_usuario.get() == "Usuario":
        entrada_usuario.delete(0, tk.END)
        entrada_usuario.config(fg="#111111")


def restaurar_usuario(event):
    if entrada_usuario.get() == "":
        entrada_usuario.insert(0, "Usuario")
        entrada_usuario.config(fg=GRIS_TEXTO)


entrada_usuario.bind(
    "<FocusIn>",
    limpiar_usuario
)

entrada_usuario.bind(
    "<FocusOut>",
    restaurar_usuario
)


# ============================================================
# CAMPO CONTRASEÑA
# ============================================================

password_frame = tk.Frame(
    panel_derecho,
    bg=BLANCO,
    highlightbackground="#b8c1ca",
    highlightthickness=1
)

password_frame.pack(
    padx=85,
    pady=15,
    fill="x",
    ipady=7
)


tk.Label(
    password_frame,
    text="🔒",
    font=("Arial", 13),
    fg="#111111",
    bg=BLANCO
).pack(
    side="left",
    padx=12
)


entrada_password = tk.Entry(
    password_frame,
    font=("Arial", 12),
    fg=GRIS_TEXTO,
    bg=BLANCO,
    bd=0
)

entrada_password.pack(
    side="left",
    fill="x",
    expand=True,
    padx=5
)


# Placeholder de contraseña
entrada_password.insert(
    0,
    "Contraseña"
)


def limpiar_password(event):
    if entrada_password.get() == "Contraseña":
        entrada_password.delete(0, tk.END)
        entrada_password.config(
            fg="#111111",
            show="*"
        )


def restaurar_password(event):
    if entrada_password.get() == "":
        entrada_password.config(
            fg=GRIS_TEXTO,
            show=""
        )
        entrada_password.insert(
            0,
            "Contraseña"
        )


entrada_password.bind(
    "<FocusIn>",
    limpiar_password
)

entrada_password.bind(
    "<FocusOut>",
    restaurar_password
)


# ============================================================
# BOTÓN INGRESAR
# ============================================================

boton_ingresar = tk.Button(
    panel_derecho,
    text="↪   Ingresar",
    font=("Arial", 12, "bold"),
    fg=BLANCO,
    bg=BORDO,
    activebackground="#650029",
    activeforeground=BLANCO,
    bd=0,
    cursor="hand2",
    command=iniciar_sesion
)

boton_ingresar.pack(
    padx=85,
    fill="x",
    ipady=8
)


# ============================================================
# ENTER PARA INICIAR SESIÓN
# ============================================================

ventana.bind(
    "<Return>",
    lambda event: iniciar_sesion()
)


# ============================================================
# INICIAR APLICACIÓN
# ============================================================

entrada_usuario.focus()

ventana.mainloop()
