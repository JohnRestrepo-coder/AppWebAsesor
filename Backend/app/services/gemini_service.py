import os
from app.services.prompt_service import prompt_service

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

class GeminiConsultantService:
    """
    Servicio encargado del procesamiento del lenguaje natural para el 
    Asistente Inteligente de Consultoría de la Fundación WWB Colombia.
    """
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        
        if self.api_key and HAS_GENAI:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=prompt_service.get_system_prompt()
                )
            except Exception as e:
                print(f"⚠️ Advertencia al inicializar Gemini: {e}")

    async def consultar(self, prompt_contextualizado: str) -> str:
        if not self.model:
            return (
                "🤖 [Modo Desarrollo / Simulación Gemini]\n\n"
                "Para obtener respuestas en tiempo real con Gemini, configura tu GEMINI_API_KEY en el archivo .env.\n\n"
                "Recomendación estratégica preliminar:\n"
                "1. Revisar la estructura de costos y punto de equilibrio en la bitácora del empresario.\n"
                "2. Validar canales digitales actuales de captación de clientes.\n"
                "3. Definir compromiso de seguimiento semanal vía WhatsApp."
            )

        try:
            response = self.model.generate_content(prompt_contextualizado)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Error al comunicar con Gemini API: {str(e)}")

gemini_service = GeminiConsultantService()
