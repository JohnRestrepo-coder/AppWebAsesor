import React from 'react';

export default function QuickPrompts({ onSelectPrompt, disabled = false }) {
  const prompts = [
    { 
      label: '📊 Analizar ventas', 
      texto: 'Analizar las ventas, precios y canales de captación del empresario utilizando su expediente.', 
      tipo: 'ventas' 
    },
    { 
      label: '💰 Costos y Finanzas', 
      texto: 'Revisar la estructura de costos, punto de equilibrio y separación de finanzas del negocio vs hogar.', 
      tipo: 'costos' 
    },
    { 
      label: '🎯 Plan de acción (7 días)', 
      texto: 'Generar un plan de acción a 7 días con compromisos claros y medibles para la próxima sesión.', 
      tipo: 'plan_accion' 
    },
    { 
      label: '⚠️ Detectar riesgos', 
      texto: 'Identificar riesgos prioritarios en clientes, liquidez, proveedores y operación del negocio.', 
      tipo: 'riesgos' 
    }
  ];

  return (
    <div className="d-flex gap-2 overflow-auto pb-2 mb-2">
      {prompts.map((p, index) => (
        <button
          key={index}
          className="btn btn-outline-secondary btn-sm text-nowrap rounded-pill px-3 shadow-none"
          style={{ fontSize: '0.75rem', borderColor: '#dee2e6' }}
          disabled={disabled}
          onClick={() => onSelectPrompt(p.texto, p.tipo)}
          title={p.texto}
        >
          {p.label}
        </button>
      ))}
    </div>
  );
}
