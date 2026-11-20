CONSULTOR_WWB/
│
├── backend/                              # [CAPA SERVIDOR - Python / FastAPI]
│   ├── app/
│   │   ├── main.py                       # Entry Point del Servidor FastAPI. Configura CORS, middleware, excepciones y orquesta los routers de API.
│   │   │
│   │   ├── api/                          # [CAPA DE RUTAS HTTP / CONTROLADORES]
│   │   │   ├── empresarios.py            # Endpoints REST para gestión de empresarios (GET /api/empresarios, GET /api/empresarios/{id}).
│   │   │   └── ia.py                     # Endpoint para orquestar consultas a Gemini (POST /api/consulta-ia).
│   │   │
│   │   ├── services/                     # [CAPA DE LÓGICA DE NEGOCIO Y CONECTORES]
│   │   │   ├── drive_service.py          # Cliente Google Drive/Sheets API. Autentica y recupera/guarda libros Excel (.xlsx).
│   │   │   ├── gemini_service.py         # Cliente SDK `google-genai`. Gestiona el envío de contexto de bitácora y la inferencia del LLM.
│   │   │   └── prompt_service.py         # Inyecta la metodología de la Fundación WWB en las plantillas de prompts del sistema.
│   │   │
│   │   ├── models/                       # [CAPA DE MODELADO Y VALIDACIÓN - Pydantic]
│   │   │   ├── empresario.py             # Schemas Pydantic de entrada/salida para el dominio Empresario.
│   │   │   └── consulta.py               # Schemas Pydantic para el payload de consultas al Asistente IA.
│   │   │
│   │   ├── utils/                        # [UTILIDADES TRANSVERSALES]
│   │   │   ├── helpers.py                # Regex para parseo de nombres de bitácora (`Bitacora [Cédula] [Nombre].xlsx`) y sanitización.
│   │   │   └── constants.py              # Constantes globales del backend (rutas base de Drive, IDs de carpetas, configuraciones).
│   │   │
│   │   └── config/
│   │       └── settings.py               # Gestión de variables de entorno (.env) vía `pydantic-settings` (API Keys, OAuth Secrets).
│   │
│   ├── requirements.txt                  # Dependencias Python del backend (fastapi, uvicorn, google-genai, google-api-python-client, pandas, openpyxl).
│   └── .env                              # Claves privadas (GEMINI_API_KEY, GOOGLE_DRIVE_FOLDER_ID).
│
├── frontend/                             # [CAPA DE PRESENTACIÓN - React / SPA]
│   │
│   ├── public/                           # [RECURSOS ESTÁTICOS SERVIDOS DIRECTAMENTE]
│   │   └── logo-wwb.png                  # Logo institucional secundario/favicon.
│   │
│   ├── src/                              # [CÓDIGO FUENTE DE REACT]
│   │   │
│   │   ├── assets/                       # Imágenes e íconos estáticos procesados por Vite (`logo_fundacion_wwb_colombia.png`).
│   │   │
│   │   ├── components/                   # [COMPONENTES DE INTERFAZ REUTILIZABLES]
│   │   │   ├── layout/                   # Componentes de estructura SPA general
│   │   │   │   ├── Sidebar.jsx           # Navegación lateral estricta con paleta WWB (#1D327D) y banderas "Próximamente".
│   │   │   │   └── Header.jsx            # Barra superior con el buscador dinámico y estado de conexión a Drive.
│   │   │   │
│   │   │   ├── empresario/               # Componentes del dominio del Empresario
│   │   │   │   ├── BusinessBanner.jsx    # Banner encabezado con resumen del expediente activo.
│   │   │   │   ├── EmpresarioCard.jsx    # Tarjeta de perfil (Nombre, Cédula, Foto, Estado, Archivo vinculado).
│   │   │   │   ├── DiagnosticoCard.jsx   # Tarjeta de matriz de diagnóstico (Fortalezas, Oportunidades, Madurez).
│   │   │   │   └── ProblematicasCard.jsx # Tarjeta de categorización (Ventas, Marketing, Finanzas, Administración).
│   │   │   │
│   │   │   ├── ia/                       # Componentes del Asistente de Consultoría
│   │   │   │   ├── ChatPanel.jsx         # Contenedor orquestador del módulo del Asistente Inteligente.
│   │   │   │   ├── ChatMessage.jsx       # Componente atómico para renderizado de burbujas de conversación.
│   │   │   │   └── QuickPrompts.jsx      # Barra de botones de interacción rápida (Analizar ventas, Plan de acción, etc.).
│   │   │   │
│   │   │   └── ui/                       # Componentes atómicos/presentacionales
│   │   │       ├── SearchInput.jsx       # Input de búsqueda reutilizable con eventos de autocompletado.
│   │   │       └── WWBButton.jsx         # Botón personalizado con token cromático de la Fundación (#F0AD15 / #1D327D).
│   │   │
│   │   ├── hooks/                        # [CUSTOM HOOKS - LÓGICA REUTILIZABLE DESACOPLADA DE LA UI]
│   │   │   ├── useEmpresarios.js         # Estado y lógica de obtención, filtrado y selección de empresarios.
│   │   │   └── useAsistenteIA.js         # Estado de la conversación, llamadas asíncronas al endpoint de IA y manejo de prompts.
│   │   │
│   │   ├── services/                     # [CLIENTES HTTP / SERVICIOS DE COMUNICACIÓN]
│   │   │   ├── api.js                    # Instancia base de Axios con baseURL e interceptores para manejo de errores.
│   │   │   ├── empresarioService.js     # Funciones de llamada a los endpoints `/api/empresarios`.
│   │   │   └── iaService.js              # Funciones de llamada al endpoint `/api/consulta-ia`.
│   │   │
│   │   ├── styles/                       # [ESTILOS GLOBALES - CSS PURO]
│   │   │   ├── variables.css             # Tokens visuales CSS (:root) con paleta oficial (#1D327D, #F0AD15, sombras, radios).
│   │   │   ├── theme.css                 # Overrides de Bootstrap 5 para imitar interfaces Notion/Linear/VSCode.
│   │   │   └── global.css                # Reset CSS, utilidades de diseño flexbox/grid y reglas de desbordamiento (overflow).
│   │   │
│   │   ├── utils/                        # Funciones puras de utilidad (formateadores de texto, fechas).
│   │   │
│   │   ├── constants.js                  # Centralización de textos configurables, prompts predeterminados y mapeos de UI.
│   │   │
│   │   ├── App.jsx                       # Componente Orquestador Principal de la SPA. Administra el layout responsive y los estados de nivel superior.
│   │   └── main.jsx                      # Punto de entrada de React. Monta la aplicación en el DOM en `index.html`.
│   │
│   ├── package.json                      # Configuración de dependencias NPM y scripts de Vite (`dev`, `build`).
│   └── vite.config.js                    # Configuración del bundler Vite, alias de importación (`@`) y proxy hacia FastAPI.
│
└── README.md                             # Documentación técnica general de arquitectura, instalación y despliegue del proyecto.