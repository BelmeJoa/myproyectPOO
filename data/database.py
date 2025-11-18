# data/database.py
import mysql.connector
from mysql.connector import Error

# NOTA CRÍTICA: Debes cambiar 'TU_USUARIO_MYSQL' y 'TU_PASSWORD_MYSQL'
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root', 
    'password': 'BelmeMySql2003', 
    'database': 'db_kinesiologia'
}

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        try:
            # Conexión parametrizada [cite: 27]
            self.conn = mysql.connector.connect(**DB_CONFIG)
            if self.conn.is_connected():
                # cursor(prepared=True) garantiza Consultas Preparadas 
                self.cursor = self.conn.cursor(prepared=True)
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            self.conn = None

    def ejecutar_consulta(self, query, params=None):
        if not self.conn:
            return None
        try:
            self.cursor.execute(query, params or ())
            return True
        except Error as e:
            print(f"Error en la consulta: {e}")
            return False

    # db/database.py (Fragmento de la clase Database)

class Database:
    def obtener_datos(self, query, params=None, fetch_all=False):
        conexion = None
        cursor = None
        try:
            # 1. Conectar y obtener el cursor
            conexion = self.conectar() 
            cursor = conexion.cursor() 
            
            # 2. Ejecutar la consulta
            cursor.execute(query, params or ())
            
            # 3. Obtener resultado
            if fetch_all:
                resultado = cursor.fetchall()
            else:
                resultado = cursor.fetchone()
            
            # 4. Retornar resultado
            return resultado

        except mysql.connector.Error as err:
            print(f"Error en la consulta: {err.errno} ({err.sqlstate}): {err.msg}")
            return None
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            return None
        finally:
            # 5. Cerrar el cursor y la conexión
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()

    def confirmar(self):
        if self.conn:
            self.conn.commit()

    def close(self):
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()