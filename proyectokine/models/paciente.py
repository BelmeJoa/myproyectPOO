# models/paciente.py
from models.persona import Persona

class Paciente(Persona):
    def __init__(self, dni, nombre, apellido, fecha_nacimiento, historia_clinica, obra_social):
        # Llama al constructor de la clase padre (Herencia) 
        super().__init__(dni, nombre, apellido, fecha_nacimiento)
        self._historia_clinica = historia_clinica
        self._obra_social = obra_social

    def get_historia_clinica(self):
        return self._historia_clinica
    
    def __str__(self):
        return f"Paciente: {self._nombre} {self._apellido} (DNI: {self._dni}, HC: {self._historia_clinica})"