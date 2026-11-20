# Plan de Implementación: Fase 0 - Saneamiento Técnico y Fundación
**Código:** SPEC-000  
**Proyecto:** Asistente Inteligente de Consultoría  

---

## 1. Arquitectura de Archivos Refactorizada

```
AppWebAsesor/
├── .gitignore                      # [NUEVO] Reglas de exclusión de seguridad
├── docs/specs/000-fase-0/          # [NUEVO] Spec Kit formal
├── Backend/
│   ├── .env.example                # [NUEVO] Plantilla de configuración
│   ├── requirements.txt            # [NUEVO] Dependencias Python fijadas
│   ├── main.py                     # [ACTUALIZADO] Proxy/entrypoint hacia app.main
│   ├── test_integration.py         # [CORREGIDO] Rutas de importación app.services
│   └── app/
│       ├── main.py                 # [NUEVO] Orquestador FastAPI y routers
│       ├── config/settings.py      # [IMPLEMENTADO] Pydantic Settings
│       ├── models/                 # [IMPLEMENTADOS] Esquemas Pydantic
│       ├── services/               # [CORREGIDOS] Resiliencia de rutas y Drive client
│       ├── api/                    # [IMPLEMENTADOS] Routers modulares (empresarios, ia)
│       └── utils/                  # [IMPLEMENTADOS] Constantes y parseo de nombres
└── Frontend/
    ├── package.json                # [ACTUALIZADO] Inclusión de axios
    └── src/
        ├── App.jsx                 # [REFACTORIZADO] Layout unificado y reactivo
        ├── services/               # [ACTUALIZADO] Manejo de errores y fallback mock
        └── components/             # [REPARADO] Imports y conexión de componentes
```

---

## 2. Estrategia de Ramas Git
1. `main`: Rama de producción / baseline.
2. `develop`: Rama principal de integración continua.
3. `feature/fase-0-saneamiento`: Rama de corta duración donde se aplican y prueban todos los cambios.
4. Pull Request en GitHub: `feature/fase-0-saneamiento` -> `develop`.
