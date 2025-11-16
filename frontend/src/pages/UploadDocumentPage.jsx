import React, { useState } from "react";
import axios from "axios";

const UploadDocumentPage = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  // Use only Vite env variable
  const API_URL = import.meta.env.VITE_API_URL;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(`${API_URL}/api/upload/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setMessage("Uploaded successfully: " + (res.data.filename || "File"));
      setFile(null);
    } catch (err) {
      console.error("Upload error:", err);
      setMessage("Upload failed. Please try again.");
    }
  };

  return (
    <div className="container mt-4">
      <h1 className="text-center mb-4">Upload Document</h1>
      <form onSubmit={handleSubmit} className="text-center">
        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
          className="form-control mb-3"
        />
        <button type="submit" className="btn btn-success">
          Upload
        </button>
      </form>
      {message && <p className="text-center mt-3">{message}</p>}
    </div>
  );
};

export default UploadDocumentPage;
