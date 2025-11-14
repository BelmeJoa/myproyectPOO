# gui/menu.py
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from services.gestion_kinesiologia import GestionKinesiologia
from models.paciente import Paciente 
from models.turno import Turno
from utils.validador import Validador # Necesario para la validación de entrada

class InterfazKinesiologia(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Sistema de Gestión Kinésica - Tkinter")
        self.manager = GestionKinesiologia() # Controlador / Service
        self.pack(fill="both", expand=True)
        self.crear_widgets()
        
    def crear_widgets(self):
        # Configuración inicial de la ventana
        self.master.geometry("500x350")
        
        # Etiqueta principal
        tk.Label(self, text="Gestión de Pacientes Kinésicos", font=('Helvetica', 18, 'bold')).pack(pady=20)

        # Frame para los botones principales
        frame_crud = tk.Frame(self)
        frame_crud.pack(pady=10)

        # Botones de Funcionalidad
        tk.Button(frame_crud, text="1. Registrar Paciente (C)", command=self.abrir_registro).grid(row=0, column=0, padx=10, pady=5, ipadx=5)
        tk.Button(frame_crud, text="2. Buscar Paciente (R)", command=self.abrir_busqueda).grid(row=0, column=1, padx=10, pady=5, ipadx=5)
        tk.Button(frame_crud, text="3. Actualizar Paciente (U)", command=self.abrir_actualizacion).grid(row=1, column=0, padx=10, pady=5, ipadx=5)
        tk.Button(frame_crud, text="4. Eliminar Paciente (D)", command=self.abrir_eliminacion).grid(row=1, column=1, padx=10, pady=5, ipadx=5)
        tk.Button(frame_crud, text="5. Generar Reporte", command=self.generar_reporte).grid(row=2, column=0, columnspan=2, pady=15, ipadx=20)
        
        # Botón 6: Salir
        tk.Button(self, text="6. SALIR", command=self.master.quit, bg='red', fg='white').pack(pady=10)


    # =======================================================
    # 1. FORMULARIO DE REGISTRO (CREATE)
    # =======================================================

    def abrir_registro(self):
        # Usamos Toplevel para crear una ventana secundaria
        self.ventana_registro = tk.Toplevel(self.master)
        self.ventana_registro.title("Registrar Nuevo Paciente")
        self.ventana_registro.geometry("350x300")
        
        campos = ["DNI", "Nombre", "Apellido", "F. Nacimiento (AAAA-MM-DD)", "Historia Clínica", "Obra Social"]
        self.entradas_registro = {}
        
        for i, campo in enumerate(campos):
            tk.Label(self.ventana_registro, text=f"{campo}:").grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entrada = tk.Entry(self.ventana_registro)
            entrada.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entradas_registro[campo] = entrada
            
        tk.Button(self.ventana_registro, text="Guardar Paciente", 
                  command=self.ejecutar_registro).grid(row=len(campos), column=0, columnspan=2, pady=10)

    def ejecutar_registro(self):
        datos = {k: v.get() for k, v in self.entradas_registro.items()}
        
        # VALIDACIONES
        if not Validador.validar_dni(datos['DNI']):
            return messagebox.showerror("Error", "DNI inválido (debe tener 7 u 8 dígitos).")
        if not Validador.validar_fecha(datos['F. Nacimiento (AAAA-MM-DD)']):
            return messagebox.showerror("Error", "Fecha inválida (formato AAAA-MM-DD o fecha futura).")

        try:
            nuevo_paciente = Paciente(
                datos['DNI'], datos['Nombre'], datos['Apellido'], 
                datos['F. Nacimiento (AAAA-MM-DD)'], datos['Historia Clínica'], datos['Obra Social']
            )
            
            if self.manager.registrar_paciente(nuevo_paciente):
                messagebox.showinfo("Éxito", "✅ Paciente registrado exitosamente.")
                self.ventana_registro.destroy()
            else:
                messagebox.showerror("Error de BD", "❌ Error al registrar paciente. DNI o HC duplicados.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")


    # =======================================================
    # 2. BUSQUEDA (READ)
    # =======================================================

    def abrir_busqueda(self):
        dni_buscar = simpledialog.askstring("Búsqueda", "Ingrese el DNI del paciente a buscar:", parent=self.master)
        if dni_buscar:
            paciente = self.manager.buscar_paciente_por_dni(dni_buscar)
            
            if paciente:
                info = (f"Paciente Encontrado:\n\n"
                        f"DNI: {paciente.get_dni()}\n"
                        f"Nombre: {paciente.get_nombre()} {paciente._apellido}\n"
                        f"Nacimiento: {paciente._fecha_nacimiento}\n"
                        f"Historia Clínica: {paciente._historia_clinica}\n"
                        f"Obra Social: {paciente._obra_social}")
                messagebox.showinfo("Resultado de Búsqueda", info)
            else:
                messagebox.showwarning("Resultado de Búsqueda", f"Paciente con DNI {dni_buscar} no encontrado.")

    # =======================================================
    # 3. ACTUALIZACIÓN (UPDATE)
    # =======================================================

    def abrir_actualizacion(self):
        # Esta es la parte más compleja, la implementamos en dos pasos: buscar y luego actualizar
        dni_actualizar = simpledialog.askstring("Actualización", "Ingrese el DNI del paciente a actualizar:", parent=self.master)
        if not dni_actualizar:
            return

        paciente = self.manager.buscar_paciente_por_dni(dni_actualizar)
        if not paciente:
            return messagebox.showwarning("Error", "Paciente no encontrado.")

        self.mostrar_formulario_actualizacion(paciente)

    def mostrar_formulario_actualizacion(self, paciente):
        self.ventana_actualizacion = tk.Toplevel(self.master)
        self.ventana_actualizacion.title(f"Actualizar a {paciente.get_nombre()} {paciente._apellido}")
        self.ventana_actualizacion.geometry("350x300")
        
        campos = ["Nombre", "Apellido", "F. Nacimiento (AAAA-MM-DD)", "Historia Clínica", "Obra Social"]
        datos_actuales = [paciente.get_nombre(), paciente._apellido, paciente._fecha_nacimiento, paciente._historia_clinica, paciente._obra_social]
        self.entradas_actualizacion = {}
        
        for i, campo in enumerate(campos):
            tk.Label(self.ventana_actualizacion, text=f"{campo}:").grid(row=i, column=0, padx=5, pady=5, sticky="w")
            entrada = tk.Entry(self.ventana_actualizacion)
            entrada.insert(0, str(datos_actuales[i])) # Precarga los datos
            entrada.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entradas_actualizacion[campo] = entrada
            
        tk.Button(self.ventana_actualizacion, text="Confirmar Actualización", 
                  command=lambda: self.ejecutar_actualizacion(paciente)).grid(row=len(campos), column=0, columnspan=2, pady=10)

    def ejecutar_actualizacion(self, paciente):
        datos = {k: v.get() for k, v in self.entradas_actualizacion.items()}

        # Asignar los nuevos valores al objeto Paciente (sin cambiar el DNI original)
        paciente.set_nombre(datos['Nombre'])
        paciente._apellido = datos['Apellido']
        paciente._fecha_nacimiento = datos['F. Nacimiento (AAAA-MM-DD)']
        paciente._historia_clinica = datos['Historia Clínica']
        paciente._obra_social = datos['Obra Social']
        
        # Validación de fecha y edad mínima
        if not Validador.validar_fecha(paciente._fecha_nacimiento):
            return messagebox.showerror("Error", "Fecha o edad no válida.")
        
        if self.manager.actualizar_paciente(paciente):
            messagebox.showinfo("Éxito", f"✅ Paciente {paciente.get_dni()} actualizado correctamente.")
            self.ventana_actualizacion.destroy()
        else:
            messagebox.showerror("Error", "❌ No se pudo actualizar el paciente en la BD.")

    # =======================================================
    # 4. ELIMINACIÓN (DELETE)
    # =======================================================

    def abrir_eliminacion(self):
        dni_eliminar = simpledialog.askstring("Eliminar Paciente", "Ingrese el DNI del paciente a eliminar:", parent=self.master)
        if dni_eliminar:
            confirmar = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al paciente con DNI {dni_eliminar}? Esta acción es irreversible.")
            
            if confirmar:
                if self.manager.eliminar_paciente(dni_eliminar):
                    messagebox.showinfo("Éxito", f"✅ Paciente con DNI {dni_eliminar} eliminado exitosamente.")
                else:
                    messagebox.showerror("Error", f"❌ No se encontró o no se pudo eliminar el paciente con DNI {dni_eliminar}.")

    # =======================================================
    # 5. REPORTE (REPORT)
    # =======================================================

    def generar_reporte(self):
        pacientes = self.manager.obtener_todos_pacientes()
        
        if not pacientes:
            return messagebox.showwarning("Reporte", "No hay pacientes registrados en la base de datos.")
            
        self.ventana_reporte = tk.Toplevel(self.master)
        self.ventana_reporte.title(f"Reporte de Pacientes ({len(pacientes)} en Total)")
        self.ventana_reporte.geometry("600x400")
        
        reporte_texto = scrolledtext.ScrolledText(self.ventana_reporte, width=80, height=20, font=('Courier', 10))
        reporte_texto.pack(pady=10, padx=10, fill="both", expand=True)

        # Encabezado
        reporte_texto.insert(tk.END, f"--- REPORTE DE PACIENTES KINÉSICOS (Total: {len(pacientes)}) ---\n")
        reporte_texto.insert(tk.END, "DNI         | APELLIDO, NOMBRE      | HC NRO.    | OBRA SOCIAL\n")
        reporte_texto.insert(tk.END, "------------|-----------------------|------------|-------------------\n")

        # Cargar los datos
        for p in pacientes:
            dni, nombre, apellido, hc, obra_social = p
            linea = f"{dni:<11} | {apellido}, {nombre:<10} | {hc:<10} | {obra_social}\n"
            reporte_texto.insert(tk.END, linea)

        reporte_texto.config(state=tk.DISABLED) # Deshabilita la edición
    # --- Ventana Secundaria de Gestión de Turnos ---

    def abrir_gestion_turnos(self):
        self.ventana_turnos = tk.Toplevel(self.master)
        self.ventana_turnos.title("Gestión de Turnos")
        self.ventana_turnos.geometry("300x250")
        
        tk.Label(self.ventana_turnos, text="Opciones de Turnos", font=('Helvetica', 14, 'bold')).pack(pady=10)

        # Botones CRUD para Turnos
        tk.Button(self.ventana_turnos, text="1. Registrar Nuevo Turno", 
                  command=self.abrir_registro_turno).pack(pady=5, fill='x', padx=20)
        
        tk.Button(self.ventana_turnos, text="2. Buscar Turno (ID)", 
                  command=self.ejecutar_busqueda_turno).pack(pady=5, fill='x', padx=20)
        
        tk.Button(self.ventana_turnos, text="3. Cancelar Turno (Eliminar)", 
                  command=self.ejecutar_eliminacion_turno).pack(pady=5, fill='x', padx=20)
        
        # ... Aquí podrías añadir botones de Actualizar Turno y Reporte de Turnos...

    # --- Lógica CRUD para Turnos ---
    
    def abrir_registro_turno(self):
        # En la práctica, se debería usar un formulario Toplevel, pero usaremos simpledialogs por simplicidad
        paciente_dni = simpledialog.askstring("Registro Turno", "DNI del Paciente:", parent=self.ventana_turnos)
        fecha = simpledialog.askstring("Registro Turno", "Fecha (AAAA-MM-DD):", parent=self.ventana_turnos)
        hora = simpledialog.askstring("Registro Turno", "Hora (HH:MM):", parent=self.ventana_turnos)
        tratamiento = simpledialog.askstring("Registro Turno", "Tratamiento:", parent=self.ventana_turnos)

        if paciente_dni and fecha and hora:
            # 1. Verificar si el paciente existe
            if not self.manager.buscar_paciente_por_dni(paciente_dni):
                 return messagebox.showwarning("Error", "El DNI del paciente no está registrado.")

            # 2. Crear el objeto Turno (ID se pone como 0 o None porque la BD lo genera)
            nuevo_turno = Turno(None, paciente_dni, fecha, hora, tratamiento) 
            
            # 3. Llamar al Service para guardar
            if self.manager.registrar_turno(nuevo_turno):
                messagebox.showinfo("Éxito", "✅ Turno registrado exitosamente.")
            else:
                messagebox.showerror("Error", "❌ Error al registrar el turno en la BD.")

    def ejecutar_busqueda_turno(self):
        id_buscar = simpledialog.askinteger("Buscar Turno", "Ingrese el ID del Turno a buscar:", parent=self.ventana_turnos)
        if id_buscar is not None:
            turno = self.manager.buscar_turno_por_id(id_buscar)
            if turno:
                info = (f"Turno Encontrado:\n"
                        f"ID: {turno.get_id()}\n"
                        f"DNI Paciente: {turno.get_paciente_dni()}\n"
                        f"Fecha: {turno.get_fecha()} a las {turno.get_hora()}\n"
                        f"Tratamiento: {turno._tratamiento}")
                messagebox.showinfo("Resultado de Búsqueda", info)
            else:
                messagebox.showwarning("Resultado", f"Turno con ID {id_buscar} no encontrado.")

    def ejecutar_eliminacion_turno(self):
        id_eliminar = simpledialog.askinteger("Cancelar Turno", "Ingrese el ID del Turno a cancelar:", parent=self.ventana_turnos)
        if id_eliminar is not None:
            confirmar = messagebox.askyesno("Confirmar", f"¿Seguro que desea cancelar el Turno ID {id_eliminar}?")
            if confirmar:
                if self.manager.eliminar_turno(id_eliminar):
                    messagebox.showinfo("Éxito", f"✅ Turno ID {id_eliminar} cancelado correctamente.")
                else:
                    messagebox.showerror("Error", f"❌ No se encontró o no se pudo cancelar el Turno ID {id_eliminar}.")


