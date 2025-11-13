# gui/menu.py
from services.gestion_kinesiologia import GestionKinesiologia
from models.paciente import Paciente
from utils.validador import Validador

def mostrar_menu():
    print("\n--- Sistema de Gestión Kinésica ---")
    print("1. 📝 Registrar nuevo paciente")
    print("2. 🔎 Buscar paciente (DNI)")
    print("3. ✍️ Actualizar paciente (DNI)")
    print("4. 🗑️ Eliminar paciente (DNI)")
    print("5. 📊 Generar Reporte de Pacientes")
    print("6. 🚪 Salir")
    return input("Seleccione una opción: ")

def registrar_paciente_view(manager):
    print("\n--- Registro de Nuevo Paciente ---")
    dni = input("DNI: ")
    if not Validador.validar_dni(dni):
        print("❌ Error: DNI inválido. Debe contener 7 u 8 dígitos.")
        return
        
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    fecha_nacimiento = input("Fecha Nacimiento (AAAA-MM-DD): ")
    if not Validador.validar_fecha(fecha_nacimiento):
        print("❌ Error: Formato de fecha incorrecto (debe ser AAAA-MM-DD).")
        return
        
    historia_clinica = input("Historia Clínica Nro: ")
    obra_social = input("Obra Social: ")
    
    nuevo_paciente = Paciente(dni, nombre, apellido, fecha_nacimiento, historia_clinica, obra_social)
    
    if manager.registrar_paciente(nuevo_paciente):
        print("✅ Paciente registrado exitosamente.")
    else:
        print("❌ Error al registrar paciente. El DNI o HC podría estar duplicado.")

# Funciones de buscar, actualizar, eliminar, y reporte (ver código completo en la sección anterior para actualizar el objeto Paciente)
# ...

def iniciar_aplicacion():
    manager = GestionKinesiologia()
    while True:
        opcion = mostrar_menu()
        if opcion == '1':
            registrar_paciente_view(manager)
        # elif opciones 2, 3, 4, 5...
        # ... (debes completar la implementación de las otras vistas aquí)
        elif opcion == '6':
            manager.db.cerrar()
            print("Cerrando el sistema.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")