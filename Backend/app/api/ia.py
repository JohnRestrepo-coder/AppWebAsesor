from fastapi import APIRouter, HTTPException
from app.models.consulta import ConsultaIARequest, ConsultaIAResponse
from app.services.gemini_service import gemini_service
from app.services.prompt_service import prompt_service

router = APIRouter(prefix="/api", tags=["IA"])

@router.post("/consulta-ia", response_model=ConsultaIAResponse)
async def consultar_ia(request: ConsultaIARequest):
    """
    Endpoint para realizar consultas estratégicas a Gemini sobre un empresario.
    """
    try:
        contexto_bitacora = f"Empresario ID/Cédula: {request.empresario_id}."
        prompt_final = prompt_service.build_consultation_prompt(
            nombre_empresario=f"Empresario {request.empresario_id}",
            cedula=request.empresario_id,
            contexto_bitacora=contexto_bitacora,
            pregunta=request.pregunta
        )
        
        respuesta_texto = await gemini_service.consultar(prompt_final)
        
        return ConsultaIAResponse(
            respuesta=respuesta_texto,
            empresario_id=request.empresario_id,
            status="success"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en consulta IA: {str(e)}")
