class SistemaClinicaUAM:
    def _init_(self):
        self.base_pacientes = {}
        self.lista_citas = []
        self.arbol_triaje = ArbolTriajeBinario()
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

        print("👤 Paciente no registrado. Complete los datos requeridos:")
        
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

if _name_ == "_main_":
    SistemaClinicaUAM().menu_principal()