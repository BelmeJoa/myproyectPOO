# services/gestion_kinesiologia.py
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
        resultado = self.db.obtener_datos(query, (dni,)) 
        
        if resultado:
            datos = resultado[0]
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
        return self.db.obtener_datos(query)
    # =======================================================
    # CRUD para Turnos
    # =======================================================

    def registrar_turno(self, turno):
        """Registra un nuevo turno en la base de datos."""
        query = "INSERT INTO turno (paciente_dni, fecha, hora, tratamiento) VALUES (%s, %s, %s, %s)"
        params = (turno.get_paciente_dni(), turno.get_fecha(), turno.get_hora(), turno._tratamiento)
        
        db = Database()
        resultado = db.ejecutar_consulta(query, params=params, commit=True)
        db.close()
        return resultado

    def buscar_turno_por_id(self, id_turno):
        """Busca un turno por su ID y devuelve un objeto Turno."""
        query = "SELECT id, paciente_dni, fecha, hora, tratamiento FROM turno WHERE id = %s"
        params = (id_turno,)
        
        db = Database()
        datos_turno = db.ejecutar_consulta(query, params=params, fetch_one=True)
        db.close()
        
        if datos_turno:
            # Creamos un objeto Turno (Recuerda que los datos[0] es el id)
            return Turno(datos_turno[0], datos_turno[1], datos_turno[2], datos_turno[3], datos_turno[4])
        return None

    def actualizar_turno(self, turno):
        """Actualiza la fecha, hora y tratamiento de un turno existente."""
        query = "UPDATE turno SET fecha = %s, hora = %s, tratamiento = %s WHERE id = %s"
        params = (turno.get_fecha(), turno.get_hora(), turno._tratamiento, turno.get_id())
        
        db = Database()
        resultado = db.ejecutar_consulta(query, params=params, commit=True)
        db.close()
        return resultado

    def eliminar_turno(self, id_turno):
        """Elimina un turno por su ID."""
        query = "DELETE FROM turno WHERE id = %s"
        params = (id_turno,)
        
        db = Database()
        resultado = db.ejecutar_consulta(query, params=params, commit=True)
        db.close()
        return resultado

    def buscar_turnos_por_criterio(self, criterio, valor):
        # ... código para armar la query ...
        
        db = Database()
        # 1. OBTIENE LOS DATOS (SELECT)
        datos_turnos = db.obtener_datos(query, params=(valor,))
        db.cerrar()
        
        # ... Aquí el código procesa lista_turnos ...
        # ...
        return datos_turnos
