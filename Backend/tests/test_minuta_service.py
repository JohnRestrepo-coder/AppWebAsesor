import unittest
from app.services.prompt_service import PromptService
from app.services.gemini_service import GeminiConsultantService
from app.models.minuta import MinutaVozResponse, TareaItem

class TestMinutaService(unittest.TestCase):
    def setUp(self):
        self.gemini = GeminiConsultantService()

    def test_build_voice_minute_prompt(self):
        prompt = PromptService.build_voice_minute_prompt(
            nombre_empresario="Luz Eugenia Pérez",
            empresa="Comercializadora Pérez",
            texto_dictado="Acordamos que el consultor revisará la lista de costos y Luz Eugenia registrará las ventas diarias."
        )
        self.assertIn("Luz Eugenia Pérez", prompt)
        self.assertIn("Comercializadora Pérez", prompt)
        self.assertIn("JSON", prompt)
        self.assertIn("tareas_consultor", prompt)
        self.assertIn("tareas_empresario", prompt)

    def test_generar_minuta_contingencia_structure(self):
        minuta = self.gemini._generar_minuta_contingencia("Astrid Natalia Aranda")
        self.assertIn("resumen_sesion", minuta)
        self.assertIn("tareas_consultor", minuta)
        self.assertIn("tareas_empresario", minuta)
        self.assertIsInstance(minuta["tareas_consultor"], list)
        self.assertIsInstance(minuta["tareas_empresario"], list)
        self.assertGreater(len(minuta["tareas_consultor"]), 0)
        self.assertGreater(len(minuta["tareas_empresario"]), 0)

    def test_minuta_response_pydantic_validation(self):
        tarea_c = TareaItem(id="c-1", descripcion="Revisar bitácora", responsable="consultor")
        tarea_e = TareaItem(id="e-1", descripcion="Anotar gastos", responsable="empresario")

        response = MinutaVozResponse(
            empresario_id="1061777035",
            nombre_empresario="Astrid Natalia Aranda",
            resumen_sesion="Sesión completada con éxito.",
            tareas_consultor=[tarea_c],
            tareas_empresario=[tarea_e]
        )
        self.assertEqual(response.status, "success")
        self.assertEqual(response.tareas_consultor[0].responsable, "consultor")
        self.assertEqual(response.tareas_empresario[0].responsable, "empresario")

if __name__ == "__main__":
    unittest.main()
