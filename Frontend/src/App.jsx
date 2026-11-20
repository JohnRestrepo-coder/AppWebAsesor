import React, { useState, useEffect, useMemo } from 'react';
import Sidebar from './components/layout/Sidebar';
import Header from './components/layout/Header';
import EmpresarioCard from './components/empresario/EmpresarioCard';
import DiagnosticoCard from './components/empresario/DiagnosticoCard';
import ProblematicasCard from './components/empresario/ProblematicasCard';
import ChatPanel from './components/ia/ChatPanel';
import { obtenerEmpresarios } from './services/empresarioService';

export default function App() {
  const [empresarios, setEmpresarios] = useState([]);
  const [empresarioActivo, setEmpresarioActivo] = useState(null);
  const [busqueda, setBusqueda] = useState('');
  const [seccionActiva, setSeccionActiva] = useState('empresarios');
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    let montado = true;
    obtenerEmpresarios()
      .then((data) => {
        if (montado && data && data.length > 0) {
          setEmpresarios(data);
          setEmpresarioActivo(data[0]);
        }
      })
      .catch((err) => {
        console.error('Error al cargar empresarios:', err);
      })
      .finally(() => {
        if (montado) setCargando(false);
      });

    return () => {
      montado = false;
    };
  }, []);

  const empresariosFiltrados = useMemo(() => {
    if (!busqueda.trim()) return empresarios;
    const termino = busqueda.toLowerCase().trim();
    return empresarios.filter((e) =>
      (e.nombre && e.nombre.toLowerCase().includes(termino)) ||
      (e.cedula && e.cedula.includes(termino))
    );
  }, [empresarios, busqueda]);

  const seleccionarEmpresario = (emp) => {
    setEmpresarioActivo(emp);
  };

  return (
    <div className="d-flex w-100" style={{ height: '100vh', overflow: 'hidden', backgroundColor: '#f4f6f9' }}>
      
      {/* 1. NAVEGACIÓN LATERAL (SIDEBAR) */}
      <Sidebar seccionActiva={seccionActiva} onNavigate={setSeccionActiva} />

      {/* 2. CONTENEDOR PRINCIPAL */}
      <div className="d-flex flex-column flex-grow-1" style={{ overflow: 'hidden' }}>
        
        {/* HEADER CON BÚSQUEDA */}
        <Header onSearch={setBusqueda} driveConectado={true} />

        {/* WORKSPACE / ÁREA DE TRABAJO */}
        <main className="flex-grow-1 p-4" style={{ overflowY: 'auto' }}>
          
          {cargando ? (
            <div className="d-flex justify-content-center align-items-center h-75">
              <div className="text-center">
                <div className="spinner-border text-primary mb-2" role="status" />
                <div className="text-muted small">Cargando base de datos de la Fundación WWB...</div>
              </div>
            </div>
          ) : (
            <>
              {/* SELECTOR RÁPIDO SI HAY BÚSQUEDA O MÚLTIPLES EMPRESARIOS */}
              {busqueda && (
                <div className="card border-0 shadow-sm p-2 mb-3 bg-white">
                  <div className="small fw-bold text-muted mb-2 px-2">
                    Resultados encontrados ({empresariosFiltrados.length}):
                  </div>
                  <div className="d-flex gap-2 flex-wrap">
                    {empresariosFiltrados.map((emp) => (
                      <button
                        key={emp.id || emp.cedula}
                        onClick={() => seleccionarEmpresario(emp)}
                        className={`btn btn-sm rounded-pill text-truncate ${
                          empresarioActivo?.id === emp.id
                            ? 'btn-primary'
                            : 'btn-outline-secondary'
                        }`}
                        style={{ maxWidth: '240px' }}
                      >
                        {emp.nombre} {emp.tiene_bitacora ? '✅' : '📁'}
                      </button>
                    ))}
                    {empresariosFiltrados.length === 0 && (
                      <div className="small text-danger px-2">
                        No se encontró ningún empresario con el criterio ingresado.
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* ENCABEZADO DEL EXPEDIENTE ACTIVO */}
              {empresarioActivo && (
                <div className="d-flex justify-content-between align-items-center mb-3">
                  <div>
                    <h4 className="fw-bold mb-0" style={{ color: 'var(--wwb-azul)' }}>
                      Expediente: {empresarioActivo.nombre}
                    </h4>
                    <small className="text-muted">
                      Cédula: <strong>{empresarioActivo.cedula}</strong> · 
                      Bitácora: <code>{empresarioActivo.archivo_bitacora || 'Sin bitácora vinculada'}</code>
                    </small>
                  </div>
                  <div>
                    <span className={`badge ${empresarioActivo.tiene_bitacora ? 'bg-success' : 'bg-secondary'}`}>
                      {empresarioActivo.tiene_bitacora ? 'Bitácora Disponible' : 'Pendiente de Bitácora'}
                    </span>
                  </div>
                </div>
              )}

              {/* GRILLA DE TARJETAS Y ASISTENTE */}
              {empresarioActivo ? (
                <div className="row g-3">
                  {/* COLUMNA IZQUIERDA: TARJETAS DEL EMPRESARIO */}
                  <div className="col-lg-4 d-flex flex-column gap-3">
                    <EmpresarioCard 
                      empresario={{
                        ...empresarioActivo,
                        archivoOriginal: empresarioActivo.archivo_bitacora || 'No disponible',
                        negocio: empresarioActivo.empresa || 'Microempresa Registrada'
                      }} 
                    />
                    <DiagnosticoCard />
                    <ProblematicasCard />
                  </div>

                  {/* COLUMNA DERECHA: ASISTENTE INTELIGENTE IA */}
                  <div className="col-lg-8">
                    <ChatPanel empresario={empresarioActivo} />
                  </div>
                </div>
              ) : (
                <div className="alert alert-info">
                  No hay empresarios disponibles para mostrar.
                </div>
              )}
            </>
          )}

        </main>
      </div>
    </div>
  );
}
