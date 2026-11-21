import { useState, useEffect, useRef, useCallback } from 'react';

export function useSpeechRecognition() {
  const [escuchando, setEscuchando] = useState(false);
  const [transcripcion, setTranscripcion] = useState('');
  const [error, setError] = useState(null);
  const [soportado, setSoportado] = useState(true);
  const recognitionRef = useRef(null);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setSoportado(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = 'es-CO';

    recognition.onresult = (event) => {
      let textoAcumulado = '';
      for (let i = 0; i < event.results.length; i++) {
        textoAcumulado += event.results[i][0].transcript + ' ';
      }
      setTranscripcion(textoAcumulado.trim());
    };

    recognition.onerror = (event) => {
      console.warn('Speech recognition event error:', event.error);
      if (event.error !== 'no-speech') {
        setError(`Error del micrófono: ${event.error}`);
      }
      setEscuchando(false);
    };

    recognition.onend = () => {
      setEscuchando(false);
    };

    recognitionRef.current = recognition;

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, []);

  const iniciarGrabacion = useCallback(() => {
    setError(null);
    if (!recognitionRef.current) {
      setError('El reconocimiento de voz no está disponible en este navegador. Puedes escribir tus notas manualmente.');
      return;
    }

    try {
      recognitionRef.current.start();
      setEscuchando(true);
    } catch (err) {
      console.warn('Error al iniciar reconocimiento:', err);
    }
  }, []);

  const detenerGrabacion = useCallback(() => {
    if (recognitionRef.current && escuchando) {
      recognitionRef.current.stop();
      setEscuchando(false);
    }
  }, [escuchando]);

  const alternarGrabacion = useCallback(() => {
    if (escuchando) {
      detenerGrabacion();
    } else {
      iniciarGrabacion();
    }
  }, [escuchando, iniciarGrabacion, detenerGrabacion]);

  const limpiarTranscripcion = useCallback(() => {
    setTranscripcion('');
    setError(null);
  }, []);

  return {
    escuchando,
    transcripcion,
    setTranscripcion,
    error,
    soportado,
    iniciarGrabacion,
    detenerGrabacion,
    alternarGrabacion,
    limpiarTranscripcion
  };
}
