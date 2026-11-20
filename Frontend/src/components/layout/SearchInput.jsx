import React from 'react';

export default function SearchInput({ onSearch }) {
  return (
    <div className="input-group">
      <input
        type="search"
        className="form-control bg-light border-0 rounded-pill px-3"
        placeholder="🔍 Buscar empresario por nombre o cédula..."
        onChange={(e) => onSearch && onSearch(e.target.value)}
        style={{ fontSize: '0.875rem' }}
      />
    </div>
  );
}