import unittest
from app.services.prompt_service import PromptService

class TestPromptService(unittest.TestCase):
    def test_system_prompt_contains_wwb_directives(self):
        prompt = PromptService.get_system_prompt()
        self.assertIn("Fundación WWB Colombia", prompt)
        self.assertIn("SEPARACIÓN DE FINANZAS", prompt)
        self.assertIn("ACCIONES CONCRETAS Y METAS SEMANALES", prompt)

    def test_build_consultation_prompt_ventas(self):
        prompt = PromptService.build_consultation_prompt(
            nombre_empresario="María Yepes",
            cedula="29740252",
            empresa="Pastelería Doña María",
            sector="Alimentos",
            contexto_bitacora="Bitácora con ventas bajas en mayo.",
            pregunta="¿Cómo mejorar las ventas de pasteles?",
            tipo_analisis="ventas"
        )
        self.assertIn("María Yepes", prompt)
        self.assertIn("Pastelería Doña María", prompt)
        self.assertIn("comercial", prompt)
        self.assertIn("¿Cómo mejorar las ventas de pasteles?", prompt)

    def test_build_consultation_prompt_costos(self):
        prompt = PromptService.build_consultation_prompt(
            nombre_empresario="Raúl Ortiz",
            cedula="80442045",
            empresa="Muebles Ortiz",
            sector="Madera",
            contexto_bitacora="Sin registro formal de costos.",
            pregunta="¿Cómo costear la madera?",
            tipo_analisis="costos"
        )
        self.assertIn("Raúl Ortiz", prompt)
        self.assertIn("costos fijos vs variables", prompt)

if __name__ == "__main__":
    unittest.main()
