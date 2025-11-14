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
        tk.Button(frame_crud, text="6. Gestion de Turnos", command=self.abrir_gestion_turnos).grid(row=3, column=0, columnspan=2, pady=15, ipadx=20)

        # Botón 6: Salir
        tk.Button(self, text="7. SALIR", command=self.master.quit, bg='red', fg='white').pack(pady=10)


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
        # Ajusta el tamaño para que se vea bien
        self.ventana_turnos.geometry("350x250") 
        
        tk.Label(self.ventana_turnos, text="Opciones de Turnos", font=('Helvetica', 14, 'bold')).pack(pady=10)

        # 1. Registro de Turno (Llama al nuevo formulario limpio)
        tk.Button(self.ventana_turnos, text="1. Registrar Nuevo Turno", 
                  command=self.abrir_registro_turno).pack(pady=5, fill='x', padx=20)
        
        # 2. Búsqueda Flexible y Cancelación
        # (Llama a la ventana que permite buscar por DNI o Fecha)
        tk.Button(self.ventana_turnos, text="2. Buscar y Gestionar Turnos (DNI/Fecha)", 
                  command=self.abrir_gestion_busqueda_turnos).pack(pady=5, fill='x', padx=20)

        # 3. Listado Completo (Para ver todos los IDs/información si es necesario)
        tk.Button(self.ventana_turnos, text="3. Listar Todos los Turnos (Ver IDs)",
                  command=self.ejecutar_listado_turnos).pack(pady=5, fill='x', padx=20)
        
        # Opcional: Botón para cerrar esta ventana
        tk.Button(self.ventana_turnos, text="Cerrar Menú", 
                  command=self.ventana_turnos.destroy).pack(pady=10)

    def abrir_registro_turno(self):
        #"""Abre un formulario Toplevel para registrar un nuevo turno."""
    
        # 1.     Crear Ventana
        ventana = tk.Toplevel(self.master)
        ventana.title("Registrar Nuevo Turno")
        ventana.geometry("400x350")
    
        # 2. Variables para almacenar los datos
        self.dni_var = tk.StringVar()
        self.fecha_var = tk.StringVar()
        self.hora_var = tk.StringVar()
        self.tratamiento_var = tk.StringVar()
    
        # 3. Diseño del Formulario
        campos = [
            ("DNI Paciente (Obligatorio):", self.dni_var),
            ("Fecha (AAAA-MM-DD):", self.fecha_var),
            ("Hora (HH:MM):", self.hora_var),
            ("Tratamiento:", self.tratamiento_var),
        ]

        for texto, var in campos:
            frame = tk.Frame(ventana)
            tk.Label(frame, text=texto, width=20, anchor='w').pack(side='left', padx=5, pady=5)
            tk.Entry(frame, textvariable=var, width=30).pack(side='right', padx=5, pady=5)
            frame.pack(fill='x', padx=20)
        
        # 4. Botón de Confirmación
        tk.Button(ventana, text="Confirmar Turno", 
                command=lambda: self.guardar_nuevo_turno(ventana)).pack(pady=20)

        # Botones CRUD para Turnos
        tk.Button(self.ventana_turnos, text="1. Registrar Nuevo Turno", 
                  command=self.abrir_registro_turno).pack(pady=5, fill='x', padx=20)

        # NUEVO BOTÓN PARA GESTIONAR BÚSQUEDA Y CANCELACIÓN
        tk.Button(self.ventana_turnos, text="2. Buscar y Gestionar Turnos (DNI/Fecha)", 
                  command=self.abrir_gestion_busqueda_turnos).pack(pady=5, fill='x', padx=20)

        tk.Button(self.ventana_turnos, text="3. Listar Todos los Turnos (Ver IDs)", # Listado para ver todos los IDs
                  command=self.ejecutar_busqueda_flexible).pack(pady=5, fill='x', padx=20)


    def guardar_nuevo_turno(self, ventana):
        """Lógica para guardar el turno desde el formulario."""
        paciente_dni = self.dni_var.get()
        fecha = self.fecha_var.get()
        hora = self.hora_var.get()
        tratamiento = self.tratamiento_var.get()
        
        # Validaciones básicas
        if not paciente_dni or not fecha or not hora:
            messagebox.showerror("Error", "Los campos DNI, Fecha y Hora son obligatorios.")
            return

        # 1. Verificar si el paciente existe
        if not self.manager.buscar_paciente_por_dni(paciente_dni):
            return messagebox.showwarning("Error", "❌ El DNI del paciente no está registrado. Registre primero al paciente.")

        # 2. Creamos el objeto Turno (ID se pasa como None porque la BD lo genera)
        # IMPORTANTE: El ID del turno es generado por la BD
        nuevo_turno = Turno(None, paciente_dni, fecha, hora, tratamiento) 
        
        # 3. Llamar al Service para guardar
        if self.manager.registrar_turno(nuevo_turno):
            messagebox.showinfo("Éxito", "✅ Turno registrado exitosamente.")
            ventana.destroy() # Cierra la ventana después de guardar
        else:
            messagebox.showerror("Error", "❌ Error al registrar el turno en la BD.")
    # gui/menu.py (Dentro de la clase InterfazKinesiologia)

    def abrir_gestion_busqueda_turnos(self):
        """Abre la ventana para buscar turnos por criterio."""

        ventana_busqueda = tk.Toplevel(self.master)
        ventana_busqueda.title("Buscar Turnos por Criterio")
        ventana_busqueda.geometry("500x450")

        tk.Label(ventana_busqueda, text="Buscar Turnos", font=('Helvetica', 14, 'bold')).pack(pady=10)

        # 1. Selección de Criterio
        self.criterio_busqueda_var = tk.StringVar(value='paciente_dni') # DNI por defecto

        frame_criterio = tk.Frame(ventana_busqueda)
        tk.Label(frame_criterio, text="Buscar por:").pack(side='left', padx=10)
        tk.Radiobutton(frame_criterio, text="DNI Paciente", variable=self.criterio_busqueda_var, 
                    value='paciente_dni').pack(side='left')
        tk.Radiobutton(frame_criterio, text="Fecha (AAAA-MM-DD)", variable=self.criterio_busqueda_var, 
                    value='fecha').pack(side='left')
        frame_criterio.pack(pady=10)

        # 2. Campo de Valor de Búsqueda
        self.valor_busqueda_var = tk.StringVar()
        tk.Label(ventana_busqueda, text="Ingrese Valor:").pack(pady=5)
        tk.Entry(ventana_busqueda, textvariable=self.valor_busqueda_var, width=40).pack(pady=5)

        # 3. Botón de Búsqueda
        tk.Button(ventana_busqueda, text="Buscar Turnos", 
                command=lambda: self.ejecutar_busqueda_flexible(ventana_busqueda)).pack(pady=15)

        # 4. Área para mostrar resultados (Usaremos ScrolledText)
        self.caja_resultados_turnos = scrolledtext.ScrolledText(ventana_busqueda, width=60, height=10, font=('Consolas', 10))
        self.caja_resultados_turnos.pack(pady=10, padx=10)
        self.caja_resultados_turnos.insert(tk.END, "Aquí se mostrarán los resultados de la búsqueda.")
        self.caja_resultados_turnos.config(state=tk.DISABLED)


    def ejecutar_busqueda_flexible(self, ventana_busqueda):
        """Llama al servicio con el criterio seleccionado y muestra los resultados."""
        criterio = self.criterio_busqueda_var.get()
        valor = self.valor_busqueda_var.get()

        if not valor:
            return messagebox.showwarning("Advertencia", "Debe ingresar un valor de búsqueda.")

        # 1. Llamar al servicio mejorado
        turnos = self.manager.buscar_turnos_por_criterio(criterio, valor)

        self.caja_resultados_turnos.config(state=tk.NORMAL)
        self.caja_resultados_turnos.delete('1.0', tk.END) # Limpiar resultados anteriores

        if not turnos:
            self.caja_resultados_turnos.insert(tk.END, f"No se encontraron turnos para {valor} ({criterio}).")
        else:
            self.caja_resultados_turnos.insert(tk.END, f"TURNOS ENCONTRADOS para {criterio.upper()}: {valor}\n\n")
            for t in turnos:
                self.caja_resultados_turnos.insert(tk.END, 
                    f"  [ID: {t.get_id()}] | Hora: {t.get_hora()} | DNI: {t.get_paciente_dni()}\n"
                    f"  Fecha: {t.get_fecha()} | Tratamiento: {t._tratamiento}\n"
                    f"{'-'*60}\n"
                )

            # Añadir opción de cancelación
            tk.Label(ventana_busqueda, text="Para Cancelar, ingrese el ID:").pack(pady=5)
            self.id_cancelar_var = tk.StringVar()
            tk.Entry(ventana_busqueda, textvariable=self.id_cancelar_var, width=10).pack(pady=5)
            tk.Button(ventana_busqueda, text="Cancelar Turno por ID", 
                    command=lambda: self.ejecutar_cancelacion_desde_busqueda(self.id_cancelar_var.get(), ventana_busqueda)).pack(pady=10)


        self.caja_resultados_turnos.config(state=tk.DISABLED)

    def ejecutar_cancelacion_desde_busqueda(self, turno_id, ventana_busqueda):
        """Cancela un turno después de haber sido listado en la búsqueda flexible."""
        try:
            id_a_cancelar = int(turno_id)
        except ValueError:
            return messagebox.showerror("Error", "El ID debe ser un número entero.")

        if messagebox.askyesno("Confirmar Cancelación", f"¿Está seguro de cancelar el turno con ID: {id_a_cancelar}?"):
            if self.manager.eliminar_turno(id_a_cancelar):
                messagebox.showinfo("Éxito", f"✅ Turno con ID {id_a_cancelar} cancelado exitosamente.")
                ventana_busqueda.destroy() # Cierra la ventana de búsqueda
                self.abrir_gestion_turnos().focus_set() # Vuelve al menú de gestión
            else:
                messagebox.showerror("Error", "❌ No se pudo cancelar el turno. Verifique el ID.")