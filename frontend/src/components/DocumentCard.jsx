import React from "react";

const DocumentCard = ({ doc }) => {
  if (!doc || !doc.file) return null; // hide if file missing
  const backendUrl = import.meta.env.VITE_API_URL || "https://rapidquest-backend-hgcc.onrender.com";
  const fileUrl = `${backendUrl}${doc.file}`;

  return (
    <div className="card mb-4 shadow-sm">
      <div className="card-body">
        <h5 className="card-title text-center">{doc.filename || "Untitled"}</h5>

        {doc.category && (
          <p>
            <strong>Category:</strong> {doc.category}
          </p>
        )}

        <p>
          <strong>Uploaded:</strong>{" "}
          {doc.uploaded_at ? new Date(doc.uploaded_at).toLocaleString() : "N/A"}
        </p>

        <div className="text-center">
          <a
            href={fileUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-outline-primary"
          >
            Preview
          </a>
        </div>
      </div>
    </div>
  );
};

export default DocumentCard;
