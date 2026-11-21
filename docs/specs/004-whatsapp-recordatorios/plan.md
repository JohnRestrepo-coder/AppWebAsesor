# Plan de Implementación: Fase 4 - Automatización de Recordatorios por WhatsApp (wa.me)
**Código:** SPEC-004  
**Rama:** `feature/fase-4-whatsapp-recordatorios`  

---

## 1. Arquitectura de Mensajería wa.me

```
[ FRONTEND React ]
     │
     ├── TareaItem (Compromiso del Microempresario)
     │       │
     │       ▼ Clic en "📲 WhatsApp"
     │  whatsappHelper.js / Backend Link
     │       │
     │       ├── 1. Normaliza teléfono (10 dígitos -> 57XXXXXXXXXX)
     │       ├── 2. Inyecta plantilla con metodología Fundación WWB
     │       ├── 3. Aplica encodeURIComponent al texto
     │       └── 4. Abre https://wa.me/57XXXXXXXXXX?text=... en nueva pestaña
     │
[ WHATSAPP WEB / APP MÓVIL ]
     └── Mensaje pre-llenado listo para que el consultor presione [Enviar] (Cero costo de API)
```

---

## 2. Componentes a Desarrollar / Modificar

1. **Backend:**
   * `app/services/whatsapp_service.py`: Normalizador telefónico, constructor de mensajes institucionales y generador de URL segura.
   * `app/models/minuta.py`: Inclusión de `enlace_whatsapp` en `TareaItem` y `telefono_empresario` en `MinutaVozResponse`.
   * `app/models/empresario.py`: Inclusión del campo `telefono` en el expediente del microempresario.
   * `app/api/minutas.py`: Generación automática del enlace en cada tarea del microempresario al procesar la minuta.
   * `tests/test_whatsapp_service.py`: Pruebas unitarias de limpieza telefónica y codificación de URLs.
2. **Frontend:**
   * `src/utils/whatsappHelper.js`: Módulo de utilidad para generación y apertura de enlaces en cliente.
   * `src/components/minuta/MinutaVozModal.jsx`: Botón activo interactivo con ícono de WhatsApp y apertura directa.
   * `src/components/empresario/ProblematicasCard.jsx` / `CompromisosCard.jsx`: Integración de vista persistente de compromisos en el panel principal.
