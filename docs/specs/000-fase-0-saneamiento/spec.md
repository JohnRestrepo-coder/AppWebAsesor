# Especificación Técnica: Fase 0 - Saneamiento Técnico y Fundación
**Código:** SPEC-000  
**Proyecto:** Asistente Inteligente de Consultoría (Fundación WWB Colombia)  
**Estado:** En Progreso  
**Rama Git:** `feature/fase-0-saneamiento`  

---

## 1. Problema y Contexto
Al retomar el desarrollo del proyecto, se identificaron varios bloqueos técnicos que impedían la ejecución local y la integración continua:
1. **Error de importación en Backend (`donde_quedamos.md`):** `from services.drive_service import drive_service` fallaba con `ModuleNotFoundError` porque `services` se encuentra dentro de `Backend/app/services` y `main.py` residía en la raíz de `Backend/`.
2. **Inconsistencias y archivos vacíos (0 bytes) en Backend:** `settings.py`, `ia.py`, `models/` y `prompt_service.py` no tenían implementación.
3. **Falta de manifiesto de dependencias Backend:** Ausencia de `requirements.txt`.
4. **Colisión sintáctica crítica en Frontend (`App.jsx`):** Existían dos bloques de código superpuestos con doble `export default` y doble importación de React, provocando fallo de compilación en Vite.
5. **Import roto en `Header.jsx`:** Apuntaba a una ruta inexistente (`../ui/SearchInput` en vez de `./SearchInput`).
6. **Dependencia faltante en `package.json`:** `axios` se usaba en `empresarioService.js` pero no estaba en dependencias.
7. **Inexistencia de control de versiones y seguridad:** El proyecto no tenía repositorio Git ni `.gitignore`, con riesgo de exponer `credentials.json` y `.env`.

---

## 2. Requerimientos Funcionales y No Funcionales

### Funcionales
* **RF-01:** La aplicación debe permitir el arranque de FastAPI sirviendo los routers de `/api/empresarios` y `/api/consulta-ia`.
* **RF-02:** `test_integration.py` debe ejecutar la suite de comprobación importando desde `app.services.*` sin errores de ruta.
* **RF-03:** La SPA de React debe compilar limpiamente con Vite, mostrando el layout corporativo de la Fundación WWB y permitiendo buscar y seleccionar microempresarios.
* **RF-04:** Si el backend o Google Drive no están disponibles temporalmente, el frontend debe degradar elegantemente mostrando datos mock de desarrollo sin estrellarse.

### No Funcionales (Seguridad y Calidad)
* **RNF-01 (Seguridad):** `.gitignore` debe impedir de forma absoluta el versionado de `credentials.json`, `.env` y carpetas de dependencias (`node_modules/`, `venv/`).
* **RNF-02 (Modularidad):** Separación estricta entre capa de presentación (React), capa API (FastAPI routers), capa de negocio (`services/`) y capa de datos (`models/`).
* **RNF-03 (Estrategia Git):** Toda alteración debe desarrollarse en ramas de corta duración derivadas de `develop` y someterse a revisión en GitHub vía Pull Request.
