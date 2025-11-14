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

    def obtener_datos(self, query, params=None):
        if self.ejecutar_consulta(query, params):
            return self.cursor.fetchall()
        return []

    def confirmar(self):
        if self.conn:
            self.conn.commit()

    def cerrar(self):
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()