import axios from 'axios';

const API_BASE_URL = '/api';

export const EMPRESARIOS_MOCK = [
  { 
    id: "80442045", 
    cedula: "80442045", 
    nombre: "RAUL HERNAN ORTIZ BELTRAN", 
    empresa: "Confecciones Ortiz", 
    sector: "Textil y Moda",
    tiene_bitacora: true,
    archivo_bitacora: "Bitacora 80442045 RAUL HERNAN ORTIZ BELTRAN.xlsx" 
  },
  { 
    id: "29740252", 
    cedula: "29740252", 
    nombre: "MARIA ISABEL YEPES ASCENSIO", 
    empresa: "Pastelería Doña María", 
    sector: "Alimentos",
    tiene_bitacora: true,
    archivo_bitacora: "Bitacora 29740252 MARIA ISABEL YEPES ASCENSIO.xlsx" 
  },
  { 
    id: "1007706965", 
    cedula: "1007706965", 
    nombre: "STEFANNY BERNAL BENAVIDES", 
    empresa: "Distribuciones Bernal", 
    sector: "Comercio",
    tiene_bitacora: false,
    archivo_bitacora: null 
  }
];

export const obtenerEmpresarios = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/empresarios`, { timeout: 4000 });
    if (Array.isArray(response.data) && response.data.length > 0) {
      return response.data;
    }
    return EMPRESARIOS_MOCK;
  } catch (error) {
    console.warn('⚠️ Backend no disponible o en carga, usando datos de desarrollo:', error.message);
    return EMPRESARIOS_MOCK;
  }
};

export const consultarIA = async (empresarioId, pregunta) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/consulta-ia`, {
      empresario_id: String(empresarioId),
      pregunta: pregunta
    }, { timeout: 8000 });
    return response.data;
  } catch (error) {
    console.warn('⚠️ Error en endpoint IA, usando respuesta simulada:', error.message);
    return {
      respuesta: `🤖 [Asistente WWB - Modo Local]\n\nAnálisis para la consulta "${pregunta}":\nSe recomienda validar en la bitácora la separación de cuentas personales y del negocio, y definir una meta de ventas para la próxima semana.`,
      status: "mock"
    };
  }
};
