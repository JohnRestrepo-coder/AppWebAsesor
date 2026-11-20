import unittest
from app.services.gemini_service import GeminiConsultantService

class TestGeminiService(unittest.TestCase):
    def setUp(self):
        self.service = GeminiConsultantService()

    def test_generar_respuesta_contingencia_ventas(self):
        resp = self.service._generar_respuesta_contingencia("Raúl Ortiz", "ventas")
        self.assertIn("Raúl Ortiz", resp)
        self.assertIn("Diagnóstico Clave", resp)
        self.assertIn("Recomendación Estratégica", resp)
        self.assertIn("Compromiso", resp)

    def test_generar_respuesta_contingencia_costos(self):
        resp = self.service._generar_respuesta_contingencia("María Yepes", "costos")
        self.assertIn("María Yepes", resp)
        self.assertIn("Fundación WWB", resp)
        self.assertIn("negocio no es la del bolsillo", resp)

    def test_generar_respuesta_contingencia_plan_accion(self):
        resp = self.service._generar_respuesta_contingencia("Stefanny Bernal", "plan_accion")
        self.assertIn("Stefanny Bernal", resp)
        self.assertIn("Plan de Acción a 7 Días", resp)

if __name__ == "__main__":
    unittest.main()
