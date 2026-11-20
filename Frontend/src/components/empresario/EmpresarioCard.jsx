
import React from 'react';

export default function EmpresarioCard({ empresario }) {
  if (!empresario) return null;

  return (
    <div className="wwb-card p-3 mb-3">
      <div className="d-flex justify-content-between align-items-start mb-2">
        <span className="badge text-dark" style={{ backgroundColor: 'var(--wwb-amarillo)', fontSize: '0.7rem' }}>
          Empresario Activo
        </span>
        <small className="text-muted" style={{ fontSize: '0.75rem' }}>CC: {empresario.cedula}</small>
      </div>
      <h5 className="fw-bold mb-1" style={{ color: 'var(--wwb-azul)' }}>{empresario.nombre}</h5>
      <p className="text-muted small mb-2">{empresario.negocio}</p>
      <hr className="my-2" />
      <div className="small text-secondary">
        <strong>Sector:</strong> {empresario.sector}
      </div>
      <div className="mt-2 p-2 bg-light rounded text-truncate border" style={{ fontSize: '0.7rem' }}>
        📁 <code>{empresario.archivoOriginal}</code>
      </div>
    </div>
  );
}