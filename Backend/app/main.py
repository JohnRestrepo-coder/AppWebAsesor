from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from app.api import empresarios, ia, minutas
    from app.config.settings import settings
except ImportError:
    from api import empresarios, ia, minutas
    from config.settings import settings

app = FastAPI(
    title="Backend Consultor WWB - Asistente Inteligente de Consultoría",
    description="API para la gestión de expedientes de microempresarios, asistencia IA y minutas de voz (Fundación WWB Colombia)",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de Routers Modulares
app.include_router(empresarios.router)
app.include_router(ia.router)
app.include_router(minutas.router)

@app.get("/", tags=["General"])
def root():
    return {
        "sistema": "Asistente Inteligente de Consultoría - Fundación WWB Colombia",
        "estado": "operativo",
        "version": "1.0.0"
    }

@app.get("/health", tags=["General"])
def health_check():
    return {"status": "ok"}
