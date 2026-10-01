import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# ---------------- VENTANA PRINCIPAL ----------------
ventana = tk.Tk()
ventana.title("Archivo Histórico")
ventana.geometry("800x500")
ventana.resizable(False, False)
ventana.configure(bg="#f5f6f8")

# ---------------- COLORES ----------------
BORDO = "#800033"
BLANCO = "#ffffff"
GRIS = "#f5f6f8"
GRIS_TEXTO = "#8a96a3"

# ---------------- CONTENEDOR PRINCIPAL ----------------
contenedor = tk.Frame(ventana, bg=BLANCO)
contenedor.pack(fill="both", expand=True, padx=5, pady=5)

# ---------------- PANEL IZQUIERDO ----------------
panel_izquierdo = tk.Frame(
    contenedor,
    bg="#3b2727",
    width=260,
    height=490
)
panel_izquierdo.pack(side="left", fill="y")
panel_izquierdo.pack_propagate(False)

# Cargar la imagen y recortar el sector izquierdo
try:
    imagen = Image.open("login.png")

    # Recorta aproximadamente el panel izquierdo de la imagen
    imagen = imagen.crop((0, 0, 260, 322))
    imagen = imagen.resize((260, 490))

    imagen_fondo = ImageTk.PhotoImage(imagen)

    etiqueta_imagen = tk.Label(
        panel_izquierdo,
        image=imagen_fondo,
        bd=0
    )
    etiqueta_imagen.place(x=0, y=0, relwidth=1, relheight=1)

except:
    # Si no encuentra la imagen
    tk.Label(
        panel_izquierdo,
        text="📜\n\nARCHIVO\nHISTÓRICO",
        font=("Arial", 22, "bold"),
        fg="white",
        bg="#3b2727"
    ).place(relx=0.5, rely=0.5, anchor="center")


# ---------------- PANEL DERECHO ----------------
panel_derecho = tk.Frame(
    contenedor,
    bg=GRIS
)
panel_derecho.pack(
    side="right",
    fill="both",
    expand=True
)

# ---------------- TÍTULO ----------------
titulo = tk.Label(
    panel_derecho,
    text="Iniciar Sesión",
    font=("Arial", 20, "bold"),
    fg=BORDO,
    bg=GRIS
)
titulo.pack(pady=(75, 20))


# ---------------- CAMPO USUARIO ----------------
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
).pack(side="left", padx=12)

entrada_usuario = tk.Entry(
    usuario_frame,
    font=("Arial", 12),
    fg=GRIS_TEXTO,
    bg=BLANCO,
    bd=0
)
entrada_usuario.pack(
    side="left",
    fill="x",
    expand=True,
    padx=5
)

entrada_usuario.insert(0, "Usuario")


# ---------------- CAMPO CONTRASEÑA ----------------
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
).pack(side="left", padx=12)

entrada_password = tk.Entry(
    password_frame,
    font=("Arial", 12),
    fg=GRIS_TEXTO,
    bg=BLANCO,
    bd=0,
    show="*"
)
entrada_password.pack(
    side="left",
    fill="x",
    expand=True,
    padx=5
)

entrada_password.insert(0, "Contraseña")


# ---------------- FUNCIÓN INGRESAR ----------------
def ingresar():
    usuario = entrada_usuario.get()
    contraseña = entrada_password.get()

    if usuario == "" or usuario == "Usuario":
        messagebox.showwarning(
            "Advertencia",
            "Ingrese un usuario."
        )
    elif contraseña == "" or contraseña == "Contraseña":
        messagebox.showwarning(
            "Advertencia",
            "Ingrese una contraseña."
        )
    else:
        messagebox.showinfo(
            "Archivo Histórico",
            "Inicio de sesión correcto."
        )


# ---------------- BOTÓN INGRESAR ----------------
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
    command=ingresar
)

boton_ingresar.pack(
    padx=85,
    fill="x",
    ipady=8
)


# ---------------- EJECUTAR ----------------
ventana.mainloop()