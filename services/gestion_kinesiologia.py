from data.database import Database
from models.paciente import Paciente
from models.turno import Turno

class GestionKinesiologia:
    def __init__(self):
        self.db = Database()

    # --- CRUD: Crear ---
    def registrar_paciente(self, paciente: Paciente):
        query_persona = "INSERT INTO persona (dni, nombre, apellido, fecha_nacimiento) VALUES (%s, %s, %s, %s)"
        params_persona = (paciente.get_dni(), paciente.get_nombre(), 
                          paciente._apellido, paciente._fecha_nacimiento)
        
        if self.db.ejecutar_consulta(query_persona, params_persona):
            paciente_id = self.db.cursor.lastrowid 
            query_paciente = "INSERT INTO paciente (id_paciente, historia_clinica, obra_social) VALUES (%s, %s, %s)"
            params_paciente = (paciente_id, paciente.get_historia_clinica(), paciente._obra_social)
            
            if self.db.ejecutar_consulta(query_paciente, params_paciente):
                self.db.confirmar()
                return True
        return False

    # --- CRUD: Leer / Buscar ---
    def buscar_paciente_por_dni(self, dni):
        query = """
        SELECT p.dni, p.nombre, p.apellido, p.fecha_nacimiento, pa.historia_clinica, pa.obra_social, p.id_persona
        FROM persona p JOIN paciente pa ON p.id_persona = pa.id_paciente
        WHERE p.dni = %s
        """
        # Cambiamos fetch_all=True (por defecto) a False para obtener una sola fila
        resultado = self.db.obtener_datos(query, (dni,), fetch_all=False) 
        
        if resultado:
            datos = resultado
            paciente = Paciente(datos[0], datos[1], datos[2], datos[3], datos[4], datos[5])
            paciente._id = datos[6]
            return paciente
        return None
    
    # --- CRUD: Actualizar ---
    def actualizar_paciente(self, paciente: Paciente):
        # Actualizar tabla Paciente
        query_pac = "UPDATE paciente SET historia_clinica = %s, obra_social = %s WHERE id_paciente = %s"
        params_pac = (paciente.get_historia_clinica(), paciente._obra_social, paciente._id)
        
        # Actualizar tabla Persona
        query_per = "UPDATE persona SET nombre = %s, apellido = %s, fecha_nacimiento = %s WHERE id_persona = %s"
        params_per = (paciente.get_nombre(), paciente._apellido, paciente._fecha_nacimiento, paciente._id)
        
        if self.db.ejecutar_consulta(query_pac, params_pac) and self.db.ejecutar_consulta(query_per, params_per):
            self.db.confirmar()
            return True
        return False
        
    # --- CRUD: Eliminar ---
    def eliminar_paciente(self, dni):
        paciente = self.buscar_paciente_por_dni(dni)
        if not paciente:
            return False

        paciente_id = paciente._id
        
        # Se debe eliminar de la tabla hija (paciente) y luego de la padre (persona)
        query_pac = "DELETE FROM paciente WHERE id_paciente = %s"
        query_per = "DELETE FROM persona WHERE id_persona = %s"
        
        # Es CRÍTICO que la eliminación sea en este orden y se confirme.
        if self.db.ejecutar_consulta(query_pac, (paciente_id,)):
            if self.db.ejecutar_consulta(query_per, (paciente_id,)):
                self.db.confirmar()
                return True
        return False
            
    # --- Reportes ---
    def obtener_todos_pacientes(self):
        query = """
        SELECT p.dni, p.nombre, p.apellido, pa.historia_clinica, pa.obra_social
        FROM persona p JOIN paciente pa ON p.id_persona = pa.id_paciente
        ORDER BY p.apellido
        """
        # Aquí sí usamos fetch_all=True
        return self.db.obtener_datos(query)
        
    # =======================================================
    # CRUD para Turnos (CORREGIDO)
    # =======================================================

    def registrar_turno(self, turno):
        "Registra un nuevo turno en la base de datos."
        paciente = self.buscar_paciente_por_dni(turno.get_paciente_dni())
        if not paciente:
            return False 
            
        id_paciente = paciente._id # El ID que la BD espera
        
        # 2. Ejecutar la consulta con el ID numérico
        query = "INSERT INTO turno (id_paciente, fecha, hora, tratamiento) VALUES (%s, %s, %s, %s)"
        params = (id_paciente, turno.get_fecha(), turno.get_hora(), turno._tratamiento)
        
        resultado = self.db.ejecutar_consulta(query, params=params)
        
        if resultado:
            self.db.confirmar() 
            return True
        return False

    def buscar_turno_por_id(self, id_turno):
        """Busca un turno por su ID y devuelve un objeto Turno."""
        # CORREGIDO: Usamos id_turno como PK y obtenemos el DNI del paciente.
        query = """
        SELECT 
            t.id_turno, p.dni, t.fecha, t.hora, t.tratamiento 
        FROM turno t
        JOIN paciente pa ON t.id_paciente = pa.id_paciente
        JOIN persona p ON pa.id_paciente = p.id_persona   
        WHERE t.id_turno = %s 
        """ 
        params = (id_turno,)
        
        datos_turno = self.db.obtener_datos(query, params=params, fetch_all=False)
        
        if datos_turno:
            # Creamos un objeto Turno: Turno(id_turno, dni, fecha, hora, tratamiento)
            return Turno(datos_turno[0], datos_turno[1], datos_turno[2], datos_turno[3], datos_turno[4], datos_turno[5])
        return None

    def actualizar_turno(self, turno):
        """Actualiza la fecha, hora y tratamiento de un turno existente."""
        # CORREGIDO: Usamos id_turno
        query = "UPDATE turno SET fecha = %s, hora = %s, tratamiento = %s WHERE id_turno = %s"
        params = (turno.get_fecha(), turno.get_hora(), turno._tratamiento, turno.get_id())
        
        resultado = self.db.ejecutar_consulta(query, params=params)
        
        if resultado:
            self.db.confirmar() 
            return True
        return False

    def eliminar_turno(self, id_turno):
        """Elimina un turno por su ID."""
        # CORREGIDO: Usamos id_turno
        query = "DELETE FROM turno WHERE id_turno = %s"
        params = (id_turno,)
        
        resultado = self.db.ejecutar_consulta(query, params=params)
        
        if resultado:
            self.db.confirmar()  
            return True
        return False

    def listar_todos_turnos(self):
        """
        Lista todos los turnos, trayendo DNI, Apellido y Tratamiento del paciente.
        """
        query = """
        SELECT 
            t.id_turno, p.dni, p.apellido, t.fecha, t.hora, t.tratamiento 
        FROM turno t
        JOIN paciente pa ON t.id_paciente = pa.id_paciente
        JOIN persona p ON pa.id_paciente = p.id_persona  
        ORDER BY t.fecha DESC
        """
        datos_turnos = self.db.obtener_datos(query, fetch_all=True)

        if datos_turnos:
            turnos = []
            for datos in datos_turnos:
                turnos.append({
                    'id': datos[0], 'dni': datos[1], 'apellido': datos[2], 
                    'fecha': datos[3], 'hora': datos[4], 'tratamiento': datos[5] # <-- Asegurado
                })
            return turnos
        return []

    def buscar_turnos_por_criterio(self, criterio, valor):
        """
        Busca turnos por DNI (criterio='dni') o por Fecha (criterio='fecha'), incluyendo tratamiento.
        """
        
        if criterio == 'dni':
            criterio_busqueda = "p.dni"
            valor_busqueda = valor 
        elif criterio == 'fecha': 
            criterio_busqueda = "t.fecha"
            valor_busqueda = valor
        else:
            return []

        query = f"""
        SELECT 
            t.id_turno, p.dni, p.apellido, t.fecha, t.hora, t.tratamiento 
        FROM turno t
        JOIN paciente pa ON t.id_paciente = pa.id_paciente
        JOIN persona p ON pa.id_paciente = p.id_persona  
        WHERE {criterio_busqueda} = %s
        ORDER BY t.fecha DESC
        """
        
        datos_turnos = self.db.obtener_datos(query, (valor_busqueda,), fetch_all=True)

        if datos_turnos:
            # tratamiento/motivo es el índice 5
            return [{'id': d[0], 'dni': d[1], 'apellido': d[2], 'fecha': d[3], 'hora': d[4], 'tratamiento': d[5]} for d in datos_turnos] # <-- Asegurado
        return []