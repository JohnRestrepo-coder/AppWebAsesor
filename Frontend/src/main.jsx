import React from 'react';
import ReactDOM from 'react-dom/client';

// 1. Estilos de Terceros (Bootstrap 5)
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

// 2. Estilos Globales Propios del Proyecto
import './styles/variables.css';
import './styles/global.css';

// 3. Orquestador Principal
import App from './App';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);