export default function Spinner({ label = "Loading..." }) {
  return (
    <div className="spinner-wrap">
      <div className="spinner" />
      {label && <p className="spinner-label">{label}</p>}
    </div>
  );
}
