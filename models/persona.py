# models/persona.py

class Persona:
    def __init__(self, dni, nombre, apellido, fecha_nacimiento):
        # Atributos protegidos (convención de Python con guion bajo)
        self._dni = dni
        self._nombre = nombre
        self._apellido = apellido
        self._fecha_nacimiento = fecha_nacimiento

    # Métodos Get (accesores)
    def get_dni(self):
        return self._dni

    def get_nombre(self):
        return self._nombre

    def get_apellido(self):
        return self._apellido
    
    def get_fecha_nacimiento(self):
        return self._fecha_nacimiento

    # Métodos Set (modificadores)
    def set_nombre(self, nuevo_nombre):
        self._nombre = nuevo_nombre

    def set_apellido(self, nuevo_apellido):
        self._apellido = nuevo_apellido
        
    # El DNI NO debe tener un setter ya que es la clave primaria.
    
    def __str__(self):
        return f"Persona: {self._nombre} {self._apellido} (DNI: {self._dni})"