# models/turno.py

class Turno:
    def __init__(self, id_turno, paciente_dni, fecha, hora, tratamiento):
        self._id_turno = id_turno
        self._paciente_dni = paciente_dni # Clave foránea al Paciente
        self._fecha = fecha
        self._hora = hora
        self._tratamiento = tratamiento

    def get_id(self):
        return self._id_turno
        
    def get_paciente_dni(self):
        return self._paciente_dni

    def get_fecha(self):
        return self._fecha
        
    def get_hora(self):
        return self._hora
    
    def set_fecha(self, nueva_fecha):
        self._fecha = nueva_fecha
        
    def set_hora(self, nueva_hora):
        self._hora = nueva_hora

    def __str__(self):
        return (f"Turno Nro: {self._id_turno} | DNI Paciente: {self._paciente_dni} | "
                f"Fecha y Hora: {self._fecha} {self._hora} | Tratamiento: {self._tratamiento}")