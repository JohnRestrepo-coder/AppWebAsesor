// src/App.jsx
import React, { useState } from 'react';
import React, { useEffect, useState } from 'react';
import { obtenerEmpresarios } from './services/empresarioService';

function App() {
  const [empresarios, setEmpresarios] = useState([]);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    obtenerEmpresarios()
      .then((data) => {
        console.log('✅ Datos de empresarios cargados en React:', data);
        setEmpresarios(data);
        setCargando(false);
      })
      .catch((err) => console.error('❌ Error en React:', err));
  }, []);

  if (cargando) return <div className="p-5 text-center">Cargando base de datos de la Fundación WWB...</div>;

  return (
    <div className="p-4">
      <h2>Empresarios Cargados: {empresarios.length}</h2>
      <ul>
        {empresarios.map((emp) => (
          <li key={emp.id}>
            <strong>{emp.nombre}</strong> - CC: {emp.cedula} | Bitácora: {emp.tiene_bitacora ? '✅ Disponible' : '❌ No encontrada'}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;

// Datos de prueba para el desarrollo visual de la UI
const EMPRESARIOS_PRUEBA = [
  { id: "80442045", nombre: "RAUL HERNAN ORTIZ BELTRAN", archivo: "Bitacora 80442045 RAUL HERNAN ORTIZ BELTRAN.xlsx" },
  { id: "29740252", nombre: "MARIA ISABEL YEPES ASCENSIO", archivo: "Bitacora 29740252 MARIA ISABEL YEPES ASCENSIO.xlsx" },
  { id: "1007706965", nombre: "STEFANNY BERNAL BENAVIDES", archivo: "Bitacora 1007706965 STEFANNY BERNAL BENAVIDES.xlsx" }
];

export default function App() {
  const [empresarioActivo, setEmpresarioActivo] = useState(EMPRESARIOS_PRUEBA[1]);
  const [busqueda, setBusqueda] = useState('');
  const [mensaje, setMensaje] = useState('');
  const [chat, setChat] = useState([
    { rol: 'ia', texto: 'Hola John. He cargado el contexto de la bitácora de María Isabel. ¿En qué área de consultoría deseas enfocarte hoy?' }
  ]);

  const azulWWB = '#1D327D';
  const amarilloWWB = '#F0AD15';

  const handleEnviar = (e) => {
    e.preventDefault();
    if (!mensaje.trim()) return;

    const nuevoChat = [...chat, { rol: 'user', texto: mensaje }];
    setChat(nuevoChat);
    setMensaje('');

    // Simulación de respuesta mientras conectamos FastAPI
    setTimeout(() => {
      setChat([...nuevoChat, { 
        rol: 'ia', 
        texto: `Análisis para ${empresarioActivo.nombre}: Basado en la bitácora individual, se recomienda revisar el margen de contribución en la pestaña de costos.` 
      }]);
    }, 600);
  };

  return (
    <div className="d-flex w-100" style={{ height: '100vh', overflow: 'hidden', backgroundColor: '#f4f6f9' }}>
      
      {/* 1. SIDEBAR / NAVEGACIÓN LATERAL */}
      <aside className="d-flex flex-column p-3 text-white shadow" style={{ width: '280px', backgroundColor: azulWWB }}>
        <div className="mb-4 text-center border-bottom border-white border-opacity-10 pb-3">
          <h4 className="fw-bold mb-0" style={{ color: amarilloWWB, letterSpacing: '1px' }}>
            fundación <span className="text-white">wwb</span>
          </h4>
          <small className="text-uppercase opacity-75" style={{ fontSize: '0.65rem' }}>Colombia</small>
        </div>

        <ul className="nav nav-pills flex-column mb-auto gap-2">
          <li className="nav-item">
            <button className="nav-link w-100 text-start text-white opacity-50 border-0" disabled>
              📊 Panel de Control <span className="badge bg-secondary float-end" style={{ fontSize: '0.55rem' }}>Próximamente</span>
            </button>
          </li>
          <li className="nav-item">
            <button className="nav-link w-100 text-start text-white active fw-bold border-0" style={{ backgroundColor: '#2b479d' }}>
              👥 Empresarios
            </button>
          </li>
          <li className="nav-item">
            <button className="nav-link w-100 text-start text-white opacity-50 border-0" disabled>
              📅 Sesiones <span className="badge bg-secondary float-end" style={{ fontSize: '0.55rem' }}>Próximamente</span>
            </button>
          </li>
        </ul>

        <div className="mt-auto pt-3 border-top border-white border-opacity-10">
          <div className="p-2 rounded text-center fw-bold text-dark" style={{ backgroundColor: amarilloWWB, fontSize: '0.75rem' }}>
            💡 RECOMENDACIONES IA
          </div>
        </div>
      </aside>

      {/* 2. CONTENEDOR PRINCIPAL */}
      <div className="d-flex flex-column flex-grow-1" style={{ overflow: 'hidden' }}>
        
        {/* HEADER / BUSCADOR */}
        <header className="bg-white border-bottom px-4 py-3 d-flex justify-content-between align-items-center shadow-sm">
          <div className="w-50">
            <input 
              type="text" 
              className="form-control bg-light border-0 rounded-pill px-3"
              placeholder="🔍 Buscar empresario por nombre o cédula..." 
              value={busqueda}
              onChange={(e) => setBusqueda(e.target.value)}
            />
          </div>
          <span className="badge bg-success bg-opacity-10 text-success border border-success px-3 py-2">
            ● Google Drive Conectado
          </span>
        </header>

        {/* WORKSPACE / TARJETAS */}
        <main className="flex-grow-1 p-4" style={{ overflowY: 'auto' }}>
          <div className="mb-3">
            <h4 className="fw-bold mb-1" style={{ color: azulWWB }}>
              Análisis IA y Recomendaciones para: {empresarioActivo.nombre}
            </h4>
            <small className="text-muted">Cédula: {empresarioActivo.id} | Archivo: <code>{empresarioActivo.archivo}</code></small>
          </div>

          <div className="row g-3">
            
            {/* COLUMNA IZQUIERDA: INFORMACIÓN DEL EMPRESARIO */}
            <div className="col-lg-4 d-flex flex-column gap-3">
              
              <div className="card border-0 shadow-sm p-3">
                <span className="badge text-dark mb-2 w-auto align-self-start" style={{ backgroundColor: amarilloWWB }}>
                  Empresario Activo
                </span>
                <h5 className="fw-bold mb-1" style={{ color: azulWWB }}>{empresarioActivo.nombre}</h5>
                <small className="text-muted">Microempresa Registrada</small>
              </div>

              <div className="card border-0 shadow-sm p-3">
                <h6 className="fw-bold mb-2" style={{ color: azulWWB }}>📋 Diagnóstico de Bitácora</h6>
                <ul className="list-unstyled small mb-0 d-flex flex-column gap-1">
                  <li className="text-success">✔ Estructura de costos inicial registrada.</li>
                  <li className="text-warning">⚠ Mezcla de finanzas personales.</li>
                  <li className="text-danger">✖ Sin canal digital formal.</li>
                </ul>
              </div>

              <div className="card border-0 shadow-sm p-3">
                <h6 className="fw-bold mb-2" style={{ color: azulWWB }}>⚠️ Problemáticas Clave</h6>
                <div className="d-flex flex-wrap gap-1">
                  <span className="badge bg-light text-dark border">Ventas Digitales</span>
                  <span className="badge bg-light text-dark border">Costos</span>
                </div>
              </div>

            </div>

            {/* COLUMNA DERECHA: ASISTENTE INTELIGENTE */}
            <div className="col-lg-8">
              <div className="card border-0 shadow-sm h-100 d-flex flex-column">
                
                <div className="card-header bg-white py-3 border-bottom d-flex justify-content-between align-items-center">
                  <div>
                    <h6 className="fw-bold mb-0" style={{ color: azulWWB }}>✨ Asistente Inteligente de Consultoría</h6>
                    <small className="text-muted" style={{ fontSize: '0.7rem' }}>
                      Impulsado por Gemini · Contexto del empresario cargado automáticamente.
                    </small>
                  </div>
                  <span className="badge bg-primary bg-opacity-10 text-primary">Gemini 2.5</span>
                </div>

                <div className="card-body bg-light p-3 flex-grow-1 overflow-auto" style={{ maxHeight: '380px' }}>
                  {chat.map((m, i) => (
                    <div 
                      key={i} 
                      className={`p-3 rounded mb-2 shadow-sm ${m.rol === 'user' ? 'bg-primary text-white ms-auto' : 'bg-white text-dark border-start border-4'}`}
                      style={{ maxWidth: '85%', borderLeftColor: m.rol === 'ia' ? amarilloWWB : 'transparent', fontSize: '0.85rem' }}
                    >
                      {m.texto}
                    </div>
                  ))}
                </div>

                <div className="card-footer bg-white border-0 p-3">
                  <div className="d-flex gap-1 overflow-auto pb-2 mb-2">
                    <button onClick={() => setMensaje('Analizar ventas del empresario')} className="btn btn-outline-secondary btn-sm text-nowrap rounded-pill">📊 Analizar ventas</button>
                    <button onClick={() => setMensaje('Generar plan de acción')} className="btn btn-outline-secondary btn-sm text-nowrap rounded-pill">🎯 Generar plan de acción</button>
                    <button onClick={() => setMensaje('Encontrar riesgos financieros')} className="btn btn-outline-secondary btn-sm text-nowrap rounded-pill">⚠️ Encontrar riesgos</button>
                  </div>

                  <form onSubmit={handleEnviar} className="input-group">
                    <input 
                      type="text" 
                      className="form-control" 
                      placeholder="Escriba su consulta específica sobre el empresario..." 
                      value={mensaje}
                      onChange={(e) => setMensaje(e.target.value)}
                    />
                    <button className="btn text-white px-4" type="submit" style={{ backgroundColor: azulWWB }}>
                      Enviar
                    </button>
                  </form>
                </div>

              </div>
            </div>

          </div>
        </main>

      </div>
    </div>
  );
}