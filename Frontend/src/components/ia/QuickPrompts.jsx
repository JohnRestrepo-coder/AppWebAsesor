import React from 'react';

export default function QuickPrompts({ onSelectPrompt }) {
  const prompts = [
    '📊 Analizar ventas',
    '📋 Preparar próxima asesoría',
    '🎯 Generar plan de acción',
    '⚠️ Encontrar riesgos',
    '📝 Resumir historial',
    '💡 Ideas de marketing'
  ];

  return (
    <div className="d-flex gap-2 overflow-auto pb-2 mb-2">
      {prompts.map((promptText, index) => (
        <button
          key={index}
          className="btn btn-outline-secondary btn-sm text-nowrap rounded-pill"
          style={{ fontSize: '0.75rem' }}
          onClick={() => onSelectPrompt(promptText)}
        >
          {promptText}
        </button>
      ))}
    </div>
  );
}