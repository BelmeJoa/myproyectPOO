# utils/validador.py
import re
from datetime import datetime

class Validador:
    @staticmethod
    def validar_dni(dni):
        # Valida 7 u 8 dígitos
        if re.match(r'^\d{7,8}$', dni):
            return True
        return False

    @staticmethod
    def validar_fecha(fecha_str, formato='%Y-%m-%d'):
        # Valida formato AAAA-MM-DD
        try:
            datetime.strptime(fecha_str, formato)
            return True
        except ValueError:
            return False