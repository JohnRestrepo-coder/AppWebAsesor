# Especificación Técnica: Fase 4 - Automatización de Recordatorios por WhatsApp (wa.me)
**Código:** SPEC-004  
**Proyecto:** Asistente Inteligente de Consultoría (Fundación WWB Colombia)  
**Estado:** En Progreso  
**Rama Git:** `feature/fase-4-whatsapp-recordatorios`  

---

## 1. Problema y Visión
Uno de los mayores desafíos en las asesorías a microempresarios es el cumplimiento de compromisos entre sesión y sesión. Al terminar una asesoría, el microempresario vuelve a la rutina absorbente de su negocio y suele olvidar las tareas acordadas (anotar gastos, cotizar materias primas, etc.).

Contratar APIs de mensajería masiva (como Twilio o Meta WhatsApp Business Cloud API con costo por plantilla/conversación) representaría un gasto recurrente inviable. 

### Solución en la Fase 4:
Implementar un **módulo de mensajería 100% gratuito basado en enlaces universales de WhatsApp (`wa.me`)**:
1. **Normalización de Teléfonos:** Limpieza automática del número celular del empresario (eliminación de espacios, caracteres especiales y prefijo internacional `57` para Colombia).
2. **Plantillas Institucionales de la Fundación WWB:** Redacción dinámica de mensajes empáticos que incluyen el nombre del empresario, el nombre del negocio, la tarea específica pactada y la fecha de la próxima sesión.
3. **Acción a Un Clic:** El consultor presiona el botón de WhatsApp al lado de cualquier compromiso y se abre instantáneamente WhatsApp Web o la App móvil con el mensaje pre-escrito listo para enviar.

---

## 2. Historias de Usuario (Gherkin)

### US-10: Generación de Enlace WhatsApp para Tareas del Empresario
```gherkin
Escenario: El consultor desea enviar un recordatorio de compromiso
  Dado que se han generado las tareas del microempresario "Raúl Hernán Ortiz"
  Cuando el consultor hace clic en el botón "📲 Enviar por WhatsApp" de una tarea
  Entonces el sistema genera un enlace https://wa.me/57{telefono}?text={mensaje_codificado}
  Y abre WhatsApp Web o la aplicación con el mensaje listo para enviar.
```

### US-11: Manejo de Teléfonos y Fallbacks
```gherkin
Escenario: El expediente no cuenta con número telefónico registrado
  Dado que el empresario no tiene número celular en su expediente
  Cuando se intenta generar el enlace de WhatsApp
  Entonces el sistema solicita o permite ingresar el número telefónico en un diálogo interactivo
  Y genera el enlace sin romper la experiencia de usuario.
```
