import React, { useState } from 'react';
import QuickPrompts from './QuickPrompts';

export default function ChatPanel({ empresario }) {
  const [pregunta, setPregunta] = useState('');
  const [historial, setHistorial] = useState([
    {
      rol: 'ia',
      texto: `Estrategias de Fidelización Recomendadas:\n\nBasado en la bitácora de ${empresario?.nombre || 'empresario'}, se recomienda implementar un programa de puntos simple y seguimiento post-venta vía WhatsApp para mejorar la retención de clientes.`
    }
  ]);

  const handleSend = (e) => {
    e?.preventDefault();
    if (!pregunta.trim()) return;

    setHistorial(prev => [...prev, { rol: 'consultor', texto: pregunta }]);
    const currentQ = pregunta;
    setPregunta('');

    // Respuesta simulada para desarrollo visual UI
    setTimeout(() => {
      setHistorial(prev => [
        ...prev,
        {
          rol: 'ia',
          texto: `🤖 [Asistente Inteligente de Consultoría]\n\nRespuesta contextualizada para **${empresario?.nombre}** sobre: "${currentQ}".\n\n1. Validar margen bruto en Excel.\n2. Establecer metas de venta semanal.`
        }
      ]);
    }, 800);
  };

  const handleQuickPrompt = (promptText) => {
    setPregunta(promptText);
  };

  return (
    <div className="wwb-card d-flex flex-column h-100">
      {/* Header Chat */}
      <div className="p-3 border-bottom d-flex justify-content-between align-items-center">
        <div>
          <h6 className="fw-bold mb-0" style={{ color: 'var(--wwb-azul)' }}>
            ✨ Asistente Inteligente de Consultoría
          </h6>
          <small className="text-muted" style={{ fontSize: '0.7rem' }}>
            Impulsado por Gemini · Contexto del empresario cargado automáticamente.
          </small>
        </div>
        <span className="badge bg-primary bg-opacity-10 text-primary">Gemini 2.5</span>
      </div>

      {/* Historial */}
      <div className="flex-grow-1 bg-light p-3 overflow-auto" style={{ minHeight: '300px', maxHeight: '450px' }}>
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
      </div>

      {/* Footer Controles */}
      <div className="p-3 border-top bg-white">
        <QuickPrompts onSelectPrompt={handleQuickPrompt} />
        <form onSubmit={handleSend} className="input-group">
          <input
            type="text"
            className="form-control"
            placeholder="Escriba su consulta específica sobre el empresario..."
            value={pregunta}
            onChange={(e) => setPregunta(e.target.value)}
            style={{ fontSize: '0.875rem' }}
          />
          <button className="btn text-white" type="submit" style={{ backgroundColor: 'var(--wwb-azul)' }}>
            Enviar
          </button>
        </form>
      </div>
    </div>
  );
}