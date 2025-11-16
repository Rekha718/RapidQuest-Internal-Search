import React from "react";
import DocumentCard from "./DocumentCard";

const DocumentList = ({ documents }) => {
  if (!documents || !documents.length) {
    return <p className="text-center">No documents found.</p>;
  }

  return (
    <div className="row">
      {documents.map((doc) => (
        <div className="col-md-6 mb-4" key={doc.id || Math.random()}>
          <DocumentCard doc={doc} />
        </div>
      ))}
    </div>
  );
};

export default DocumentList;
