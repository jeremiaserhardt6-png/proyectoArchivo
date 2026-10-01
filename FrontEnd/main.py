import tkinter as tk
from frames.materiales import crear_materiales

ventana = tk.Tk()
ventana.title("NombreApp")
ventana.geometry("800x500")

def mostrar_frame(funcion_frame):
    for widget in contenedor.winfo_children():
        widget.destroy()
    frame= funcion_frame(contenedor)
    frame.pack(fill="both", expand=True)

def mostrar_menu():
    menu=tk.Frame(ventana, bg="red", height=60) 
    menu.pack(side="top", fill="x")
    
    global contenedor 
    contenedor = tk.Frame(ventana, bg="white")
    contenedor.pack(fill="both", expand=True)
    
    tk.Button(menu, text="materiales", command=lambda: mostrar_frame(crear_materiales)).pack(side="left", padx=10, pady=10)

mostrar_menu()
ventana.mainloop()