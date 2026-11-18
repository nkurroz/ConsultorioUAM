# Árbol Binario de Decisión
class NodoTriaje:
    def __init__(self, pregunta=None, nivel_urgencia=None, descripcion_riesgo=None):
        self.pregunta = pregunta
        self.nivel_urgencia = nivel_urgencia
        self.descripcion_riesgo = descripcion_riesgo
        self.si = None
        self.no = None

class ArbolTriajeBinario:
    def __init__(self):
        self.raiz = self._construir_arbol()

    def _construir_arbol(self):
        raiz = NodoTriaje("¿Presenta dolor opresivo en el pecho, pérdida de conocimiento o dificultad severa para respirar?")
        raiz.si = NodoTriaje(nivel_urgencia=1, descripcion_riesgo="ALTA URGENCIA / EMERGENCIA - Atención Inmediata")
        q2 = NodoTriaje("¿Tiene fiebre mayor a 38.5°C, sangrado activo o dolor agudo e intenso?")
        raiz.no = q2
        q2.si = NodoTriaje(nivel_urgencia=2, descripcion_riesgo="URGENCIA MEDIA - Prioridad Preferente")
        q3 = NodoTriaje("¿Sus síntomas son malestares leves (tos ligera, congestión, chequeo de rutina)?")
        q2.no = q3
        q3.si = NodoTriaje(nivel_urgencia=3, descripcion_riesgo="BAJA URGENCIA - Consulta General / Rutinaria")
        q3.no = NodoTriaje(nivel_urgencia=3, descripcion_riesgo="BAJA URGENCIA - Consulta General / Rutinaria")
        return raiz

    def ejecutar_evaluacion(self):
        nodo_actual = self.raiz
        print("\n=== EVALUACIÓN CLÍNICA DE TRIAJE ===")
        print("Responda las preguntas para evaluar la severidad de su estado médico:\n")

        while nodo_actual.nivel_urgencia is None:
            # BLOQUE DE VALIDACIÓN: Respuesta Binaria (Sí/No)
            while True:
                respuesta = input(f"{nodo_actual.pregunta} (s/n): ").strip().lower()
                if respuesta in ['s', 'sí', 'si', 'n', 'no']:
                    break
                print("Entrada no válida. Por favor responda solo con 's' (Sí) o 'n' (No).\n")

            if respuesta in ['s', 'sí', 'si']:
                nodo_actual = nodo_actual.si
            else:
                nodo_actual = nodo_actual.no

        print(f"\nResultados: {nodo_actual.descripcion_riesgo}")
        return nodo_actual.nivel_urgencia


# Grafo Dirigido Ponderado
class GrafoAgendaPonderado:
    def __init__(self):
        self.red_medica = {
            "Medicina General": {
                "Dra. Mariela Hurtado": [{"horario": "Hoy 11:00 AM", "espera_horas": 0.5}, {"horario": "Hoy 03:00 PM", "espera_horas": 4.5}],
                "Dr. Fernando Duarte": [{"horario": "Hoy 01:30 PM", "espera_horas": 3.0}]
            },
            "Cardiología": {
                "Dr. Ivanna Icasa": [{"horario": "Hoy 11:30 AM", "espera_horas": 1.0}]
            },
            "Pediatría": {
                "Dra. Lucía Martínez": [{"horario": "Hoy 02:00 PM", "espera_horas": 3.5}]
            }
        }

    def listar_especialidades(self):
        return list(self.red_medica.keys())

    def buscar_cupo_optimo(self, especialidad_solicitada, nivel_urgencia):
        mejor_opcion = None
        menor_tiempo = float('inf')
        especialidades_a_evaluar = self.listar_especialidades() if nivel_urgencia == 1 else [especialidad_solicitada]

        for esp in especialidades_a_evaluar:
            for nombre_medico, bloques in self.red_medica.get(esp, {}).items():
                for bloque in bloques:
                    if bloque["espera_horas"] < menor_tiempo:
                        menor_tiempo = bloque["espera_horas"]
                        mejor_opcion = {
                            "especialidad": esp, "medico": nombre_medico,
                            "horario": bloque["horario"], "espera_horas": menor_tiempo
                        }
        return mejor_opcion