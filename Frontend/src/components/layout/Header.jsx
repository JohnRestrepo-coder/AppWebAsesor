import React from 'react';
import SearchInput from './SearchInput';

export default function Header({ 
  onSearch, 
  driveStatus = 'connected', 
  ultimaSync, 
  onSincronizar, 
  sincronizando = false 
}) {
  const getBadgeConfig = () => {
    switch (driveStatus) {
      case 'connected':
        return {
          clase: 'bg-success bg-opacity-10 text-success border border-success',
          texto: '● Google Drive Conectado',
          titulo: `Sincronizado: ${ultimaSync || 'Reciente'}`
        };
      case 'api_disabled':
        return {
          clase: 'bg-warning bg-opacity-10 text-dark border border-warning',
          texto: '⚠ API Drive por Habilitar',
          titulo: 'Habilitar Google Drive API en Google Cloud Console'
        };
      default:
        return {
          clase: 'bg-secondary bg-opacity-10 text-secondary border border-secondary',
          texto: '○ Modo Contingencia Local',
          titulo: 'Operando con base de datos local'
        };
    }
  };

  const badge = getBadgeConfig();

  return (
    <header className="bg-white border-bottom px-4 py-2 d-flex align-items-center justify-content-between shadow-sm" style={{ height: '60px' }}>
      <div className="w-50">
        <SearchInput onSearch={onSearch} />
      </div>

      <div className="d-flex align-items-center gap-3">
        {/* Botón de Sincronización Manual */}
        <button
          onClick={onSincronizar}
          disabled={sincronizando}
          className="btn btn-sm btn-outline-primary d-flex align-items-center gap-1 rounded-pill px-3"
          title="Consultar novedades en Google Drive"
          style={{ fontSize: '0.75rem' }}
        >
          {sincronizando ? (
            <>
              <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true" />
              <span>Sincronizando...</span>
            </>
          ) : (
            <>
              <span>🔄</span>
              <span>Sincronizar Drive</span>
            </>
          )}
        </button>

        {/* Badge de Estado */}
        <span 
          className={`badge ${badge.clase} px-2 py-1`} 
          style={{ fontSize: '0.75rem' }}
          title={badge.titulo}
        >
          {badge.texto}
        </span>
      </div>
    </header>
  );
}
