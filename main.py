# main.py
import tkinter as tk
# Importamos la clase de la interfaz desde el archivo menu.py
from gui.menu import InterfazKinesiologia 

if __name__ == "__main__":
    # 1. Crea la raíz de la ventana (el objeto principal de Tkinter)
    root = tk.Tk()
    
    # 2. Inicializa la interfaz gráfica, pasando la raíz como master
    app = InterfazKinesiologia(master=root)
    
    # 3. Inicia el bucle principal de Tkinter.
    # La aplicación se mantendrá activa hasta que se cierre la ventana.
    root.mainloop()