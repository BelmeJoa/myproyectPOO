# data/database.py
import mysql.connector
from mysql.connector import Error

# NOTA CRÍTICA: Debes confirmar que estos datos sean correctos para tu instalación.
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'BelmeMySql2003', # Confirma este password
    'database': 'db_kinesiologia' # Confirma que la BD se llama así
}

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                # print("Conexión inicial exitosa.")
            else:
                print("Conexión inicial fallida.")
        except Error as e:
            print(f"Error al conectar a MySQL: {e}")
            self.conn = None

    def ejecutar_consulta(self, query, params=None):
        if not self.conn or not self.cursor:
            # print("Error: Conexión o cursor no disponible.")
            return False
        try:
            self.cursor.execute(query, params or ())
            # NOTA: No hacemos commit aquí. Lo hace la función 'confirmar'.
            return True
        except Error as e:
            print(f"Error en la consulta: {e}")
            return False

    def obtener_datos(self, query, params=None, fetch_all=True):
        """
        Ejecuta SELECT y obtiene los datos.
        fetch_all=True (por defecto): devuelve todas las filas.
        fetch_all=False: devuelve una sola fila.
        """
        if self.ejecutar_consulta(query, params):
            if fetch_all:
                return self.cursor.fetchall()
            else:
                return self.cursor.fetchone()
        return [] if fetch_all else None

    def confirmar(self):
        """Aplica los cambios pendientes (INSERT, UPDATE, DELETE)."""
        if self.conn:
            self.conn.commit()

    def close(self):
        """Cierra el cursor y la conexión."""
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()