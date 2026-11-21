# Especificación Técnica: Fase 3 - Minutas por Voz y Clasificación Inteligente de Compromisos
**Código:** SPEC-003  
**Proyecto:** Asistente Inteligente de Consultoría (Fundación WWB Colombia)  
**Estado:** En Progreso  
**Rama Git:** `feature/fase-3-minuta-voz-tareas`  

---

## 1. Problema y Visión
Durante las sesiones de asesoría (presenciales o virtuales), los consultores de la Fundación WWB Colombia conversan con el microempresario, analizan la situación y pactan compromisos. Tomar notas manuales al mismo tiempo distrae al consultor y reduce la empatía y atención dedicada a la persona.

### Solución en la Fase 3:
1. **Dictado por Voz Nativo (Web Speech API):** Capturar la conversación o el dictado de cierre del consultor directamente desde el micrófono del navegador con idioma local (`es-CO`), sin consumir APIs de audio de pago.
2. **Estructuración y Separación Inteligente con Gemini:** Procesar el texto bruto de la conversación y extraer automáticamente:
   * **Resumen Ejecutivo de la Sesión:** Síntesis clara de los temas tratados.
   * **Tareas del Consultor:** Tareas técnicas o metodológicas (ej. validar bitácora de costos, preparar plantilla).
   * **Tareas del Microempresario:** Acciones prácticas y medibles para los siguientes 7 días (ej. no mezclar dinero, registrar ventas diarias).
3. **Panel Interactivo de Compromisos:** Visualización estructurada de las tareas con checkboxes para marcar completadas y botón de acción para contacto.

---

## 2. Historias de Usuario (Gherkin)

### US-07: Captura de Minuta por Voz en el Navegador
```gherkin
Escenario: El consultor dicta el resumen de la asesoría
  Dado que el consultor finaliza la sesión con el empresario activo
  Cuando presiona el botón "Iniciar Dictado" y habla al micrófono
  Entonces el navegador transcribe la voz a texto en tiempo real en la pantalla
  Y permite pausar, reanudar o editar el texto antes de procesarlo.
```

### US-08: Clasificación Automatizada de Compromisos
```gherkin
Escenario: Procesamiento del texto bruto con Gemini AI
  Dado que se ha capturado el texto del dictado
  Cuando el consultor hace clic en "Procesar Minuta con IA"
  Entonces el backend orquesta la consulta a Gemini solicitando un esquema JSON estricto
  Y la interfaz muestra el resumen y separa claramente las "Tareas del Consultor" y las "Tareas del Empresario".
```

### US-09: Resiliencia ante Ausencia de Soporte de Voz
```gherkin
Escenario: El navegador no soporta Web Speech API o no hay micrófono disponible
  Dado que el usuario accede desde un navegador sin soporte o sin permisos de micrófono
  Cuando ingresa al módulo de Minuta
  Entonces la interfaz permite escribir o pegar manualmente las notas de la sesión sin bloquearse.
```
