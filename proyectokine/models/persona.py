# models/persona.py
class Persona:
    def __init__(self, dni, nombre, apellido, fecha_nacimiento):
        # Encapsulamiento con atributos protegidos (_): [cite: 26]
        self._dni = dni
        self._nombre = nombre
        self._apellido = apellido
        self._fecha_nacimiento = fecha_nacimiento
        self._id = None 

    # Métodos GET (Encapsulamiento)
    def get_dni(self):
        return self._dni
    def get_nombre(self):
        return self._nombre
    
    # Método SET (Ejemplo)
    def set_nombre(self, nuevo_nombre):
        self._nombre = nuevo_nombre