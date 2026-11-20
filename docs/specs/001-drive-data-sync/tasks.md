# Lista de Tareas: Fase 1 - Core Data Pipeline y Sincronización Google Drive
**Código:** SPEC-001  

---

- [x] **1.1 Backend: Pipeline de Datos y Capa de Caché:**
  - [x] Enriquecer modelos Pydantic en `Backend/app/models/empresario.py` (metadatos de sincronización).
  - [x] Implementar `Backend/app/services/data_pipeline_service.py` con caché en memoria (TTL 10 min) y manejo de fallback resiliente.
  - [x] Actualizar router `Backend/app/api/empresarios.py` con `GET /api/empresarios`, `GET /api/empresarios/{id}` y `POST /api/empresarios/sincronizar`.

- [x] **1.2 Frontend: Custom Hook y UI Reactiva:**
  - [x] Actualizar `Frontend/src/services/empresarioService.js` con métodos para forzar sincronización y consultar detalle.
  - [x] Crear custom hook `Frontend/src/hooks/useEmpresarios.js` desacoplando la lógica de negocio de la UI.
  - [x] Actualizar `Frontend/src/components/layout/Header.jsx` con botón interactivo de sincronización y estado real de Drive.
  - [x] Integrar `useEmpresarios` en `Frontend/src/App.jsx`.

- [x] **1.3 Verificación y Publicación:**
  - [x] Probar compilación del Frontend (`npm run build` - 104 módulos).
  - [x] Probar data pipeline en backend con detección automática de `api_disabled`.
  - [x] Realizar commit atómico en `feature/fase-1-drive-data-sync`.
  - [x] Publicar rama en GitHub y generar Pull Request hacia `develop`.
