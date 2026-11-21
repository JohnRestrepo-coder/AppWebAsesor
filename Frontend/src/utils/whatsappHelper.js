/**
 * Utilidades para la generación y apertura segura de enlaces wa.me
 * para la Fundación WWB Colombia.
 */

export const normalizarTelefono = (telefonoRaw) => {
  if (!telefonoRaw) return '';
  const soloDigitos = String(telefonoRaw).replace(/\D/g, '');

  // Si tiene 10 dígitos y empieza por 3 (celular Colombia)
  if (soloDigitos.length === 10 && soloDigitos.startsWith('3')) {
    return `57${soloDigitos}`;
  }

  // Si ya tiene 12 dígitos y empieza por 57
  if (soloDigitos.length === 12 && soloDigitos.startsWith('57')) {
    return soloDigitos;
  }

  return soloDigitos;
};

export const construirMensajeWWB = (nombreEmpresario, empresa, descripcionTarea) => {
  const nombre = nombreEmpresario ? nombreEmpresario.split(' ')[0] : 'Empresario';
  const negocio = empresa || 'su negocio';

  return `¡Hola ${nombre}! Te saluda tu consultor de la Fundación WWB Colombia. 👋\n\nTe comparto el compromiso acordado en nuestra asesoría para *${negocio}*:\n📌 *${descripcionTarea}*\n\n📅 *Meta:* Tenerlo listo para nuestra próxima sesión.\n\n¡Muchos éxitos y nos vemos pronto! 🚀`;
};

export const generarEnlaceWhatsApp = (telefono, mensaje) => {
  const telLimpio = normalizarTelefono(telefono);
  const textoCodificado = encodeURIComponent(mensaje);
  
  if (telLimpio) {
    return `https://wa.me/${telLimpio}?text=${textoCodificado}`;
  }
  return `https://wa.me/?text=${textoCodificado}`;
};

export const abrirWhatsApp = (enlace) => {
  if (!enlace) return;
  window.open(enlace, '_blank', 'noopener,noreferrer');
};
