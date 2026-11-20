import React, { useState } from 'react';
import QuickPrompts from './QuickPrompts';
import { consultarIA } from '../../services/empresarioService';

export default function ChatPanel({ empresario }) {
  const [pregunta, setPregunta] = useState('');
  const [cargando, setCargando] = useState(false);
  const [historial, setHistorial] = useState([
    {
      rol: 'ia',
      texto: `¡Hola! Soy el Asistente Inteligente de Consultoría de la Fundación WWB Colombia.\n\nHe cargado el contexto del expediente de **${empresario?.nombre || 'empresario'}**. ¿En qué área de la asesoría deseas enfocarte hoy?`
    }
  ]);

  const handleSend = async (e) => {
    e?.preventDefault();
    if (!pregunta.trim() || cargando) return;

    const textoPregunta = pregunta;
    setHistorial(prev => [...prev, { rol: 'consultor', texto: textoPregunta }]);
    setPregunta('');
    setCargando(true);

    try {
      const data = await consultarIA(empresario?.id || empresario?.cedula || '1', textoPregunta);
      setHistorial(prev => [
        ...prev,
        {
          rol: 'ia',
          texto: data.respuesta || "Respuesta generada por el asistente."
        }
      ]);
    } catch (err) {
      setHistorial(prev => [
        ...prev,
        {
          rol: 'ia',
          texto: `⚠️ Error al procesar la consulta: ${err.message}`
        }
      ]);
    } finally {
      setCargando(false);
    }
  };

  const handleQuickPrompt = (promptText) => {
    setPregunta(promptText);
  };

  return (
    <div className="card border-0 shadow-sm h-100 d-flex flex-column">
      {/* Header Chat */}
      <div className="card-header bg-white py-3 border-bottom d-flex justify-content-between align-items-center">
        <div>
          <h6 className="fw-bold mb-0" style={{ color: 'var(--wwb-azul)' }}>
            ✨ Asistente Inteligente de Consultoría
          </h6>
          <small className="text-muted" style={{ fontSize: '0.7rem' }}>
            Fundación WWB Colombia · Contexto del empresario activo
          </small>
        </div>
        <span className="badge bg-primary bg-opacity-10 text-primary">Gemini AI</span>
      </div>

      {/* Historial */}
      <div className="card-body bg-light p-3 flex-grow-1 overflow-auto" style={{ minHeight: '340px', maxHeight: '420px' }}>
        {historial.map((msg, i) => (
          <div
            key={i}
            className={`p-3 rounded mb-3 shadow-sm ${
              msg.rol === 'consultor'
                ? 'bg-primary text-white ms-auto'
                : 'bg-white text-dark border-start border-4'
            }`}
            style={{
              maxWidth: '85%',
              borderLeftColor: msg.rol === 'ia' ? 'var(--wwb-amarillo)' : 'transparent',
              whiteSpace: 'pre-line',
              fontSize: '0.85rem'
            }}
          >
            {msg.texto}
          </div>
        ))}
        {cargando && (
          <div className="p-3 bg-white rounded border-start border-4 border-warning shadow-sm small text-muted" style={{ maxWidth: '60%' }}>
            <span className="spinner-border spinner-border-sm me-2 text-warning" role="status" />
            Gemini está analizando la bitácora...
          </div>
        )}
      </div>

      {/* Footer Controles */}
      <div className="card-footer bg-white border-0 p-3">
        <QuickPrompts onSelectPrompt={handleQuickPrompt} />
        <form onSubmit={handleSend} className="input-group">
          <input
            type="text"
            className="form-control"
            placeholder="Escriba su consulta específica sobre el empresario..."
            value={pregunta}
            onChange={(e) => setPregunta(e.target.value)}
            disabled={cargando}
            style={{ fontSize: '0.875rem' }}
          />
          <button 
            className="btn text-white px-4" 
            type="submit" 
            disabled={cargando || !pregunta.trim()}
            style={{ backgroundColor: 'var(--wwb-azul)' }}
          >
            {cargando ? 'Consultando...' : 'Enviar'}
          </button>
        </form>
      </div>
    </div>
  );
}
