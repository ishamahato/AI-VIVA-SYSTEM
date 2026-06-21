import { useState, useRef, useCallback } from "react";

// Records microphone audio and returns the recorded Blob (audio/webm).
export default function useRecorder() {
  const [recording, setRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [error, setError] = useState(null);
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const streamRef = useRef(null);

  const start = useCallback(async () => {
    setError(null);
    setAudioBlob(null);
    setAudioUrl(null);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      const mr = new MediaRecorder(stream);
      chunksRef.current = [];
      mr.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };
      mr.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: mr.mimeType || "audio/webm" });
        setAudioBlob(blob);
        setAudioUrl(URL.createObjectURL(blob));
        if (streamRef.current) streamRef.current.getTracks().forEach((t) => t.stop());
      };
      mr.start();
      mediaRecorderRef.current = mr;
      setRecording(true);
    } catch {
      setError("Microphone access denied or unavailable.");
    }
  }, []);

  const stop = useCallback(() => {
    if (mediaRecorderRef.current) mediaRecorderRef.current.stop();
    setRecording(false);
  }, []);

  const reset = useCallback(() => {
    setAudioBlob(null);
    setAudioUrl(null);
    setError(null);
  }, []);

  return { recording, audioBlob, audioUrl, error, start, stop, reset };
}
