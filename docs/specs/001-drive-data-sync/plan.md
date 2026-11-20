# Plan de Implementación: Fase 1 - Core Data Pipeline y Sincronización Google Drive
**Código:** SPEC-001  
**Rama:** `feature/fase-1-drive-data-sync`  

---

## 1. Arquitectura Técnica

```
[ FRONTEND React ]
     │
     ├── useEmpresarios Hook (Caché local, debounce, estado sync)
     │       │
     │       ▼
     │  Header (Botón "Sincronizar", badge de estado de Drive)
     │       │
     │       ▼ (HTTP GET/POST)
     │
[ BACKEND FastAPI ]
     │
     ├── Router: /api/empresarios (GET listado, GET /{id}, POST /sincronizar)
     │       │
     │       ▼
     ├── Data Pipeline Service (Memory Cache con TTL 10 min)
     │       │
     │       ├── Si caché válida: Retorna inmediatamente (< 50ms)
     │       │
     │       └── Si expirada o ?force=true:
     │               ├── Intenta Google Drive API (Maestro + Asesorias_2026)
     │               └── Si falla: Activa modo Resiliencia / Fallback estructurado
```

---

## 2. Componentes a Desarrollar / Modificar

1. **Backend:**
   * `Backend/app/models/empresario.py`: Enriquecer modelo con `drive_status`, `ultima_sincronizacion` y respuesta de lista con metadatos.
   * `Backend/app/services/data_pipeline_service.py`: Nuevo servicio orquestador con caché en memoria y resiliencia.
   * `Backend/app/api/empresarios.py`: Exponer endpoints actualizados (`GET /`, `GET /{id}`, `POST /sincronizar`).
2. **Frontend:**
   * `Frontend/src/hooks/useEmpresarios.js`: Nuevo custom hook para encapsular la lógica de estado y llamadas.
   * `Frontend/src/components/layout/Header.jsx`: Botón interactivo de sincronización y badge dinámico de estado.
   * `Frontend/src/services/empresarioService.js`: Integración de endpoint de sincronización y detalle.
   * `Frontend/src/App.jsx`: Integración con `useEmpresarios`.
