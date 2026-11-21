import React, { useState } from 'react';
import { useSpeechRecognition } from '../../hooks/useSpeechRecognition';
import { procesarMinutaVoz } from '../../services/empresarioService';
import { abrirWhatsApp, generarEnlaceWhatsApp, construirMensajeWWB } from '../../utils/whatsappHelper';

export default function MinutaVozModal({ empresario, isOpen, onClose }) {
  const {
    escuchando,
    transcripcion,
    setTranscripcion,
    error: errorVoz,
    soportado,
    alternarGrabacion,
    limpiarTranscripcion
  } = useSpeechRecognition();

  const [procesando, setProcesando] = useState(false);
  const [minutaResultado, setMinutaResultado] = useState(null);
  const [tareasConsultor, setTareasConsultor] = useState([]);
  const [tareasEmpresario, setTareasEmpresario] = useState([]);

  if (!isOpen) return null;

  const handleProcesar = async () => {
    if (!transcripcion.trim() || procesando) return;

    setProcesando(true);
    try {
      const data = await procesarMinutaVoz(
        empresario?.id || empresario?.cedula || '1',
        transcripcion
      );
      setMinutaResultado(data);
      setTareasConsultor(data.tareas_consultor || []);
      setTareasEmpresario(data.tareas_empresario || []);
    } catch (err) {
      console.error('Error al procesar minuta:', err);
    } finally {
      setProcesando(false);
    }
  };

  const toggleTareaConsultor = (id) => {
    setTareasConsultor(prev => prev.map(t => t.id === id ? { ...t, completada: !t.completada } : t));
  };

  const toggleTareaEmpresario = (id) => {
    setTareasEmpresario(prev => prev.map(t => t.id === id ? { ...t, completada: !t.completada } : t));
  };

  const handleEnviarWhatsApp = (tarea) => {
    const enlace = tarea.enlace_whatsapp || generarEnlaceWhatsApp(
      empresario?.telefono || '3150000000',
      construirMensajeWWB(empresario?.nombre, empresario?.empresa, tarea.descripcion)
    );
    abrirWhatsApp(enlace);
  };

  return (
    <div className="modal show d-block" tabIndex="-1" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1050 }}>
      <div className="modal-dialog modal-lg modal-dialog-scrollable">
        <div className="modal-content border-0 shadow-lg">
          
          {/* Header */}
          <div className="modal-header border-bottom py-3" style={{ backgroundColor: '#1D327D', color: '#fff' }}>
            <div>
              <h5 className="modal-title fw-bold mb-0">
                🎙️ Registro de Minuta de Asesoría por Voz
              </h5>
              <small className="opacity-75">
                Fundación WWB Colombia · Asesoría con: <strong>{empresario?.nombre}</strong> (Tel: {empresario?.telefono || 'Sin celular'})
              </small>
            </div>
            <button type="button" className="btn-close btn-close-white" onClick={onClose} aria-label="Cerrar" />
          </div>

          {/* Body */}
          <div className="modal-body p-4 bg-light">
            
            {!soportado && (
              <div className="alert alert-warning small py-2 mb-3">
                ⚠️ Tu navegador actual no tiene activada la Web Speech API nativa. Puedes escribir o pegar tus notas manualmente en el campo inferior.
              </div>
            )}

            {errorVoz && (
              <div className="alert alert-danger small py-2 mb-3">
                {errorVoz}
              </div>
            )}

            {/* SECCIÓN 1: CONTROL DE GRABACIÓN */}
            <div className="card border-0 shadow-sm p-3 mb-3 bg-white text-center">
              <div className="d-flex justify-content-center align-items-center gap-3">
                <button
                  type="button"
                  onClick={alternarGrabacion}
                  className={`btn rounded-pill px-4 py-2 fw-bold d-flex align-items-center gap-2 ${
                    escuchando ? 'btn-danger animate-pulse' : 'btn-primary'
                  }`}
                  style={{ backgroundColor: escuchando ? '#dc3545' : '#1D327D' }}
                >
                  <span style={{ fontSize: '1.2rem' }}>{escuchando ? '⏹️' : '🎙️'}</span>
                  <span>{escuchando ? 'Detener Grabación (Escuchando...)' : 'Iniciar Dictado de Voz'}</span>
                </button>

                {transcripcion && (
                  <button
                    type="button"
                    onClick={limpiarTranscripcion}
                    className="btn btn-outline-secondary btn-sm rounded-pill"
                    disabled={procesando || escuchando}
                  >
                    Borrar texto
                  </button>
                )}
              </div>

              {escuchando && (
                <div className="text-danger small mt-2 fw-bold">
                  ● Micrófono activo · Habla con claridad sobre lo acordado en la asesoría...
                </div>
              )}
            </div>

            {/* SECCIÓN 2: ÁREA DE TEXTO TRANSCRIBIDO / EDITABLE */}
            <div className="card border-0 shadow-sm p-3 mb-3 bg-white">
              <label className="form-label small fw-bold text-muted mb-1">
                Transcripción de la Sesión (puedes editar o complementar el texto):
              </label>
              <textarea
                className="form-control"
                rows={4}
                placeholder="Las notas dictadas aparecerán aquí automáticamente. También puedes escribir directamente..."
                value={transcripcion}
                onChange={(e) => setTranscripcion(e.target.value)}
                disabled={procesando}
                style={{ fontSize: '0.875rem' }}
              />

              <div className="d-flex justify-content-end mt-3">
                <button
                  type="button"
                  onClick={handleProcesar}
                  disabled={!transcripcion.trim() || procesando || escuchando}
                  className="btn text-white fw-bold px-4 rounded-pill d-flex align-items-center gap-2"
                  style={{ backgroundColor: '#F0AD15' }}
                >
                  {procesando ? (
                    <>
                      <span className="spinner-border spinner-border-sm" role="status" />
                      <span>Gemini está clasificando compromisos...</span>
                    </>
                  ) : (
                    <>
                      <span>⚡</span>
                      <span>Procesar Minuta con Gemini AI</span>
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* SECCIÓN 3: RESULTADOS CLASIFICADOS CON BOTONES WHATSAPP */}
            {minutaResultado && (
              <div className="card border-0 shadow-sm p-3 bg-white">
                
                {/* Resumen */}
                <div className="mb-3 p-3 rounded bg-light border-start border-4" style={{ borderLeftColor: '#1D327D' }}>
                  <h6 className="fw-bold mb-1" style={{ color: '#1D327D' }}>
                    📋 Resumen Ejecutivo de la Asesoría
                  </h6>
                  <p className="small mb-0 text-secondary">
                    {minutaResultado.resumen_sesion}
                  </p>
                </div>

                <div className="row g-3">
                  {/* Tareas del Consultor */}
                  <div className="col-md-6">
                    <div className="p-3 rounded border h-100 bg-white">
                      <div className="d-flex justify-content-between align-items-center mb-2">
                        <h6 className="fw-bold mb-0 text-primary small">
                          💼 Tareas del Consultor ({tareasConsultor.length})
                        </h6>
                        <span className="badge bg-primary bg-opacity-10 text-primary" style={{ fontSize: '0.65rem' }}>
                          Metodología
                        </span>
                      </div>
                      <div className="d-flex flex-column gap-2">
                        {tareasConsultor.map((tarea) => (
                          <div key={tarea.id} className="form-check small">
                            <input
                              className="form-check-input"
                              type="checkbox"
                              checked={tarea.completada}
                              onChange={() => toggleTareaConsultor(tarea.id)}
                              id={tarea.id}
                            />
                            <label 
                              className={`form-check-label ${tarea.completada ? 'text-decoration-line-through text-muted' : ''}`} 
                              htmlFor={tarea.id}
                            >
                              {tarea.descripcion}
                            </label>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Tareas del Microempresario con Botón WhatsApp */}
                  <div className="col-md-6">
                    <div className="p-3 rounded border h-100 bg-white">
                      <div className="d-flex justify-content-between align-items-center mb-2">
                        <h6 className="fw-bold mb-0 text-success small">
                          🎯 Tareas del Microempresario ({tareasEmpresario.length})
                        </h6>
                        <span className="badge bg-success bg-opacity-10 text-success" style={{ fontSize: '0.65rem' }}>
                          Acción 7 días
                        </span>
                      </div>
                      <div className="d-flex flex-column gap-2">
                        {tareasEmpresario.map((tarea) => (
                          <div key={tarea.id} className="d-flex align-items-start justify-content-between gap-2 p-2 rounded bg-light border">
                            <div className="form-check small flex-grow-1">
                              <input
                                className="form-check-input"
                                type="checkbox"
                                checked={tarea.completada}
                                onChange={() => toggleTareaEmpresario(tarea.id)}
                                id={tarea.id}
                              />
                              <label 
                                className={`form-check-label ${tarea.completada ? 'text-decoration-line-through text-muted' : ''}`} 
                                htmlFor={tarea.id}
                              >
                                {tarea.descripcion}
                              </label>
                            </div>
                            <button
                              type="button"
                              onClick={() => handleEnviarWhatsApp(tarea)}
                              className="btn btn-success btn-sm py-1 px-2 text-nowrap d-flex align-items-center gap-1 rounded-pill shadow-none"
                              style={{ fontSize: '0.68rem', backgroundColor: '#25D366', borderColor: '#25D366' }}
                              title="Enviar recordatorio gratuito por WhatsApp"
                            >
                              <span>💬</span>
                              <span>WhatsApp</span>
                            </button>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

              </div>
            )}

          </div>

          {/* Footer */}
          <div className="modal-footer bg-white py-2 border-top">
            <button type="button" className="btn btn-secondary btn-sm rounded-pill px-4" onClick={onClose}>
              Cerrar
            </button>
          </div>

        </div>
      </div>
    </div>
  );
}
