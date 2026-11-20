from fastapi import APIRouter, HTTPException
from app.models.consulta import ConsultaIARequest, ConsultaIAResponse
from app.services.gemini_service import gemini_service
from app.services.prompt_service import prompt_service
from app.services.data_pipeline_service import data_pipeline_service
from app.services.excel_service import excel_service
from app.services.drive_service import drive_service

router = APIRouter(prefix="/api", tags=["IA"])

@router.post("/consulta-ia", response_model=ConsultaIAResponse)
async def consultar_ia(request: ConsultaIARequest):
    """
    Endpoint para realizar consultas estratégicas a Gemini AI
    inyectando el contexto de la bitácora del microempresario activo.
    """
    try:
        # 1. Recuperar datos del empresario desde el catálogo en memoria
        empresario = data_pipeline_service.obtener_empresario_por_id(request.empresario_id)
        
        nombre = empresario.nombre if empresario else f"Empresario {request.empresario_id}"
        cedula = empresario.cedula if empresario else request.empresario_id
        empresa = empresario.empresa if empresario else "Microempresa Registrada"
        sector = empresario.sector if empresario else "Por Definir"

        # 2. Extraer contexto de bitácora
        contexto_bitacora = ""
        if empresario and empresario.tiene_bitacora and empresario.bitacora_file_id:
            try:
                bytes_excel = drive_service.descargar_archivo_bytes(empresario.bitacora_file_id)
                contexto_bitacora = excel_service.extraer_resumen_bitacora(bytes_excel)
            except Exception as e:
                contexto_bitacora = excel_service.generar_contexto_contingencia(nombre, empresa, sector)
        else:
            contexto_bitacora = excel_service.generar_contexto_contingencia(nombre, empresa, sector)

        # 3. Construir prompt enriquecido con metodología Fundación WWB
        tipo = request.tipo_analisis or "general"
        prompt_final = prompt_service.build_consultation_prompt(
            nombre_empresario=nombre,
            cedula=cedula,
            empresa=empresa,
            sector=sector,
            contexto_bitacora=contexto_bitacora,
            pregunta=request.pregunta,
            tipo_analisis=tipo
        )

        # 4. Inferencia con Gemini
        respuesta_texto = await gemini_service.consultar(
            prompt_contextualizado=prompt_final,
            nombre_empresario=nombre,
            tipo_analisis=tipo
        )

        return ConsultaIAResponse(
            respuesta=respuesta_texto,
            empresario_id=request.empresario_id,
            tipo_analisis=tipo,
            contexto_utilizado=f"Bitácora: {empresario.archivo_bitacora if empresario else 'Sintética'}",
            modelo=gemini_service.active_model_name,
            status="success"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en orquestación de IA: {str(e)}")
