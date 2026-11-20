// src/components/layout/Sidebar.jsx
import React from 'react';
import logoWWB from '../../assets/logo_fundacion_wwb_colombia.png';

export default function Sidebar({ seccionActiva, onNavigate }) {
  const menuItems = [
    { id: 'panel', label: '📊 Panel de Control', disabled: true },
    { id: 'empresarios', label: '👥 Empresarios', disabled: false },
    { id: 'sesiones', label: '📅 Sesiones de Asesoría', disabled: true },
    { id: 'asistente', label: '✨ Asistente IA', disabled: true },
    { id: 'reportes', label: '📈 Reportes', disabled: true },
    { id: 'configuracion', label: '⚙️ Configuración', disabled: true },
  ];

  return (
    <aside className="sidebar-wwb p-3 text-white d-flex flex-column">
      
      {/* BRANDING: LOGO OFICIAL FUNDACIÓN WWB COLOMBIA */}
      <div className="sidebar-brand-container">
        <img 
          src={logoWWB} 
          alt="Fundación WWB Colombia" 
          className="sidebar-logo mb-1" 
        />
      </div>

      {/* PERFIL DEL CONSULTOR */}
      <div className="p-2 mb-3 rounded bg-white bg-opacity-10 d-flex align-items-center gap-2">
        <div className="rounded-circle bg-light text-dark d-flex align-items-center justify-content-center fw-bold" style={{ width: '32px', height: '32px', fontSize: '0.85rem' }}>
          CG
        </div>
        <div className="text-truncate">
          <div className="small fw-bold lh-1">Carlos Gómez</div>
          <small className="opacity-75" style={{ fontSize: '0.7rem' }}>Consultor Senior</small>
        </div>
      </div>

      {/* MENÚ DE NAVEGACIÓN SPA */}
      <ul className="nav nav-pills flex-column mb-auto gap-1">
        {menuItems.map((item) => (
          <li key={item.id} className="nav-item">
            <button
              onClick={() => !item.disabled && onNavigate(item.id)}
              className={`nav-link w-100 text-start text-white border-0 d-flex justify-content-between align-items-center ${
                seccionActiva === item.id ? 'fw-bold' : 'opacity-75'
              }`}
              style={{
                backgroundColor: seccionActiva === item.id ? 'var(--wwb-azul-hover)' : 'transparent',
                cursor: item.disabled ? 'not-allowed' : 'pointer'
              }}
            >
              <span>{item.label}</span>
              {item.disabled && (
                <span className="badge bg-secondary opacity-50" style={{ fontSize: '0.55rem' }}>
                  Próximamente
                </span>
              )}
            </button>
          </li>
        ))}
      </ul>

      {/* BOTÓN / BANNER DE RECOMENDACIONES IA */}
      <div className="pt-3 border-top border-white border-opacity-10">
        <div className="p-2 rounded text-center fw-bold text-dark" style={{ backgroundColor: 'var(--wwb-amarillo)', fontSize: '0.75rem' }}>
          💡 RECOMENDACIONES IA
        </div>
      </div>
    </aside>
  );
}