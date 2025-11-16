import React, { useState } from "react";
import { Client, Storage } from "appwrite";

// Appwrite config (you can also move these to .env)
const APPWRITE_ENDPOINT = "https://fra.cloud.appwrite.io/v1";
const APPWRITE_PROJECT_ID = "69199dd4001999027b50";
const APPWRITE_BUCKET_ID = "69199e4b0022548436b1";

const client = new Client()
  .setEndpoint(APPWRITE_ENDPOINT)
  .setProject(APPWRITE_PROJECT_ID);

const storage = new Storage(client);

const UploadDocumentPage = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setMessage("Please select a file first.");
      return;
    }

    try {
      // Upload file to Appwrite storage
      const response = await storage.createFile(APPWRITE_BUCKET_ID, "unique()", file);
      console.log("Appwrite upload response:", response);

      // You can optionally send file metadata to your backend
      // axios.post(`${API_URL}/api/upload/`, { filename: file.name, file_id: response.$id });

      setMessage("Uploaded successfully: " + file.name);
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
          accept="application/pdf"
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
