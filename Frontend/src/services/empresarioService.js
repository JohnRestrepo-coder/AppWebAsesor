import axios from 'axios';

const API_BASE_URL = '/api';

export const EMPRESARIOS_MOCK = [
  { 
    id: "80442045", 
    cedula: "80442045", 
    nombre: "RAÚL HERNÁN ORTIZ BELTRÁN", 
    empresa: "Muebles Ortiz", 
    sector: "Madera y Muebles",
    telefono: "3154567890",
    tiene_bitacora: true,
    archivo_bitacora: "Bitacora 80442045 RAUL HERNAN ORTIZ BELTRAN.xlsx" 
  },
  { 
    id: "29740252", 
    cedula: "29740252", 
    nombre: "MARÍA ISABEL YEPES ASCENSIO", 
    empresa: "Confecciones El Sol", 
    sector: "Textil y Confección",
    telefono: "3187654321",
    tiene_bitacora: true,
    archivo_bitacora: "Bitacora 29740252 MARIA ISABEL YEPES ASCENSIO.xlsx" 
  },
  { 
    id: "1007706965", 
    cedula: "1007706965", 
    nombre: "STEFANNY BERNAL BENAVIDES", 
    empresa: "Detalles Stefanny", 
    sector: "Artesanías y Regalos",
    telefono: "3123456789",
    tiene_bitacora: true,
    archivo_bitacora: "Bitacora 1007706965 STEFANNY BERNAL BENAVIDES.xlsx" 
  },
  { 
    id: "31880769", 
    cedula: "31880769", 
    nombre: "LUZ EUGENIA PÉREZ PEÑA", 
    empresa: "Comercializadora Pérez", 
    sector: "Comercio Minorista",
    telefono: "3169876543",
    tiene_bitacora: true,
    archivo_bitacora: "Bitacora 31880769 LUZ EUGENIA PEREZ PEÑA.xlsx" 
  },
  { 
    id: "1061777035", 
    cedula: "1061777035", 
    nombre: "ASTRID NATALIA ARANDA PATIÑO", 
    empresa: "Estética Natalia", 
    sector: "Servicios y Belleza",
    telefono: "3171122334",
    tiene_bitacora: true,
    archivo_bitacora: "Bitacora 1061777035 ASTRID NATALIA ARANDA PATIÑO.xlsx" 
  }
];

export const obtenerEmpresarios = async (force = false) => {
  try {
    const url = force ? `${API_BASE_URL}/empresarios?force=true` : `${API_BASE_URL}/empresarios`;
    const response = await axios.get(url, { timeout: 6000 });
    
    if (response.data && response.data.empresarios) {
      return response.data;
    }
    
    if (Array.isArray(response.data)) {
      return {
        drive_status: "connected",
        mensaje: "Conectado",
        ultima_sincronizacion: new Date().toLocaleTimeString(),
        total_empresarios: response.data.length,
        empresarios: response.data
      };
    }
    
    throw new Error("Formato de respuesta inesperado");
  } catch (error) {
    console.warn('⚠️ Usando datos de contingencia en frontend:', error.message);
    return {
      drive_status: "offline",
      mensaje: "Modo contingencia local",
      ultima_sincronizacion: new Date().toLocaleTimeString(),
      total_empresarios: EMPRESARIOS_MOCK.length,
      empresarios: EMPRESARIOS_MOCK
    };
  }
};

export const forzarSincronizacion = async () => {
  try {
    const response = await axios.post(`${API_BASE_URL}/empresarios/sincronizar`, {}, { timeout: 10000 });
    if (response.data && response.data.empresarios) {
      return response.data;
    }
    return await obtenerEmpresarios(true);
  } catch (error) {
    console.warn('⚠️ Error al forzar sincronización:', error.message);
    return await obtenerEmpresarios(false);
  }
};

