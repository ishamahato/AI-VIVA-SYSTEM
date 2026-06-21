import useRecorder from "../hooks/useRecorder";

export default function MicRecorder({ onSubmit, disabled }) {
  const { recording, audioBlob, audioUrl, error, start, stop, reset } = useRecorder();

  return (
    <div className="mic-recorder">
      {error && <p className="error-text">{error}</p>}
      <div className="mic-controls">
        {!recording && !audioBlob && (
          <button className="btn btn-record" onClick={start} disabled={disabled}>
            Start Recording
          </button>
        )}
        {recording && (
          <button className="btn btn-stop" onClick={stop}>Stop</button>
        )}
        {recording && <span className="recording-dot">Recording...</span>}
      </div>

      {audioUrl && (
        <div className="mic-preview">
          <audio controls src={audioUrl} />
          <div className="mic-actions">
            <button className="btn btn-secondary" onClick={reset} disabled={disabled}>Re-record</button>
            <button className="btn" onClick={() => onSubmit(audioBlob)} disabled={disabled}>Submit Answer</button>
          </div>
        </div>
      )}
    </div>
  );
}
