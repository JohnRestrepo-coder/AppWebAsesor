import React from 'react';

export default function ProblematicasCard() {
  return (
    <div className="wwb-card p-3">
      <h6 className="fw-bold mb-2" style={{ color: 'var(--wwb-azul)' }}>⚠️ Problemáticas Clave</h6>
      <div className="d-flex flex-wrap gap-1">
        <span className="badge bg-light text-dark border">Ventas Digitales</span>
        <span className="badge bg-light text-dark border">Cadena de Suministro</span>
        <span className="badge bg-light text-dark border">Gestión de Inventario</span>
      </div>
    </div>
  );
}