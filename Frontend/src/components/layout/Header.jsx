import React from 'react';
import SearchInput from '../ui/SearchInput';

export default function Header({ onSearch }) {
  return (
    <header className="bg-white border-bottom px-4 py-2 d-flex align-items-center justify-content-between shadow-sm" style={{ height: '60px' }}>
      <div className="w-50">
        <SearchInput onSearch={onSearch} />
      </div>
      <div className="d-flex align-items-center gap-3">
        <span className="badge bg-success bg-opacity-10 text-success border border-success px-2 py-1" style={{ fontSize: '0.75rem' }}>
          ● Google Drive Conectado
        </span>
      </div>
    </header>
  );
}