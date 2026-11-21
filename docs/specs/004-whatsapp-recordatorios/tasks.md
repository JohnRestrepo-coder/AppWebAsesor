# Lista de Tareas: Fase 4 - Automatización de Recordatorios por WhatsApp (wa.me)
**Código:** SPEC-004  

---

- [x] **4.1 Backend: Servicio de WhatsApp y Modelos:**
  - [x] Añadir campo `telefono` en `app/models/empresario.py` y actualizar lista de contingencia en `data_pipeline_service.py`.
  - [x] Añadir `enlace_whatsapp` a `TareaItem` y `telefono_empresario` a `MinutaVozResponse` en `app/models/minuta.py`.
  - [x] Crear `app/services/whatsapp_service.py` con normalizador de teléfonos (código país `57`), constructor de mensaje WWB y generador de enlaces `wa.me`.
  - [x] Actualizar `app/api/minutas.py` para inyectar el enlace de WhatsApp en cada tarea del microempresario.

- [x] **4.2 Frontend: Integración de Botones WhatsApp y Utilidades:**
  - [x] Crear `src/utils/whatsappHelper.js` con constructor de URL y apertura en nueva ventana.
  - [x] Actualizar `src/components/minuta/MinutaVozModal.jsx` para convertir las etiquetas en botones interactivos con acción directa.
  - [x] Actualizar `src/components/empresario/EmpresarioCard.jsx` mostrando el celular/WhatsApp del microempresario.

- [x] **4.3 Pruebas Unitarias y Compilación:**
  - [x] Crear `Backend/tests/test_whatsapp_service.py` validando normalización telefónica y codificación URL.
  - [x] Ejecutar suite con `unittest` (17 de 17 pruebas aprobadas al 100% en 0.643s).
  - [x] Validar compilación del frontend con `npm run build` (107 módulos en 2.35s).

- [x] **4.4 Publicación:**
  - [x] Realizar commit atómico en `feature/fase-4-whatsapp-recordatorios`.
  - [x] Publicar rama en GitHub.
  - [x] Generar Pull Request hacia `develop` con su título y comentario completo.
