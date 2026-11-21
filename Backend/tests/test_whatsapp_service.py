import unittest
import urllib.parse
from app.services.whatsapp_service import WhatsAppService

class TestWhatsAppService(unittest.TestCase):
    def test_normalizar_telefono_10_digitos(self):
        tel = WhatsAppService.normalizar_telefono("3151234567")
        self.assertEqual(tel, "573151234567")

    def test_normalizar_telefono_con_guiones_y_espacios(self):
        tel = WhatsAppService.normalizar_telefono("318-765 4321")
        self.assertEqual(tel, "573187654321")

    def test_normalizar_telefono_con_prefijo_existente(self):
        tel = WhatsAppService.normalizar_telefono("+57 312 345 6789")
        self.assertEqual(tel, "573123456789")

    def test_normalizar_telefono_vacio(self):
        self.assertEqual(WhatsAppService.normalizar_telefono(""), "")
        self.assertEqual(WhatsAppService.normalizar_telefono(None), "")

    def test_construir_mensaje_recordatorio_format(self):
        mensaje = WhatsAppService.construir_mensaje_recordatorio(
            nombre_empresario="Raúl Hernán Ortiz",
            empresa="Muebles Ortiz",
            descripcion_tarea="Registrar las ventas de la semana en el cuaderno",
            fecha_limite="el próximo martes"
        )
        self.assertIn("Raúl", mensaje)
        self.assertIn("Fundación WWB Colombia", mensaje)
        self.assertIn("Muebles Ortiz", mensaje)
        self.assertIn("Registrar las ventas", mensaje)
        self.assertIn("el próximo martes", mensaje)

    def test_generar_enlace_wa_url_encoded(self):
        mensaje = "Hola Raúl, compromiso: anotar gastos."
        enlace = WhatsAppService.generar_enlace_wa("3154567890", mensaje)

        self.assertTrue(enlace.startswith("https://wa.me/573154567890?text="))
        self.assertNotIn(" ", enlace)  # No deben quedar espacios sin codificar
        
        # Verificar decodificación
        query = urllib.parse.urlparse(enlace).query
        params = urllib.parse.parse_qs(query)
        self.assertEqual(params["text"][0], mensaje)

if __name__ == "__main__":
    unittest.main()
