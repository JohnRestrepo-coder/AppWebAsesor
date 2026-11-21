import re
import urllib.parse
from typing import Optional

class WhatsAppService:
    """
    Servicio para la normalización de números de teléfono y generación
    de enlaces universales wa.me con plantillas metodológicas de la Fundación WWB Colombia.
    """
    CODIGO_PAIS_COLOMBIA = "57"

    @classmethod
    def normalizar_telefono(cls, telefono_raw: Optional[str]) -> str:
        """
        Limpia un número telefónico eliminando espacios, guiones y caracteres especiales.
        Si es un celular colombiano de 10 dígitos (ej. 3151234567), le antepone el prefijo '57'.
        """
        if not telefono_raw:
            return ""

        solo_digitos = re.sub(r'\D', '', str(telefono_raw))

        # Si tiene 10 dígitos (ej: 3151234567), anteponer 57
        if len(solo_digitos) == 10 and solo_digitos.startswith('3'):
            return f"{cls.CODIGO_PAIS_COLOMBIA}{solo_digitos}"

        # Si tiene 12 dígitos y ya empieza con 57
        if len(solo_digitos) == 12 and solo_digitos.startswith('57'):
            return solo_digitos

        return solo_digitos

    @classmethod
    def construir_mensaje_recordatorio(
        cls, 
        nombre_empresario: str, 
        empresa: str, 
        descripcion_tarea: str, 
        fecha_limite: Optional[str] = "la próxima sesión"
    ) -> str:
        """
        Construye el texto del recordatorio siguiendo el tono empático,
        cercano y motivador de la Fundación WWB Colombia.
        """
        nombre_corto = nombre_empresario.split()[0].title() if nombre_empresario else "Empresario"
        negocio = empresa.title() if empresa else "su negocio"

        return (
            f"¡Hola {nombre_corto}! Te saluda tu consultor de la Fundación WWB Colombia. 👋\n\n"
            f"Te comparto el compromiso acordado en nuestra asesoría para *{negocio}*:\n"
            f"📌 *{descripcion_tarea}*\n\n"
            f"📅 *Meta:* Tenerlo listo para {fecha_limite}.\n\n"
            f"¡Muchos éxitos y nos vemos pronto para revisar tus avances! 🚀"
        )

    @classmethod
    def generar_enlace_wa(cls, telefono: str, mensaje: str) -> str:
        """
        Genera la URL final compatible con WhatsApp Web y App Móvil:
        https://wa.me/{telefono}?text={mensaje_url_encoded}
        """
        telefono_limpio = cls.normalizar_telefono(telefono)
        mensaje_encoded = urllib.parse.quote(mensaje)
        
        if telefono_limpio:
            return f"https://wa.me/{telefono_limpio}?text={mensaje_encoded}"
        return f"https://wa.me/?text={mensaje_encoded}"

whatsapp_service = WhatsAppService()
