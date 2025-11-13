# models/paciente.py

from .persona import Persona

class Paciente(Persona):
    def __init__(self, dni, nombre, apellido, fecha_nacimiento, historia_clinica, obra_social):
        super().__init__(dni, nombre, apellido, fecha_nacimiento)
        self._historia_clinica = historia_clinica
        self._obra_social = obra_social

    def get_historia_clinica(self):
        return self._historia_clinica

    def get_obra_social(self):
        return self._obra_social

    def set_historia_clinica(self, nueva_hc):
        self._historia_clinica = nueva_hc
        
    def set_obra_social(self, nueva_os):
        self._obra_social = nueva_os

    def __str__(self):
        # Acceso recomendado a través de getters para atributos de Persona
        return (f"Paciente: {self.get_nombre()} {self.get_apellido()} | DNI: {self.get_dni()} | "
                f"HC: {self._historia_clinica} | OS: {self._obra_social}")