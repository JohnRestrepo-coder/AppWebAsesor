import React, { useState, useEffect, useRef } from 'react';
import QuickPrompts from './QuickPrompts';
import { consultarIA } from '../../services/empresarioService';

export default function ChatPanel({ empresario }) {
  const [pregunta, setPregunta] = useState('');
  const [cargando, setCargando] = useState(false);
  const [historial, setHistorial] = useState([]);
  const chatBottomRef = useRef(null);

  // Reiniciar bienvenida cuando cambia el empresario activo
  useEffect(() => {
    if (!empresario) return;

    setHistorial([
      {
        rol: 'ia',
        texto: `¡Hola! Soy el Asistente Inteligente de Consultoría de la Fundación WWB Colombia.\n\nHe cargado el expediente de **${empresario.nombre}** (${empresario.empresa || 'Microempresa Registrada'}).\n\n¿En qué área de la asesoría deseas enfocarte hoy? Puedes escribir una pregunta o usar los botones de análisis rápido abajo.`
      }
    ]);
  }, [empresario?.id, empresario?.cedula]);

  // Auto-scroll al final del chat
  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [historial, cargando]);

  const procesarConsulta = async (textoPregunta, tipo = "general") => {
    if (!textoPregunta.trim() || cargando) return;

    setHistorial(prev => [...prev, { rol: 'consultor', texto: textoPregunta }]);
    setPregunta('');
    setCargando(true);

    try {
      const data = await consultarIA(
        empresario?.id || empresario?.cedula || '1', 
        textoPregunta,
        tipo
      );

      setHistorial(prev => [
        ...prev,
        {
          rol: 'ia',
          texto: data.respuesta || "Respuesta generada por el asistente.",
          tipo_analisis: data.tipo_analisis
        }
      ]);
    } catch (err) {
      setHistorial(prev => [
        ...prev,
        {
          rol: 'ia',
          texto: `⚠️ Error al procesar la consulta con Gemini: ${err.message}`
        }
      ]);
    } finally {
      setCargando(false);
    }
  };

  const handleFormSubmit = (e) => {
    e?.preventDefault();
    procesarConsulta(pregunta, "general");
  };

  const handleQuickPromptSelect = (textoPrompt, tipoAnalisis) => {
    procesarConsulta(textoPrompt, tipoAnalisis);
  };

  return (
    <div className="card border-0 shadow-sm h-100 d-flex flex-column">
      {/* Header del Chat */}
      <div className="card-header bg-white py-3 border-bottom d-flex justify-content-between align-items-center">
        <div>
          <h6 className="fw-bold mb-0" style={{ color: 'var(--wwb-azul)' }}>
            ✨ Asistente Inteligente de Consultoría
          </h6>
          <small className="text-muted" style={{ fontSize: '0.7rem' }}>
            Metodología Fundación WWB · Contexto activo: {empresario?.nombre || 'Seleccionado'}
          </small>
        </div>
        <div className="d-flex align-items-center gap-2">
          <span className="badge bg-primary bg-opacity-10 text-primary">Gemini 1.5 Flash</span>
        </div>
      </div>

      {/* Historial de Mensajes */}
      <div 
        className="card-body bg-light p-3 flex-grow-1 overflow-auto" 
        style={{ minHeight: '340px', maxHeight: '430px' }}
      >
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
              fontSize: '0.875rem',
              lineHeight: '1.5'
            }}
          >
            {msg.texto}
          </div>
        ))}

        {cargando && (
          <div className="p-3 bg-white rounded border-start border-4 border-warning shadow-sm small text-muted" style={{ maxWidth: '65%' }}>
            <span className="spinner-border spinner-border-sm me-2 text-warning" role="status" />
            Gemini está analizando la bitácora de {empresario?.nombre}...
          </div>
        )}
        <div ref={chatBottomRef} />
      </div>

      {/* Footer con Quick Prompts y Formulario */}
      <div className="card-footer bg-white border-0 p-3">
        <QuickPrompts onSelectPrompt={handleQuickPromptSelect} disabled={cargando} />
        
        <form onSubmit={handleFormSubmit} className="input-group">
          <input
            type="text"
            className="form-control"
            placeholder="Escribe tu consulta estratégica sobre el empresario..."
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
