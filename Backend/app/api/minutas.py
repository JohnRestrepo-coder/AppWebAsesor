from fastapi import APIRouter, HTTPException
import uuid
from app.models.minuta import MinutaVozRequest, MinutaVozResponse, TareaItem
from app.services.gemini_service import gemini_service
from app.services.prompt_service import prompt_service
from app.services.data_pipeline_service import data_pipeline_service

router = APIRouter(prefix="/api", tags=["Minutas y Tareas"])

@router.post("/minuta-voz", response_model=MinutaVozResponse)
async def procesar_minuta_voz(request: MinutaVozRequest):
    """
    Recibe la transcripción de voz de la sesión de asesoría, la analiza con Gemini
    y genera el resumen y las tareas separadas (Consultor vs Empresario).
    """
    try:
        empresario = data_pipeline_service.obtener_empresario_por_id(request.empresario_id)
        nombre = empresario.nombre if empresario else f"Empresario {request.empresario_id}"
        empresa = empresario.empresa if empresario else "Microempresa Registrada"

        prompt = prompt_service.build_voice_minute_prompt(
            nombre_empresario=nombre,
            empresa=empresa,
            texto_dictado=request.texto_dictado
        )

        datos_minuta = await gemini_service.procesar_minuta_voz(
            prompt_minuta=prompt,
            nombre_empresario=nombre
        )

        # Construir listas de TareaItem
        tareas_consultor = []
        for idx, desc in enumerate(datos_minuta.get("tareas_consultor", [])):
            tareas_consultor.append(TareaItem(
                id=f"tc-{uuid.uuid4().hex[:6]}",
                descripcion=str(desc),
                responsable="consultor",
                completada=False,
                fecha_limite="Próxima sesión (7 días)"
            ))

        tareas_empresario = []
        for idx, desc in enumerate(datos_minuta.get("tareas_empresario", [])):
            tareas_empresario.append(TareaItem(
                id=f"te-{uuid.uuid4().hex[:6]}",
                descripcion=str(desc),
                responsable="empresario",
                completada=False,
                fecha_limite="En 7 días"
            ))

        return MinutaVozResponse(
            empresario_id=request.empresario_id,
            nombre_empresario=nombre,
            resumen_sesion=datos_minuta.get("resumen_sesion", "Sesión de asesoría completada."),
            tareas_consultor=tareas_consultor,
            tareas_empresario=tareas_empresario,
            status="success"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la minuta de voz: {str(e)}")
