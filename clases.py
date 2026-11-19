import random
from datetime import datetime

class Paciente:
    def __init__(self, cedula, nombre_completo, correo, telefono, tipo_paciente):
        self.cedula = cedula
        self.nombre_completo = nombre_completo
        self.correo = correo
        self.telefono = telefono
        self.tipo_paciente = tipo_paciente

class CitaMedica:
    def __init__(self, paciente, especialidad, medico, fecha_hora, nivel_urgencia):
        self.id_cita = random.randint(1000, 9999)
        self.folio_codigo = f"UAM-{datetime.now().strftime('%Y%m%d')}-{random.randint(100, 999)}"
        self.paciente = paciente
        self.especialidad = especialidad
        self.medico = medico
        self.fecha_hora = fecha_hora
        self.nivel_urgencia = nivel_urgencia
        self.estado = "Confirmada"
        self.codigo_qr = f"QR-{self.folio_codigo}"