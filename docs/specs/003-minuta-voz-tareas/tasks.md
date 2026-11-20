# Lista de Tareas: Fase 3 - Minutas por Voz y Clasificación Inteligente de Compromisos
**Código:** SPEC-003  

---

- [x] **3.1 Backend: Pipeline de Clasificación JSON:**
  - [x] Crear modelos Pydantic en `app/models/minuta.py` (`MinutaVozRequest`, `TareaItem`, `MinutaVozResponse`).
  - [x] Implementar `build_voice_minute_prompt` en `app/services/prompt_service.py` con directivas JSON y metodología WWB.
  - [x] Implementar `procesar_minuta_voz` en `app/services/gemini_service.py` con extractor y validador JSON.
  - [x] Crear router `app/api/minutas.py` exponiendo `POST /api/minuta-voz`.
  - [x] Registrar router en `app/main.py`.

- [x] **3.2 Frontend: Módulo de Voz y Gestión de Compromisos:**
  - [x] Crear hook `src/hooks/useSpeechRecognition.js` con Web Speech API nativa (es-CO).
  - [x] Crear componente `src/components/minuta/MinutaVozModal.jsx` con interfaz de dictado, animación de grabación y panel de tareas.
  - [x] Actualizar `src/services/empresarioService.js` con método `procesarMinutaVoz`.
  - [x] Conectar modal en `src/App.jsx` y botón en `src/components/layout/Sidebar.jsx`.

- [x] **3.3 Pruebas Unitarias y Calidad:**
  - [x] Crear `Backend/tests/test_minuta_service.py` validando la separación de tareas y formato JSON.
  - [x] Ejecutar suite con `unittest` (11 de 11 pruebas aprobadas al 100% en 0.935s).
  - [x] Validar compilación del frontend con `npm run build` (106 módulos en 2.88s).

- [x] **3.4 Publicación:**
  - [x] Realizar commit atómico en `feature/fase-3-minuta-voz-tareas`.
  - [x] Publicar rama en GitHub.
  - [x] Generar Pull Request hacia `develop` con su comentario completo.
