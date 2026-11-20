import unittest
import io
import pandas as pd
from app.services.excel_service import ExcelService

class TestExcelService(unittest.TestCase):
    def test_generar_contexto_contingencia(self):
        contexto = ExcelService.generar_contexto_contingencia(
            nombre="Stefanny Bernal",
            empresa="Detalles Stefanny",
            sector="Artesanías"
        )
        self.assertIn("Diagnóstico Inicial", contexto)
        self.assertIn("Ventas", contexto)
        self.assertIn("Finanzas", contexto)

    def test_extraer_resumen_bitacora_dummy_excel(self):
        # Crear un libro Excel en memoria para la prueba
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_diagnostico = pd.DataFrame({
                "Concepto": ["Costos", "Ventas", "Separación de Dinero"],
                "Estado": ["Pendiente", "Regular", "Requiere acompañamiento"]
            })
            df_diagnostico.to_excel(writer, sheet_name="Diagnóstico", index=False)
        output.seek(0)

        resumen = ExcelService.extraer_resumen_bitacora(output.getvalue())
        self.assertIn("Diagnóstico", resumen)
        self.assertIn("Concepto: Costos", resumen)

if __name__ == "__main__":
    unittest.main()
