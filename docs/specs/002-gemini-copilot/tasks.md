# Lista de Tareas: Fase 2 - Asistente Copiloto Gemini AI
**Código:** SPEC-002  

---

- [x] **2.1 Backend: Lógica RAG y Prompts de Consultoría WWB:**
  - [x] Enriquecer `app/services/prompt_service.py` con directrices metodológicas WWB y plantillas por tipo de análisis.
  - [x] Actualizar `app/services/excel_service.py` con método de extracción contextual de bitácoras.
  - [x] Robustecer `app/services/gemini_service.py` con soporte para selección de modelo y captura de fallos.
  - [x] Enriquecer router `app/api/ia.py` con soporte para `tipo_analisis` y entrega de metadatos de contexto.

- [x] **2.2 Frontend: Experiencia de Chat y Quick Prompts:**
  - [x] Actualizar `Frontend/src/services/empresarioService.js` para pasar `tipo_analisis`.
  - [x] Mejorar `Frontend/src/components/ia/ChatPanel.jsx`: envío con un clic en Quick Prompts, reinicio de bienvenida al cambiar empresario y formato visual.
  - [x] Mejorar `Frontend/src/components/ia/QuickPrompts.jsx` con iconos y categorización.

- [x] **2.3 Pruebas Unitarias y Calidad:**
  - [x] Crear suite de pruebas en `Backend/tests/test_prompt_service.py`, `Backend/tests/test_excel_service.py` y `Backend/tests/test_gemini_service.py`.
  - [x] Ejecutar suite con unittest (8 de 8 pruebas pasadas exitosamente en 0.736s).
  - [x] Validar compilación del frontend con `npm run build` (104 módulos en 2.43s).

- [x] **2.4 Publicación:**
  - [x] Realizar commit atómico en `feature/fase-2-gemini-copilot`.
  - [x] Publicar rama en GitHub.
  - [x] Generar Pull Request hacia `develop` con su comentario completo.
