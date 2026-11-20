# Plan de Implementación: Fase 2 - Asistente Copiloto Gemini AI
**Código:** SPEC-002  
**Rama:** `feature/fase-2-gemini-copilot`  

---

## 1. Arquitectura del Flujo de Inferencia (RAG Ligero)

```
[ FRONTEND React ]
     │
     ├── ChatPanel (Historial, QuickPrompts, Spinner)
     │       │
     │       ▼ (POST /api/consulta-ia { empresario_id, pregunta, tipo_analisis })
     │
[ BACKEND FastAPI ]
     │
     ├── 1. Identificar empresario en DataPipelineService (Memoria RAM)
     │
     ├── 2. Extraer contexto de bitácora (ExcelService / Resumen de Expediente)
     │
     ├── 3. Construir Prompt con Metodología WWB (PromptService)
     │       ├── Rol: Consultor Experto Fundación WWB Colombia
     │       ├── Contexto: Cédula, Nombre, Sector, Bitácora
     │       └── Consulta del usuario / Intención del Quick Prompt
     │
     ├── 4. Inferencia con Gemini (GeminiConsultantService)
     │       └── Fallback resiliente si GEMINI_API_KEY no está configurada
     │
     └── 5. Retornar Respuesta estructurada en Markdown hacia React
```

---

## 2. Componentes a Desarrollar / Modificar

1. **Backend:**
   * `app/services/excel_service.py`: Agregar función para extracción estructurada de hojas y celdas de bitácoras.
   * `app/services/prompt_service.py`: Enriquecer plantillas con directrices oficiales de consultoría WWB.
   * `app/services/gemini_service.py`: Soporte de modelos `gemini-1.5-flash` / `gemini-2.5` y manejo robusto de excepciones.
   * `app/api/ia.py`: Ampliar endpoint para recibir metadatos y retornar contexto utilizado.
   * `tests/`: Crear suite de pruebas unitarias (`test_prompt_service.py`, `test_excel_service.py`).
2. **Frontend:**
   * `src/components/ia/ChatPanel.jsx`: Soporte de Quick Prompts instantáneos, reseteo contextual al cambiar de empresario, renderizado Markdown y feedback de estado.
   * `src/services/empresarioService.js`: Soporte de `tipo_analisis` en `consultarIA`.
