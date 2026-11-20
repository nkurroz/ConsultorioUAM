import random, re
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

# Árbol Binario de Decisión
class NodoTriaje:
    def __init__(self, pregunta=None, nivel_urgencia=None, descripcion_riesgo=None):
        self.pregunta = pregunta
        self.nivel_urgencia = nivel_urgencia
        self.descripcion_riesgo = descripcion_riesgo
        self.si = None
        self.no = None

class ArbolBinario:
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
                "Dr. Fernando Duarte": [{"horario": "Hoy 01:30 PM", "espera_horas": 3.0}]
            },
            "Cardiología": {
                "Dra. Ivanna Icasa": [{"horario": "Hoy 11:30 AM", "espera_horas": 1.0}]
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

class SistemaClinicaUAM:
    def _init_(self):
        self.base_pacientes = {}
        self.lista_citas = []
        self.arbol_triaje = ArbolBinario()
        self.grafo_agenda = GrafoAgendaPonderado()

    def registrar_o_buscar_paciente(self):
        print("\n--- IDENTIFICACIÓN DEL PACIENTE ---")
        
        # BLOQUE DE VALIDACIÓN: Cédula
        while True:
            cedula = input("Ingrese la cédula del paciente: ").strip().upper()
            if re.match(r'^[0-9]{3}-?[0-9]{6}-?[0-9]{4}[A-Z]$', cedula) or (len(cedula) >= 8 and cedula.isalnum()):
                break
            print(" Error: Formato de cédula inválido. (Ej. 001-281098-0005Y o 0012810980005Y)\n")

        if cedula in self.base_pacientes:
            paciente = self.base_pacientes[cedula]
            print(f" Paciente existente encontrado: {paciente.nombre_completo} ({paciente.tipo_paciente})\n")
            return paciente

        print("Paciente no registrado. Complete los datos requeridos:")
        
        # BLOQUE DE VALIDACIÓN: Campos de texto no vacíos
        while True:
            nombre = input("Nombre completo: ").strip()
            if nombre: break
            print(" El nombre no puede estar vacío.")
            
        while True:
            correo = input("Correo electrónico: ").strip()
            if correo: break
            print(" El correo no puede estar vacío.")
            
        while True:
            telefono = input("Teléfono de contacto: ").strip()
            if telefono: break
            print(" El teléfono no puede estar vacío.")

        # BLOQUE DE VALIDACIÓN: Tipo de paciente (Entero en rango)
        print("\nSeleccione el tipo de paciente:\n1. Estudiante UAM\n2. Docente / Administrativo UAM\n3. Público General")
        while True:
            try:
                tipo_op = int(input("Opción (1-3): ").strip())
                if 1 <= tipo_op <= 3:
                    break
                print(" Selección fuera de rango. Ingrese 1, 2 o 3.")
            except ValueError:
                print(" Entrada inválida. Debe ingresar un número entero.")

        tipos_map = {1: "Estudiante", 2: "Docente", 3: "Publico"}
        nuevo_paciente = Paciente(cedula, nombre, correo, telefono, tipos_map[tipo_op])
        self.base_pacientes[cedula] = nuevo_paciente
        print(" Paciente registrado exitosamente.\n")
        return nuevo_paciente

    def flujo_agendar_cita(self):
        print("\n=============================================")
        print("     PROCESO DE AGENDAMIENTO DE CITAS UAM    ")
        print("=============================================")
        
        paciente = self.registrar_o_buscar_paciente()
        especialidades = self.grafo_agenda.listar_especialidades()
        
        print("Especialidades disponibles:")
        for idx, esp in enumerate(especialidades, 1):
            print(f"{idx}. {esp}")

        # BLOQUE DE VALIDACIÓN: Selección de Especialidad
        while True:
            try:
                op_esp = int(input(f"Seleccione una especialidad (1-{len(especialidades)}): ").strip())
                if 1 <= op_esp <= len(especialidades):
                    break
                print(f" Fuera de rango. Ingrese un número entre 1 y {len(especialidades)}.")
            except ValueError:
                print(" Entrada inválida. Debe ingresar un número entero.")

        especialidad_deseada = especialidades[op_esp - 1]
        nivel_urgencia = self.arbol_triaje.ejecutar_evaluacion()
        asignacion = self.grafo_agenda.buscar_cupo_optimo(especialidad_deseada, nivel_urgencia)

        if not asignacion:
            print(" Lo sentimos, no hay cupos disponibles.")
            return

        if nivel_urgencia == 1 and asignacion["especialidad"] != especialidad_deseada:
            print(f"\n NOTA: Por su alta urgencia, el sistema reorientó su cita a {asignacion['especialidad']}.")

        cita = CitaMedica(paciente, asignacion["especialidad"], asignacion["medico"], asignacion["horario"], nivel_urgencia)
        self.lista_citas.append(cita)

        print("\n--- COMPROBANTE DE CITA ---")
        print(f"Folio : {cita.folio_codigo} | Paciente: {cita.paciente.nombre_completo}")
        print(f"Médico: {cita.medico} | Horario: {cita.fecha_hora} ({asignacion['espera_horas']}h espera)\n")

    def menu_principal(self):
        while True:
            print("\n=== SISTEMA CLINICA UAM ===")
            print("1. Agendar Cita Médica")
            print("2. Salir")
            
            # BLOQUE DE VALIDACIÓN: Menú principal
            while True:
                try:
                    opcion = int(input("Seleccione una opción (1-2): ").strip())
                    if opcion in [1, 2]:
                        break
                    print(" Opción inválida.")
                except ValueError:
                    print(" Debe ingresar un número.")
            
            if opcion == 1:
                self.flujo_agendar_cita()
            elif opcion == 2:
                print("Saliendo del sistema...")
                break

SistemaClinicaUAM().menu_principal()