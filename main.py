from experta import Fact, Field, Rule, KnowledgeEngine, NOT, MATCH

# Definición de hechos
class Paciente(Fact):
    """Información sobre el paciente."""
    id = Field(str, mandatory=True)
    fiebre = Field(bool, default=False)
    tos = Field(bool, default=False)
    dolor_de_garganta = Field(bool, default=False)
    dolor_de_cabeza = Field(bool, default=False)
    nausea = Field(bool, default=False)
    dolor_abdominal = Field(bool, default=False)
    fatiga = Field(bool, default=False)

class HistorialMedico(Fact):
    """Historial médico del paciente."""
    paciente_id = Field(str, mandatory=True)
    fumador = Field(bool, default=False)
    hipertension = Field(bool, default=False)

# Motor de conocimiento
class SistemaExpertoMedico(KnowledgeEngine):
    @Rule(Paciente(fiebre=True, dolor_de_garganta=True, id=MATCH.id),
          HistorialMedico(paciente_id=MATCH.id, fumador=True))
    def diagnosticar_gripe_fumador(self, id):
        print(f"Paciente {id}: Posible gripe. Nota: El paciente es fumador, atención adicional requerida.")

    @Rule(Paciente(fiebre=True, tos=True, dolor_de_cabeza=True))
    def diagnosticar_influenza(self):
        print("Diagnóstico: Posible influenza.")

    @Rule(Paciente(dolor_abdominal=True, fiebre=True), NOT(Paciente(nausea=True)))
    def diagnosticar_apendicitis(self):
        print("Diagnóstico: Posible apendicitis. Urgencia: Buscar atención médica inmediata.")

    @Rule(Paciente(fiebre=True, dolor_de_cabeza=True, rigidez_de_cuello=True))
    def diagnosticar_meningitis(self):
        print("Diagnóstico: Posible meningitis. Recomendación: Acudir al hospital inmediatamente.")

    @Rule(Paciente(fiebre=True, dolor_de_cabeza=True, id=MATCH.id),
          HistorialMedico(paciente_id=MATCH.id, hipertension=True))
    def check_conditions_hypertension(self, id):
        print(f"Paciente {id}: Presenta fiebre y dolor de cabeza con historial de hipertensión. Monitorizar presión arterial.")

# Ejecución del sistema experto
if __name__ == "__main__":
    engine = SistemaExpertoMedico()
    engine.reset()  # Reiniciar el motor de conocimientos
    engine.declare(Paciente(id="001", fiebre=True, tos=False, dolor_de_garganta=True, dolor_de_cabeza=True))
    engine.declare(HistorialMedico(paciente_id="001", fumador=False, hipertension=True))
    engine.run()  # Ejecutar el motor para evaluar las reglas
