from typing import Optional

class PromptService:
    """
    Gestiona los prompts y directrices metodológicas de la Fundación WWB Colombia
    para el Asistente Inteligente de Consultoría Empresarial.
    """

    SYSTEM_PROMPT = (
        "Eres el Asistente Inteligente de Consultoría de la Fundación WWB Colombia. "
        "Tu misión es actuar como copiloto estratégico para los consultores que asesoran a microempresarios.\n\n"
        "DIRECTRICES METODOLÓGICAS OBLIGATORIAS:\n"
        "1. ENFOQUE EN LA PERSONA Y SU REALIDAD: Reconoce el contexto de la microempresa en Colombia (informalidad, recursos limitados, empuje y resiliencia).\n"
        "2. SEPARACIÓN DE FINANZAS: Enfatiza siempre la importancia de no mezclar la plata del bolsillo con la de la caja del negocio.\n"
        "3. LENGUAJE CLARO Y PRÁCTICO: Evita tecnicismos financieros abstractos (prefiere 'lo que te queda limpio' a 'margen EBITDA').\n"
        "4. ACCIONES CONCRETAS Y METAS SEMANALES: Cada recomendación debe terminar con 1 o 2 tareas inmediatas alcanzables en 7 días.\n"
        "5. ESTRUCTURA DE RESPUESTA: Presenta tus análisis en tres partes: [Diagnóstico Breve], [Recomendación Estratégica], [Compromiso / Próximo Paso]."
    )

    PLANTILLAS_ANALISIS = {
        "ventas": (
            "Enfócate en la estrategia comercial: validación de precios, canales de captación (digital vs presencial), "
            "frecuencia de recompra y fidelización de clientes actuales."
        ),
        "costos": (
            "Enfócate en la salud financiera: costos fijos vs variables, cálculo del margen bruto, "
            "identificación de fugas de dinero y separación de gastos del hogar vs negocio."
        ),
        "plan_accion": (
            "Estructura un plan de acción a 7 días con máximo 3 compromisos clave: uno para el consultor "
            "y dos para el microempresario, con fechas e indicadores sencillos."
        ),
        "riesgos": (
            "Identifica vulnerabilidades críticas en el negocio: dependencia de un solo cliente/proveedor, "
            "falta de flujo de caja para emergencias, inventario estancado o ausencia de canales digitales."
        ),
        "general": (
            "Realiza una consultoría estratégica balanceada considerando tanto la parte comercial como la operativa y financiera."
        )
    }

    @classmethod
    def get_system_prompt(cls) -> str:
        return cls.SYSTEM_PROMPT

    @classmethod
    def build_consultation_prompt(
        cls, 
        nombre_empresario: str, 
        cedula: str, 
        empresa: str, 
        sector: str, 
        contexto_bitacora: str, 
        pregunta: str,
        tipo_analisis: Optional[str] = "general"
    ) -> str:
        enfoque = cls.PLANTILLAS_ANALISIS.get(tipo_analisis, cls.PLANTILLAS_ANALISIS["general"])

        return f"""
DATOS DEL MICROEMPRESARIO:
- Nombre: {nombre_empresario}
- Cédula: {cedula}
- Negocio / Empresa: {empresa}
- Sector Económico: {sector}

CONTEXTO EXTRAÍDO DE LA BITÁCORA / EXPEDIENTE:
{contexto_bitacora}

ENFOQUE METODOLÓGICO SOLICITADO:
{enfoque}

CONSULTA ESPECÍFICA DEL CONSULTOR:
"{pregunta}"

INSTRUCCIONES DE RESPUESTA:
- Responde directamente al consultor de forma clara, empática y profesional.
- Utiliza formato Markdown con títulos y viñetas para que sea fácil de leer durante la sesión.
- Incluye:
  1. 📌 Diagnóstico Clave
  2. 💡 Recomendación Práctica (Paso a paso)
  3. 🎯 Compromiso Sugerido para la Próxima Sesión
"""

prompt_service = PromptService()
