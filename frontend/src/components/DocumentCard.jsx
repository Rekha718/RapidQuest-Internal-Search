import React from "react";

// Appwrite config (you can also move these to .env)
const APPWRITE_ENDPOINT = "https://fra.cloud.appwrite.io/v1";
const APPWRITE_PROJECT_ID = "69199dd4001999027b50";
const APPWRITE_BUCKET_ID = "69199e4b0022548436b1";

const DocumentCard = ({ doc }) => {
  if (!doc || !doc.file_id) return null; // hide if file missing

  // Construct Appwrite file view URL
  const fileUrl = `${APPWRITE_ENDPOINT}/storage/buckets/${APPWRITE_BUCKET_ID}/files/${doc.file_id}/view?project=${APPWRITE_PROJECT_ID}&mode=inline`;

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
