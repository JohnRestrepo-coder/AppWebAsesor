# Plan de Implementación: Fase 3 - Minutas por Voz y Clasificación Inteligente de Compromisos
**Código:** SPEC-003  
**Rama:** `feature/fase-3-minuta-voz-tareas`  

---

## 1. Arquitectura del Flujo de Minutas y Clasificación

```
[ FRONTEND React ]
     │
     ├── 1. Web Speech API (Navegador local: Chrome/Edge/Safari - es-CO)
     │       └── Convierte voz a texto bruto
     │
     ├── 2. Modal / Panel de Minuta de Voz
     │       └── Permite al consultor editar o agregar notas
     │       │
     │       ▼ (POST /api/minuta-voz { empresario_id, texto_dictado })
     │
[ BACKEND FastAPI ]
     │
     ├── 3. Enriquecer con Contexto del Expediente (DataPipelineService)
     │
     ├── 4. Prompt Estructurado JSON (PromptService)
     │       └── Schema: { resumen, tareas_consultor, tareas_empresario }
     │
     ├── 5. Inferencia Gemini (GeminiConsultantService)
     │       └── Parseo robusto de JSON con fallback metodológico
     │
     └── 6. Retorno de MinutaVozResponse hacia React
             │
             ▼
[ FRONTEND React ]
     └── 7. Renderizado de Compromisos en Tablas Separadas
             ├── Tareas del Consultor (con checkboxes)
             └── Tareas del Empresario (con botón de preparación para WhatsApp)
```

---

## 2. Componentes a Desarrollar

1. **Backend:**
   * `app/models/minuta.py`: Esquemas Pydantic `MinutaVozRequest`, `TareaItem`, `MinutaVozResponse`.
   * `app/services/prompt_service.py`: Método `build_voice_minute_prompt`.
   * `app/services/gemini_service.py`: Método `procesar_minuta_voz`.
   * `app/api/minutas.py`: Nuevo router modular `POST /api/minuta-voz`.
   * `app/main.py`: Registro del nuevo router.
   * `tests/test_minuta_service.py`: Pruebas unitarias de estructura JSON.
2. **Frontend:**
   * `src/hooks/useSpeechRecognition.js`: Hook nativo para Web Speech API.
   * `src/components/minuta/MinutaVozModal.jsx`: Modal interactivo de grabación, edición y visualización de compromisos.
   * `src/services/empresarioService.js`: Función `procesarMinutaVoz`.
   * `src/App.jsx` y `src/components/layout/Sidebar.jsx`: Activación del acceso a Minutas.
