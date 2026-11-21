import os
import json
import re
from typing import Optional, Dict, Any
from app.services.prompt_service import prompt_service

try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

class GeminiConsultantService:
    """
    Servicio encargado de la orquestación del LLM para el Asistente Inteligente
    de Consultoría de la Fundación WWB Colombia.
    """
    DEFAULT_MODEL = "gemini-1.5-flash"

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = None
        self.active_model_name = self.DEFAULT_MODEL
        
        if self.api_key and HAS_GENAI:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(
                    model_name=self.DEFAULT_MODEL,
                    system_instruction=prompt_service.get_system_prompt()
                )
            except Exception as e:
                print(f"⚠️ Advertencia al inicializar Gemini: {e}")

    async def consultar(
        self, 
        prompt_contextualizado: str, 
        nombre_empresario: str = "Empresario",
        tipo_analisis: str = "general"
    ) -> str:
        """
        Ejecuta la inferencia con el modelo Gemini configurado.
        Si la API Key no está presente o falla, devuelve una respuesta simulada estructurada.
        """
        if self.model:
            try:
                response = self.model.generate_content(prompt_contextualizado)
                if response and response.text:
                    return response.text
            except Exception as e:
                print(f"⚠️ Error en llamada a Gemini API ({e}). Usando motor de contingencia.")

        return self._generar_respuesta_contingencia(nombre_empresario, tipo_analisis)

    async def procesar_minuta_voz(self, prompt_minuta: str, nombre_empresario: str = "Empresario") -> Dict[str, Any]:
        """
        Procesa el dictado de voz de la sesión de consultoría y extrae
        un JSON estructurado con el resumen y las tareas separadas.
        """
        if self.model:
            try:
                response = self.model.generate_content(prompt_minuta)
                if response and response.text:
                    texto = response.text.strip()
                    # Limpiar posibles bloques ```json ... ```
                    match = re.search(r'\{.*\}', texto, re.DOTALL)
                    if match:
                        return json.loads(match.group())
            except Exception as e:
                print(f"⚠️ Error procesando minuta con Gemini ({e}). Usando clasificador de contingencia.")

        return self._generar_minuta_contingencia(nombre_empresario)

    def _generar_minuta_contingencia(self, nombre_empresario: str) -> Dict[str, Any]:
        return {
            "resumen_sesion": (
                f"Sesión de asesoría metodológica con {nombre_empresario}. "
                "Se identificaron oportunidades para ordenar los registros diarios y fortalecer el canal de contacto con clientes."
            ),
            "tareas_consultor": [
                f"Revisar la pestaña de costos en la bitácora de {nombre_empresario} antes de la próxima asesoría.",
                "Estructurar un formato de catálogo rápido para compartir por WhatsApp."
            ],
            "tareas_empresario": [
                "Llevar el registro diario de todas las entradas y salidas de dinero durante los próximos 7 días.",
                "Separar físicamente el dinero de gastos del hogar de las ventas del negocio.",
                "Hacer una lista de los 10 clientes más frecuentes con su número de teléfono."
            ]
        }

    def _generar_respuesta_contingencia(self, nombre_empresario: str, tipo_analisis: str) -> str:
        respuestas = {
            "ventas": f"""### 📌 Diagnóstico Clave
Para **{nombre_empresario}**, las ventas dependen actualmente de recomendaciones directas y clientes recurrentes presenciales, sin canales formales de reactivación.

### 💡 Recomendación Estratégica (Paso a paso)
1. **Lista de difusión de clientes frecuentes:** Crear una lista en WhatsApp con los últimos 20 clientes para enviarles una promoción quincenal sencilla.
2. **Estandarización de precios:** Validar que los precios cubran el costo de reposición de la materia prima.
3. **Catálogo visual básico:** Fotografiar los 5 productos con mayor margen y compartirlos en estados de WhatsApp.

### 🎯 Compromiso para la Próxima Sesión
* **Microempresario:** Escribir en un cuaderno los 15 mejores clientes con número de teléfono.
* **Consultor:** Diseñar juntos el primer mensaje de fidelización en la siguiente asesoría.""",

            "costos": f"""### 📌 Diagnóstico Clave
En el expediente de **{nombre_empresario}** se observa el riesgo común en microempresas: tomar dinero de la caja diaria para gastos imprevistos del hogar.

### 💡 Recomendación Estratégica (Paso a paso)
1. **Regla de oro de la Fundación WWB:** La plata del negocio no es la del bolsillo. Asignarse un "sueldo simbólico" semanal fijo.
2. **Registro diario de entradas y salidas:** Usar el cuaderno de costos durante 7 días consecutivos sin saltarse ningún gasto menor.
3. **Punto de equilibrio:** Identificar cuánto es lo mínimo que debe vender al día para pagar costos fijos (arriendo, servicios, transporte).

### 🎯 Compromiso para la Próxima Sesión
* **Microempresario:** Llevar el registro completo de ingresos y gastos de esta semana en una sola hoja.
* **Consultor:** Revisar la hoja de cálculo de costos para definir el margen neto real.""",

            "plan_accion": f"""### 📌 Diagnóstico Clave
**{nombre_empresario}** requiere priorizar acciones de corto impacto para generar liquidez inmediata y ordenar la administración.

### 💡 Plan de Acción a 7 Días
1. **Día 1-2 (Orden Financiero):** Separar físicamente el dinero del negocio en un sobre o cuenta digital independiente.
2. **Día 3-4 (Ventas):** Ofrecer un combo o producto estrella a clientes que no compran hace más de un mes.
3. **Día 5-7 (Seguimiento):** Registrar el total recaudado y calcular la ganancia neta.

### 🎯 Compromiso para la Próxima Sesión
* Cumplir con la meta de ventas pactada y traer el cuaderno de bitácora con los números actualizados.""",

            "riesgos": f"""### 📌 Diagnóstico Clave
Riesgos prioritarios identificados para **{nombre_empresario}**:
* Concentración en pocos clientes o en una sola temporada.
* Falta de reserva para emergencias (colchón de flujo de caja).
* Dependencia exclusiva de un único proveedor de insumos.

### 💡 Recomendación Preventiva
1. **Diversificar proveedores:** Cotizar insumos con al menos dos proveedores alternativos en la ciudad.
2. **Ahorro de protección:** Destinar el 5% de cada venta a una alcancía o fondo de emergencias del negocio.
3. **Canal alternativo:** Empezar a captar pedidos por anticipado con 50% de abono.

### 🎯 Compromiso para la Próxima Sesión
* Identificar un proveedor alternativo y cotizar los 3 insumos de mayor rotación."""
        }

        return respuestas.get(tipo_analisis, f"""### 📌 Diagnóstico General
Análisis estratégico para **{nombre_empresario}** basado en la metodología de la Fundación WWB Colombia.

### 💡 Recomendación Estratégica
1. **Separación de cuentas:** Evitar mezclar finanzas personales y del negocio.
2. **Revisión de margen:** Asegurar que cada producto deje ganancia real descontando insumos y tiempo de trabajo.
3. **Canal de contacto activo:** Mantener comunicación constante con los clientes vía WhatsApp.

### 🎯 Compromiso para la Próxima Sesión
* Registrar todas las ventas y compras de la semana para evaluar el avance en la bitácora.""")

gemini_service = GeminiConsultantService()
