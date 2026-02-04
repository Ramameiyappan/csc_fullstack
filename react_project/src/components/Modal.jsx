import "../styles/modal.css";

const Modal = ({ show, onClose, children }) => {
  if (!show) return null;

  return (
    <div
      className="modal-bg"
      onClick={onClose}
    >
      <div
        className="modal-box"
        onClick={(e) => e.stopPropagation()}
      >
        <span className="close" onClick={onClose}>
          ×
        </span>

        {children}
      </div>
    </div>
  );
};

export default Modal;
