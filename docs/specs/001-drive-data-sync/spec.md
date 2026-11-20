# Especificación Técnica: Fase 1 - Core Data Pipeline y Sincronización Google Drive
**Código:** SPEC-001  
**Proyecto:** Asistente Inteligente de Consultoría (Fundación WWB Colombia)  
**Estado:** En Progreso  
**Rama Git:** `feature/fase-1-drive-data-sync`  

---

## 1. Problema y Objetivos
En la operación diaria de los consultores de la Fundación WWB Colombia, la información de los microempresarios reside en Google Drive:
* Una hoja maestra (`Lista Emprendedores.xlsx`) con datos de contacto y negocio.
* Una carpeta de bitácoras individuales (`Asesorias_2026/`) con libros Excel por cada asesoría.

Actualmente, consultar la API de Google Drive en cada petición HTTP produce:
1. **Alta latencia (3 a 6 segundos por petición)** afectando la fluidez del consultor.
2. **Consumo excesivo de cuota de Google Drive API.**
3. **Fragilidad ante fallas de red o errores de configuración de Google Cloud (ej. API deshabilitada temporalmente).**

### Objetivos de la Fase 1:
* Implementar una **capa de caché en memoria con TTL de 10 minutos** en el backend para servir el listado de empresarios en < 50 ms.
* Proveer un mecanismo de **sincronización forzada bajo demanda (`POST /api/empresarios/sincronizar` o `?force=true`)**.
* Diseñar un **modo de resiliencia y degradación elegante**: si Google Drive no está disponible, el sistema informa el estado exacto sin lanzar error HTTP 500 y provee datos de contingencia.
* Implementar el endpoint de detalle **`GET /api/empresarios/{id}`**.
* Implementar en el Frontend el custom hook **`useEmpresarios`** y el botón interactivo de sincronización en el `Header`.

---

## 2. Requerimientos Funcionales y Criterios de Aceptación (Gherkin)

### US-01: Listado de Empresarios con Caché en Memoria
```gherkin
Escenario: Consulta del listado en condiciones normales
  Dado que los datos de empresarios fueron sincronizados desde Drive hace menos de 10 minutos
  Cuando el Frontend solicita GET /api/empresarios
  Entonces el Backend responde en menos de 50 ms utilizando la caché en memoria
  Y la respuesta incluye el estado de conexión "connected" y la fecha de última sincronización.
```

### US-02: Sincronización Manual Forzada
```gherkin
Escenario: El consultor presiona el botón "Sincronizar con Drive"
  Dado que se agregaron nuevas bitácoras en Google Drive
  Cuando el usuario presiona el botón en la interfaz (disparando POST /api/empresarios/sincronizar)
  Entonces el Backend invalida la caché, consulta Google Drive y actualiza la lista
  Y el Frontend muestra un indicador de carga y actualiza el contador de empresarios.
```

### US-03: Resiliencia ante Desconexión o Cuota Agotada
```gherkin
Escenario: Falla temporal de Google Drive API o credenciales
  Dado que la API de Google Drive no responde o está deshabilitada en Google Cloud
  Cuando se consulta GET /api/empresarios
  Entonces el sistema responde con código HTTP 200 con bandera drive_status: "disconnected"
  Y entrega el listado de contingencia con mensaje explicativo para el usuario.
```

### US-04: Consulta de Detalle de Empresario Específico
```gherkin
Escenario: Selección de un empresario en el panel
  Dado que existe un empresario con cédula "80442045"
  Cuando se consulta GET /api/empresarios/80442045
  Entonces se retorna el objeto completo con datos de la bitácora vinculada.
```
