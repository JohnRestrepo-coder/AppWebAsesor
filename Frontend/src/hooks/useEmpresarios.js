import { useState, useEffect, useMemo, useCallback } from 'react';
import { obtenerEmpresarios, forzarSincronizacion } from '../services/empresarioService';

export function useEmpresarios() {
  const [empresarios, setEmpresarios] = useState([]);
  const [empresarioActivo, setEmpresarioActivo] = useState(null);
  const [busqueda, setBusqueda] = useState('');
  const [cargando, setCargando] = useState(true);
  const [sincronizando, setSincronizando] = useState(false);
  const [driveStatus, setDriveStatus] = useState('disconnected');
  const [mensajeStatus, setMensajeStatus] = useState('');
  const [ultimaSync, setUltimaSync] = useState('Nunca');

  // Carga inicial
  useEffect(() => {
    let montado = true;
    obtenerEmpresarios()
      .then((data) => {
        if (!montado) return;
        setEmpresarios(data.empresarios || []);
        setDriveStatus(data.drive_status || 'offline');
        setMensajeStatus(data.mensaje || '');
        setUltimaSync(data.ultima_sincronizacion || 'Ahora');
        if (data.empresarios && data.empresarios.length > 0) {
          setEmpresarioActivo(data.empresarios[0]);
        }
      })
      .catch((err) => {
        console.error('Error inicial en useEmpresarios:', err);
      })
      .finally(() => {
        if (montado) setCargando(false);
      });

    return () => {
      montado = false;
    };
  }, []);

  // Forzar sincronización con Google Drive
  const sincronizar = useCallback(async () => {
    setSincronizando(true);
    try {
      const data = await forzarSincronizacion();
      setEmpresarios(data.empresarios || []);
      setDriveStatus(data.drive_status || 'offline');
      setMensajeStatus(data.mensaje || '');
      setUltimaSync(data.ultima_sincronizacion || 'Ahora');
      if (data.empresarios && data.empresarios.length > 0) {
        // Preservar activo si existe en la nueva lista, o seleccionar el primero
        setEmpresarioActivo((prev) => {
          if (!prev) return data.empresarios[0];
          const existe = data.empresarios.find((e) => e.id === prev.id || e.cedula === prev.cedula);
          return existe || data.empresarios[0];
        });
      }
    } catch (err) {
      console.error('Error al sincronizar con Drive:', err);
    } finally {
      setSincronizando(false);
    }
  }, []);

  // Filtrado instantáneo en memoria
  const empresariosFiltrados = useMemo(() => {
    if (!busqueda.trim()) return empresarios;
    const termino = busqueda.toLowerCase().trim();
    return empresarios.filter((e) =>
      (e.nombre && e.nombre.toLowerCase().includes(termino)) ||
      (e.cedula && e.cedula.includes(termino)) ||
      (e.empresa && e.empresa.toLowerCase().includes(termino))
    );
  }, [empresarios, busqueda]);

  const seleccionarEmpresario = useCallback((emp) => {
    setEmpresarioActivo(emp);
  }, []);

  return {
    empresarios,
    empresarioActivo,
    empresariosFiltrados,
    cargando,
    sincronizando,
    driveStatus,
    mensajeStatus,
    ultimaSync,
    busqueda,
    setBusqueda,
    seleccionarEmpresario,
    sincronizar
  };
}
