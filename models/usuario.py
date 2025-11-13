# models/usuario.py

from .persona import Persona

class Usuario(Persona):
    def __init__(self, dni, nombre, apellido, fecha_nacimiento, matricula, rol):
        super().__init__(dni, nombre, apellido, fecha_nacimiento)
        self._matricula = matricula
        self._rol = rol

    def get_matricula(self):
        return self._matricula

    def get_rol(self):
        return self._rol

    def set_rol(self, nuevo_rol):
        self._rol = nuevo_rol
        
    def __str__(self):
        return (f"Usuario: {self.get_nombre()} {self._apellido} | DNI: {self.get_dni()} | "
                f"Matrícula: {self._matricula} | Rol: {self._rol}")