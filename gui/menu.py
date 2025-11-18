# gui/menu.py
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
from services.gestion_kinesiologia import GestionKinesiologia
from models.paciente import Paciente 
from models.turno import Turno
from utils.validador import Validador 
from datetime import date

# --- CONFIGURACIÓN DE ESTILOS ---
COLOR_PRINCIPAL = "#90EE90"  # Verde Manzana (LightGreen)
COLOR_SECUNDARIO = "#B0E0E6" # Azul Celeste (PowderBlue)
COLOR_FONDO = "#F5F5F5"      # Blanco Humo (WhiteSmoke)
COLOR_TEXTO = "#333333"      # Gris oscuro
FUENTE_PRINCIPAL = ('Segoe UI', 10)
FUENTE_TITULO = ('Segoe UI', 18, 'bold')
FUENTE_SUBTITULO = ('Segoe UI', 12, 'bold')


class InterfazKinesiologia(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg=COLOR_FONDO)
        self.master = master
        self.master.title("Sistema de Gestión Kinésica")
        self.master.configure(bg=COLOR_FONDO)
        self.manager = GestionKinesiologia() # Controlador / Service
        self.pack(fill="both", expand=True)
        self.crear_widgets()
        
    def crear_widgets(self):
        # Tamaño ajustado para un mejor layout
        self.master.geometry("650x450") 
        
        # Frame del Título
        frame_titulo = tk.Frame(self, bg=COLOR_SECUNDARIO)
        frame_titulo.pack(fill='x', pady=10)
        tk.Label(frame_titulo, text="🤸 Gestión de Pacientes y Agenda Kinésica 🗓️", 
                 font=FUENTE_TITULO, bg=COLOR_SECUNDARIO, fg=COLOR_TEXTO).pack(pady=10)

        # Frame principal de botones (Centrado con Grid)
        frame_principal = tk.Frame(self, bg=COLOR_FONDO)
        frame_principal.pack(pady=20)

        # Separación y Subtítulo: Módulo Pacientes
        tk.Label(frame_principal, text="--- Módulo Pacientes (CRUD) ---", 
                 font=FUENTE_SUBTITULO, bg=COLOR_FONDO, fg=COLOR_PRINCIPAL).grid(row=0, column=0, columnspan=2, pady=(10, 5), sticky='ew')
        
        # Botones CRUD Pacientes (GRID)
        self._crear_boton(frame_principal, "1. Registrar Paciente (C)", self.abrir_registro, 
                              row=1, column=0, color=COLOR_PRINCIPAL)
        self._crear_boton(frame_principal, "2. Buscar Paciente (R)", self.abrir_busqueda, 
                              row=1, column=1, color=COLOR_PRINCIPAL)
        self._crear_boton(frame_principal, "3. Actualizar Paciente (U)", self.abrir_actualizacion, 
                              row=2, column=0, color=COLOR_PRINCIPAL)
        self._crear_boton(frame_principal, "4. Eliminar Paciente (D)", self.abrir_eliminacion, 
                              row=2, column=1, color=COLOR_PRINCIPAL)
                              
        # Separación y Subtítulo: Reportes y Turnos
        tk.Label(frame_principal, text="--- Agenda y Reportes ---", 
                 font=FUENTE_SUBTITULO, bg=COLOR_FONDO, fg=COLOR_SECUNDARIO).grid(row=3, column=0, columnspan=2, pady=(10, 5), sticky='ew')

        # Botones de Reporte y Turnos
        self._crear_boton(frame_principal, "5. Generar Reporte Pacientes", self.generar_reporte, 
                              row=4, column=0, columnspan=2, color=COLOR_SECUNDARIO)
        self._crear_boton(frame_principal, "6. Gestión de Turnos", self.abrir_gestion_turnos, 
                              row=5, column=0, columnspan=2, color=COLOR_SECUNDARIO)

        # Botón Salir (Abajo)
        tk.Button(self, text="7. SALIR", command=self.master.quit, font=('Segoe UI', 12, 'bold'),
                  bg='#DC143C', fg='white', relief=tk.FLAT, padx=20, pady=5).pack(pady=20)


    def _crear_boton(self, master, texto, comando, row, column, columnspan=1, color=COLOR_PRINCIPAL):
        """Función auxiliar para crear botones con estilo unificado y grid."""
        return tk.Button(master, text=texto, command=comando, font=FUENTE_PRINCIPAL,
                          bg=color, fg=COLOR_TEXTO, relief=tk.RAISED, padx=15, pady=8).grid(
                               row=row, column=column, columnspan=columnspan, padx=10, pady=5, sticky='ew')

    # =======================================================
    # 1. FORMULARIO DE REGISTRO (CREATE)
    # =======================================================

    def abrir_registro(self):
        self.ventana_registro = tk.Toplevel(self.master, bg=COLOR_FONDO)
        self.ventana_registro.title("Registrar Nuevo Paciente")
        self.ventana_registro.geometry("380x320")
        
        campos = ["DNI", "Nombre", "Apellido", "F. Nacimiento (AAAA-MM-DD)", "Historia Clínica", "Obra Social"]
        self.entradas_registro = {}
        
        frame_campos = tk.Frame(self.ventana_registro, bg=COLOR_FONDO)
        frame_campos.pack(padx=10, pady=10) 
        # ----------------------------------------------------
        
        for i, campo in enumerate(campos):
            # Estos elementos usan grid() dentro de frame_campos
            tk.Label(frame_campos, text=f"{campo}:", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_PRINCIPAL).grid(
                row=i, column=0, padx=5, pady=5, sticky="w")
            entrada = tk.Entry(frame_campos, font=FUENTE_PRINCIPAL)
            entrada.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entradas_registro[campo] = entrada
            
        tk.Button(self.ventana_registro, text="Guardar Paciente", font=FUENTE_PRINCIPAL,
                  bg=COLOR_PRINCIPAL, fg=COLOR_TEXTO, relief=tk.FLAT,
                  command=self.ejecutar_registro).pack(pady=10)

    def ejecutar_registro(self):
        datos = {k: v.get() for k, v in self.entradas_registro.items()}
        
        # VALIDACIONES
        if not Validador.validar_dni(datos['DNI']):
            return messagebox.showerror("Error", "DNI inválido (debe tener 7 u 8 dígitos).")
        if not Validador.validar_fecha(datos['F. Nacimiento (AAAA-MM-DD)']):
            return messagebox.showerror("Error", "Fecha inválida (formato AAAA-MM-DD).")

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
                        f"Nombre: {paciente.get_nombre()} {paciente.get_apellido()}\n"
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
        dni_actualizar = simpledialog.askstring("Actualización", "Ingrese el DNI del paciente a actualizar:", parent=self.master)
        if not dni_actualizar:
            return

        paciente = self.manager.buscar_paciente_por_dni(dni_actualizar)
        if not paciente:
            return messagebox.showwarning("Error", "Paciente no encontrado.")

        self.mostrar_formulario_actualizacion(paciente)

    def mostrar_formulario_actualizacion(self, paciente):
        self.ventana_actualizacion = tk.Toplevel(self.master, bg=COLOR_FONDO)
        self.ventana_actualizacion.title(f"Actualizar a {paciente.get_nombre()} {paciente.get_apellido()}")
        self.ventana_actualizacion.geometry("380x320")
        
        campos = ["Nombre", "Apellido", "F. Nacimiento (AAAA-MM-DD)", "Historia Clínica", "Obra Social"]
        datos_actuales = [paciente.get_nombre(), paciente.get_apellido(), paciente._fecha_nacimiento, paciente._historia_clinica, paciente._obra_social]
        
        self.entradas_actualizacion = {}
        
        frame_campos = tk.Frame(self.ventana_actualizacion, bg=COLOR_FONDO)
        frame_campos.pack(padx=10, pady=10)

        for i, campo in enumerate(campos):
            tk.Label(frame_campos, text=f"{campo}:", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_PRINCIPAL).grid(
                row=i, column=0, padx=5, pady=5, sticky="w")
            entrada = tk.Entry(frame_campos, font=FUENTE_PRINCIPAL)
            entrada.insert(0, str(datos_actuales[i])) 
            entrada.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
            self.entradas_actualizacion[campo] = entrada
            
        tk.Button(self.ventana_actualizacion, text="Confirmar Actualización", font=FUENTE_PRINCIPAL,
                  bg=COLOR_SECUNDARIO, fg=COLOR_TEXTO, relief=tk.FLAT,
                  command=lambda: self.ejecutar_actualizacion(paciente)).pack(pady=10)

    def ejecutar_actualizacion(self, paciente):
        datos = {k: v.get() for k, v in self.entradas_actualizacion.items()}

        # Asignar los nuevos valores al objeto Paciente
        paciente.set_nombre(datos['Nombre'])
        paciente.set_apellido(datos['Apellido']) 
        paciente._fecha_nacimiento = datos['F. Nacimiento (AAAA-MM-DD)']
        paciente.set_historia_clinica(datos['Historia Clínica']) 
        paciente.set_obra_social(datos['Obra Social']) 
        
        # Validación de fecha 
        if not Validador.validar_fecha(paciente._fecha_nacimiento):
            return messagebox.showerror("Error", "Fecha de nacimiento no válida.")
        
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
            
        
        # Encabezado
        reporte_texto = f"--- REPORTE DE PACIENTES KINÉSICOS (Total: {len(pacientes)}) ---\n"
        reporte_texto += "DNI         | APELLIDO, NOMBRE       | HC NRO.    | OBRA SOCIAL\n"
        reporte_texto += "------------|------------------------|------------|-------------------\n"

        # Cargar los datos
        for dni, nombre, apellido, hc, obra_social in pacientes:
            linea = f"{dni:<11} | {apellido}, {nombre:<10} | {hc:<10} | {obra_social}\n" 
            reporte_texto += linea

        self.mostrar_reporte_en_ventana(f"Reporte de Pacientes ({len(pacientes)} en Total)", reporte_texto)
        
    # =======================================================
    # 6. GESTIÓN DE TURNOS (Submenú)
    # =======================================================

    def mostrar_reporte_en_ventana(self, titulo, contenido):
        """Abre una ventana Toplevel para mostrar un contenido largo (listado de pacientes/turnos)."""
        ventana_reporte = tk.Toplevel(self.master, bg=COLOR_FONDO)
        ventana_reporte.title(titulo)
        ventana_reporte.geometry("600x400") 

        # Frame para el contenido desplazable
        frame_contenido = tk.Frame(ventana_reporte, bg='white')
        frame_contenido.pack(expand=True, fill='both')

        # Scrollbar vertical
        scrollbar = tk.Scrollbar(frame_contenido, orient="vertical")
        
        # Widget Text para mostrar el listado
        listado_text = tk.Text(frame_contenido, wrap="none", yscrollcommand=scrollbar.set, font=('Courier New', 10), bg='white', fg='black')
        
        scrollbar.config(command=listado_text.yview)
        scrollbar.pack(side="right", fill="y")
        listado_text.pack(expand=True, fill='both', padx=10, pady=10)
        
        listado_text.insert("1.0", contenido)
        listado_text.config(state="disabled") # Hacer el texto de solo lectura


    def abrir_gestion_turnos(self):
        self.ventana_turnos = tk.Toplevel(self.master, bg=COLOR_FONDO)
        self.ventana_turnos.title("Gestión de Turnos")
        self.ventana_turnos.geometry("380x250") 
        
        tk.Label(self.ventana_turnos, text="Opciones de Turnos", font=('Segoe UI', 14, 'bold'), 
                 bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=10)
                         
        
        frame_botones_grid = tk.Frame(self.ventana_turnos, bg=COLOR_FONDO)
        frame_botones_grid.pack(pady=5, padx=20) 
        # ----------------------------------------------------

        
        self._crear_boton(frame_botones_grid, "1. Registrar Nuevo Turno", 
                              self.abrir_registro_turno, row=1, column=0, columnspan=2, color=COLOR_PRINCIPAL)
        
        self._crear_boton(frame_botones_grid, "2. Buscar y Gestionar Turnos (DNI/Fecha)", 
                              self.abrir_gestion_busqueda_turnos, row=2, column=0, columnspan=2, color=COLOR_SECUNDARIO)

        self._crear_boton(frame_botones_grid, "3. Listar Todos los Turnos",
                              self.ejecutar_listado_turnos, row=3, column=0, columnspan=2, color=COLOR_SECUNDARIO)
        
        tk.Button(self.ventana_turnos, text="Cerrar Menú", font=FUENTE_PRINCIPAL,
                  command=self.ventana_turnos.destroy, bg='#DC143C', fg='white', relief=tk.FLAT).pack(pady=10)

    def abrir_registro_turno(self):
        ventana = tk.Toplevel(self.master, bg=COLOR_FONDO)
        ventana.title("Registrar Nuevo Turno")
        ventana.geometry("400x350")
        
        self.dni_var = tk.StringVar()
        self.fecha_var = tk.StringVar()
        self.hora_var = tk.StringVar()
        self.tratamiento_var = tk.StringVar()
        
        campos = [
            ("DNI Paciente (Obligatorio):", self.dni_var),
            ("Fecha (AAAA-MM-DD):", self.fecha_var),
            ("Hora (HH:MM):", self.hora_var),
            ("Tratamiento:", self.tratamiento_var),
        ]

        frame_campos = tk.Frame(ventana, bg=COLOR_FONDO)
        frame_campos.pack(padx=20, pady=10, fill='x')

        for texto, var in campos:
            frame = tk.Frame(frame_campos, bg=COLOR_FONDO)
            tk.Label(frame, text=texto, width=20, anchor='w', bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_PRINCIPAL).pack(side='left', padx=5, pady=5)
            tk.Entry(frame, textvariable=var, width=30, font=FUENTE_PRINCIPAL).pack(side='right', padx=5, pady=5, fill='x', expand=True)
            frame.pack(fill='x')
        
        tk.Button(ventana, text="Confirmar Turno", font=FUENTE_PRINCIPAL,
                  bg=COLOR_PRINCIPAL, fg=COLOR_TEXTO, relief=tk.FLAT,
                  command=lambda: self.guardar_nuevo_turno(ventana)).pack(pady=20)

    def guardar_nuevo_turno(self, ventana):
        """Lógica para guardar el turno desde el formulario."""
        paciente_dni = self.dni_var.get()
        fecha = self.fecha_var.get()
        hora = self.hora_var.get()
        tratamiento = self.tratamiento_var.get()
        
        if not paciente_dni or not fecha or not hora:
            messagebox.showerror("Error", "Los campos DNI, Fecha y Hora son obligatorios.")
            return

        # 1. Verificar si el paciente existe
        if not self.manager.buscar_paciente_por_dni(paciente_dni):
            return messagebox.showwarning("Error", "❌ El DNI del paciente no está registrado.")

        # 2. Creamos el objeto Turno (DNI del paciente se usa para buscar el ID en el Service)
        nuevo_turno = Turno(None, paciente_dni, fecha, hora, tratamiento) 
        
        # 3. Llamar al Service para guardar
        if self.manager.registrar_turno(nuevo_turno):
            messagebox.showinfo("Éxito", "✅ Turno registrado exitosamente.")
            ventana.destroy() 
        else:
            messagebox.showerror("Error", "❌ Error al registrar el turno en la BD.")

    def ejecutar_listado_turnos(self):
        """Muestra una ventana con el listado completo de turnos (incluye tratamiento)."""
        turnos = self.manager.listar_todos_turnos()
        
        if not turnos:
            return messagebox.showinfo("Listado de Turnos", "No hay turnos registrados en la base de datos.")

        listado_texto = "--- LISTADO DE TURNOS ---\n"
        # ✅ CAMBIO: Añadir Motivo/Tratamiento al encabezado
        listado_texto += (f"{'Apellido':<15} | {'DNI Paciente':<12} | {'Fecha':<10} | {'Hora':<5} | {'Estado':<10} | {'Motivo/Tratamiento'}\n")
        listado_texto += "-" * 75 + "\n" # Longitud ajustada para el nuevo campo

        hoy = date.today()
        for t in turnos:
            fecha_turno = t['fecha'] 
            estado = "EXPIRADO" if fecha_turno < hoy else "VIGENTE"
            
            # ✅ CAMBIO: Añadir el motivo/tratamiento al final
            listado_texto += (f"{t['apellido']:<15} | {t['dni']:<12} | "
                               f"{str(fecha_turno):<10} | {str(t['hora']):<5} | {estado:<10} | {t['tratamiento']}\n")

        self.mostrar_reporte_en_ventana("Listado de Turnos", listado_texto)


    def abrir_gestion_busqueda_turnos(self):
        """Abre el formulario para buscar turnos por DNI o Fecha."""
        self.ventana_gestion_busqueda_turnos = tk.Toplevel(self.master, bg=COLOR_FONDO)
        self.ventana_gestion_busqueda_turnos.title("Buscar y Gestionar Turnos")
        self.ventana_gestion_busqueda_turnos.geometry("450x200")

        tk.Label(self.ventana_gestion_busqueda_turnos, text="Buscar Turno", font=('Segoe UI', 14, 'bold'),
                 bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=10)

        tk.Label(self.ventana_gestion_busqueda_turnos, text="Buscar por:", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_PRINCIPAL).pack()

        # Usamos una lista de criterio para la búsqueda (DNI o Fecha)
        criterios = ['DNI Paciente', 'Fecha (AAAA-MM-DD)']
        self.criterio_busqueda_turnos = tk.StringVar(self.ventana_gestion_busqueda_turnos)
        self.criterio_busqueda_turnos.set(criterios[0]) # Valor inicial

        tk.OptionMenu(self.ventana_gestion_busqueda_turnos, self.criterio_busqueda_turnos, *criterios).pack(pady=5)

        tk.Label(self.ventana_gestion_busqueda_turnos, text="Valor a buscar:", bg=COLOR_FONDO, fg=COLOR_TEXTO, font=FUENTE_PRINCIPAL).pack()
        self.entrada_busqueda_turnos = tk.Entry(self.ventana_gestion_busqueda_turnos, font=FUENTE_PRINCIPAL)
        self.entrada_busqueda_turnos.pack(pady=5)
        
        tk.Button(self.ventana_gestion_busqueda_turnos, text="Buscar", font=FUENTE_PRINCIPAL,
                  bg=COLOR_PRINCIPAL, fg=COLOR_TEXTO, relief=tk.FLAT,
                  command=self.ejecutar_busqueda_flexible).pack(pady=10)
        
    def ejecutar_busqueda_flexible(self):
        """Ejecuta la búsqueda de turnos según el criterio seleccionado y MUESTRA EL LISTADO (incluye tratamiento)."""
        
        criterio_display = self.criterio_busqueda_turnos.get()
        valor = self.entrada_busqueda_turnos.get().strip()

        if not valor:
            messagebox.showwarning("Advertencia", "Debe ingresar un valor de búsqueda.")
            return

        # Mapeo del criterio de display al nombre de columna real en la BD
        if criterio_display == 'DNI Paciente':
            criterio_db = 'dni' 
        else: # 'Fecha (AAAA-MM-DD)'
            criterio_db = 'fecha'

        # Llama al manager para obtener la lista de turnos
        turnos = self.manager.buscar_turnos_por_criterio(criterio_db, valor)
        
        # --- Generar el texto completo del listado ---
        listado_texto = f"--- RESULTADOS DE BÚSQUEDA por {criterio_display}: {valor} ---\n"
        # ✅ CAMBIO: Añadir Motivo/Tratamiento al encabezado
        listado_texto += (f"{'Apellido':<15} | {'DNI Paciente':<12} | {'Fecha':<10} | {'Hora':<5} | {'Estado':<10} | {'Motivo/Tratamiento'}\n")
        listado_texto += "-" * 75 + "\n"
        
        if turnos:
            hoy = date.today()
            for t in turnos:
                fecha_turno = t['fecha']
                estado = "EXPIRADO" if fecha_turno < hoy else "VIGENTE"
                
                # ✅ CAMBIO: Añadir el motivo/tratamiento al final
                listado_texto += (f"{t['apellido']:<15} | {t['dni']:<12} | "
                                  f"{str(fecha_turno):<10} | {str(t['hora']):<5} | {estado:<10} | {t['tratamiento']}\n")
            
            self.mostrar_reporte_en_ventana("Resultados de Búsqueda", listado_texto)
            self.ventana_gestion_busqueda_turnos.destroy() 
            
        else:
            listado_texto += f"No se encontró ningún turno para el {criterio_display}: {valor}\n"
            messagebox.showinfo("Búsqueda", listado_texto)

    def ejecutar_cancelacion_desde_busqueda(self, turno_id, ventana_busqueda):
        """Cancela un turno después de haber sido listado en la búsqueda flexible."""
        try:
            id_a_cancelar = int(turno_id)
        except ValueError:
            return messagebox.showerror("Error", "El ID debe ser un número entero.")

        if messagebox.askyesno("Confirmar Cancelación", f"¿Está seguro de cancelar el turno con ID: {id_a_cancelar}?"):
            if self.manager.eliminar_turno(id_a_cancelar):
                messagebox.showinfo("Éxito", f"✅ Turno con ID {id_a_cancelar} cancelado exitosamente.")
                ventana_busqueda.destroy() 
                self.abrir_gestion_turnos() 
            else:
                messagebox.showerror("Error", "❌ No se pudo cancelar el turno. Verifique el ID.")