export const obtenerEmpresarioPorId = async (id) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/empresarios/${id}`, { timeout: 4000 });
    return response.data;
  } catch (error) {
    const mock = EMPRESARIOS_MOCK.find(e => e.id === String(id) || e.cedula === String(id));
    return mock || null;
  }
};

export const consultarIA = async (empresarioId, pregunta, tipoAnalisis = "general") => {
  try {
    const response = await axios.post(`${API_BASE_URL}/consulta-ia`, {
      empresario_id: String(empresarioId),
      pregunta: pregunta,
      tipo_analisis: tipoAnalisis
    }, { timeout: 12000 });
    return response.data;
  } catch (error) {
    console.warn('⚠️ Error en endpoint IA, usando respuesta de contingencia:', error.message);
    return {
      respuesta: `### 📌 Diagnóstico Clave\nConsulta procesada en modo contingencia para el microempresario.\n\n### 💡 Recomendación Práctica\n1. Validar la separación de gastos personales del negocio.\n2. Establecer meta semanal de ventas para la siguiente sesión.\n\n### 🎯 Compromiso Sugerido\n* Traer el registro de ingresos y gastos de la semana.`,
      status: "mock",
      tipo_analisis: tipoAnalisis
    };
  }
};

export const procesarMinutaVoz = async (empresarioId, textoDictado) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/minuta-voz`, {
      empresario_id: String(empresarioId),
      texto_dictado: textoDictado
    }, { timeout: 15000 });
    return response.data;
  } catch (error) {
    console.warn('⚠️ Error al procesar minuta en backend, usando generador de contingencia con WhatsApp:', error.message);
    const mockEmpresario = EMPRESARIOS_MOCK.find(e => e.id === String(empresarioId)) || EMPRESARIOS_MOCK[0];
    const tel = mockEmpresario.telefono || "3154567890";

    const msg1 = encodeURIComponent(`¡Hola! Te saluda tu consultor de la Fundación WWB Colombia. 👋\n\nTe comparto tu compromiso acordado:\n📌 *Registrar diariamente todas las ventas y compras en el cuaderno de trabajo.*\n\n📅 *Meta:* Próxima sesión.\n\n¡Muchos éxitos! 🚀`);
    const msg2 = encodeURIComponent(`¡Hola! Te saluda tu consultor de la Fundación WWB Colombia. 👋\n\nTe comparto tu compromiso acordado:\n📌 *Separar físicamente el dinero de los gastos del hogar de las ventas del negocio.*\n\n📅 *Meta:* Próxima sesión.\n\n¡Muchos éxitos! 🚀`);

    return {
      empresario_id: String(empresarioId),
      nombre_empresario: mockEmpresario.nombre,
      telefono_empresario: tel,
      resumen_sesion: `Resumen de sesión: Se identificaron oportunidades clave para ordenar los registros y separar el dinero personal de las ventas del negocio.`,
      tareas_consultor: [
        { 
          id: "c-1", 
          descripcion: "Revisar la hoja de cálculo de costos en la bitácora antes de la próxima asesoría.", 
          responsable: "consultor", 
          completada: false, 
          fecha_limite: "En 7 días" 
        },
        { 
          id: "c-2", 
          descripcion: "Preparar formato de lista de difusión para clientes frecuentes.", 
          responsable: "consultor", 
          completada: false, 
          fecha_limite: "En 7 días" 
        }
      ],
      tareas_empresario: [
        { 
          id: "e-1", 
          descripcion: "Registrar diariamente todas las ventas y compras en el cuaderno de trabajo.", 
          responsable: "empresario", 
          completada: false, 
          fecha_limite: "Próxima sesión",
          enlace_whatsapp: `https://wa.me/57${tel}?text=${msg1}`
        },
        { 
          id: "e-2", 
          descripcion: "Separar físicamente el dinero de los gastos del hogar de las ventas del negocio.", 
          responsable: "empresario", 
          completada: false, 
          fecha_limite: "Próxima sesión",
          enlace_whatsapp: `https://wa.me/57${tel}?text=${msg2}`
        }
      ],
      status: "mock"
    };
  }
};
