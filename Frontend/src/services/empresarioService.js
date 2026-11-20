// src/services/empresarioService.js
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export const obtenerEmpresarios = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/empresarios`);
    return response.data;
  } catch (error) {
    console.error('Error al conectar con la API de Empresarios:', error);
    throw error;
  }
};
