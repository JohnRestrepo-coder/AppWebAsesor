import os
import google.generativeai as genai

class GeminiConsultantService:
    """
    Servicio encargado del procesamiento del lenguaje natural para el 
    Asistente Inteligente de Consultoría de la Fundación WWB Colombia.
    """
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Error de Configuración: GEMINI_API_KEY no encontrada en las variables de entorno.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=(
                "Eres el Asistente Inteligente de Consultoría de la Fundación WWB Colombia. "
                "Apoyas a los consultores analizando bitácoras de empresarios con enfoque estratégico."
            )
        )

    async def consultar(self, prompt_contextualizado: str) -> str:
        try:
            response = self.model.generate_content(prompt_contextualizado)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Error al comunicar con Gemini API: {str(e)}")