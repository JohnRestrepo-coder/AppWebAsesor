import React from 'react';

export default function DiagnosticoCard() {
  return (
    <div className="wwb-card p-3 mb-3">
      <h6 className="fw-bold mb-2" style={{ color: 'var(--wwb-azul)' }}>📋 Diagnóstico de Bitácora</h6>
      <ul className="list-unstyled small mb-0 d-flex flex-column gap-2">
        <li className="text-success">✔ Estructura de costos inicial registrada.</li>
        <li className="text-warning">⚠ Mezcla de finanzas personales y del negocio.</li>
        <li className="text-danger">✖ Sin canal digital formal de ventas.</li>
      </ul>
    </div>
  );
}