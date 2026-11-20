# Lista de Tareas: Fase 0 - Saneamiento Técnico y Fundación
**Código:** SPEC-000  

---

- [x] **0.1 Seguridad y Control de Versiones:**
  - [x] Crear `.gitignore` con exclusión estricta de `credentials.json`, `*.env` y `node_modules/`.
  - [x] Crear `Backend/.env.example`.
  - [x] Inicializar Git en rama `main`.
  - [x] Crear rama `develop` y publicar ambas en GitHub.
  - [x] Crear y cambiar a rama de corta duración `feature/fase-0-saneamiento`.

- [x] **0.2 Saneamiento de Backend:**
  - [x] Crear `Backend/requirements.txt`.
  - [x] Implementar `Backend/app/config/settings.py` con variables de entorno.
  - [x] Implementar modelos en `Backend/app/models/` (`empresario.py`, `consulta.py`).
  - [x] Implementar constantes y helpers en `Backend/app/utils/` (`constants.py`, `helpers.py`).
  - [x] Implementar `prompt_service.py` con metodología WWB y robustecer `gemini_service.py`.
  - [x] Implementar router `ia.py` y corregir imports en router `empresarios.py`.
  - [x] Crear entrypoint modular `Backend/app/main.py` y actualizar `Backend/main.py`.
  - [x] Corregir `Backend/test_integration.py` para importar desde `app.services`.
  - [x] Diagnosticar estado de la API de Google Drive (detección del error 403 API no habilitada en proyecto Google Cloud).

- [x] **0.3 Saneamiento de Frontend:**
  - [x] Agregar `axios` a `Frontend/package.json`.
  - [x] Corregir import de `SearchInput` en `Frontend/src/components/layout/Header.jsx`.
  - [x] Refactorizar `Frontend/src/components/ia/ChatPanel.jsx` para invocar el servicio de IA de forma asíncrona.
  - [x] Reconstruir `Frontend/src/App.jsx` eliminando duplicación y ensamblando los componentes atómicos.
  - [x] Actualizar `Frontend/src/services/empresarioService.js` con soporte de fallback y timeout.

- [x] **0.4 Verificación, Compilación y Publicación:**
  - [x] Validar instalación y build del frontend (`npm run build`).
  - [ ] Realizar commit atómico de los cambios en `feature/fase-0-saneamiento`.
  - [ ] Publicar rama `feature/fase-0-saneamiento` en GitHub (`origin`).
  - [ ] Preparar el Pull Request hacia `develop` para revisión.
