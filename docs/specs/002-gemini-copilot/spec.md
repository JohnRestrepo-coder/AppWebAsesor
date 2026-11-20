# Especificación Técnica: Fase 2 - Asistente Copiloto Gemini AI
**Código:** SPEC-002  
**Proyecto:** Asistente Inteligente de Consultoría (Fundación WWB Colombia)  
**Estado:** En Progreso  
**Rama Git:** `feature/fase-2-gemini-copilot`  

---

## 1. Problema y Visión
El consultor empresarial de la Fundación WWB Colombia maneja expedientes y bitácoras de asesoría individuales en Excel. Diagnosticar manualmente la situación financiera, identificar si el empresario mezcla finanzas personales con el negocio o preparar un plan de acción para la próxima sesión requiere tiempo de análisis que limita la cantidad y calidad de asesorías.

### Propósito de la Fase 2:
Dotar a la plataforma de un **copiloto inteligente impulsado por Gemini AI** que actúe como asistente estratégico del consultor en tiempo real:
1. **RAG Ligero sobre Bitácora:** Extraer el contexto real del microempresario (sector, diagnóstico, estructura de costos y problemáticas) para alimentar el prompt de Gemini.
2. **Inyección Metodológica WWB:** Aplicar las directrices de consultoría de la Fundación WWB Colombia (enfoque práctico, lenguaje claro, recomendaciones accionables y metas semanales).
3. **Quick Prompts Especializados:** Botones de un solo clic en la interfaz para análisis recurrentes (*"📊 Analizar ventas"*, *"🎯 Generar plan de acción"*, *"⚠️ Encontrar riesgos"*, *"📋 Preparar próxima asesoría"*).
4. **Chat Interactivo con Memoria de Sesión:** Conversación fluida con indicador de procesamiento y renderizado visual en Markdown.

---

## 2. Historias de Usuario (Formato Gherkin)

### US-04: Consulta Contextualizada con Datos de Bitácora
```gherkin
Escenario: El consultor realiza una pregunta sobre el empresario activo
  Dado que el consultor tiene seleccionado al empresario "Raúl Hernán Ortiz"
  Cuando envía la consulta "¿Cómo puedo mejorar su margen de ganancia?"
  Entonces el sistema inyecta automáticamente el sector ("Madera y Muebles"), bitácora y diagnóstico
  Y Gemini genera una recomendación estratégica alineada con la metodología de la Fundación WWB.
```

### US-05: Activación de Quick Prompts
```gherkin
Escenario: El consultor pulsa el botón "📊 Analizar ventas"
  Dado que hay un empresario activo en pantalla
  Cuando el usuario hace clic en el botón rápido de análisis
  Entonces el sistema envía el prompt preconfigurado a Gemini
  Y muestra la respuesta estructurada con diagnóstico, acción sugerida y meta semanal.
```

### US-06: Resiliencia ante Ausencia de API Key o Bitácora
```gherkin
Escenario: No se ha configurado GEMINI_API_KEY o el empresario no tiene bitácora vinculada
  Dado que el sistema opera en modo local o el expediente no tiene archivo .xlsx
  Cuando se envía una consulta al Asistente
  Entonces el sistema responde con una recomendación simulada de contingencia
  Y notifica amigablemente que se encuentra en modo desarrollo sin interrumpir la experiencia.
```
