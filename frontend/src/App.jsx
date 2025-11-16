import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import UploadDocumentPage from "./pages/UploadDocumentPage"; 

const App = () => {
  return (
    <div className="container mt-5">
      <nav className="mb-4">
        <Link to="/" className="btn btn-outline-primary me-2">
          Dashboard
        </Link>
        <Link to="/upload" className="btn btn-outline-success">
          Upload Document
        </Link>
      </nav>

      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/upload" element={<UploadDocumentPage />} />
      </Routes>
    </div>
  );
};

export default App;
