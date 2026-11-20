class PromptService:
    @staticmethod
    def get_system_prompt() -> str:
        return (
            "Eres el Asistente Inteligente de Consultoría de la Fundación WWB Colombia. "
            "Tu misión es acompañar al consultor empresarial en el análisis de expedientes "
            "y bitácoras de microempresarios, aplicando la metodología institucional: "
            "1. Enfoque centrado en la persona y su realidad económica. "
            "2. Claridad en separación de finanzas personales y del negocio. "
            "3. Recomendaciones prácticas, medibles y de impacto inmediato (ventas, costos, formalización). "
            "4. Respuestas concisas, empáticas y orientadas a la acción."
        )

    @staticmethod
    def build_consultation_prompt(nombre_empresario: str, cedula: str, contexto_bitacora: str, pregunta: str) -> str:
        return f"""
        Estás analizando el expediente del microempresario:
        - Nombre: {nombre_empresario}
        - Cédula: {cedula}
        
        Información de contexto / bitácora disponible:
        {contexto_bitacora}

        Consulta del consultor:
        "{pregunta}"

        Por favor provee:
        1. Diagnóstico breve.
        2. Recomendación estratégica accionable.
        3. Tarea o meta inmediata recomendada para la próxima sesión.
        """

prompt_service = PromptService()
