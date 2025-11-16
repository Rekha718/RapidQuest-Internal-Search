import React, { useState, useEffect } from "react";
import axios from "axios";
import SearchBar from "../components/SearchBar";
import DocumentList from "../components/DocumentList";

const Dashboard = () => {
  const [documents, setDocuments] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("");
  const [loading, setLoading] = useState(false);

  const API_URL = import.meta.env.VITE_API_URL;

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/api/documents/`);
      setDocuments(res.data || []);
    } catch (err) {
      console.error("Error fetching documents:", err);
      setDocuments([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (query, category) => {
    if (!query && !category) {
      // if no search key and no category, fetch all documents
      fetchDocuments();
      return;
    }

    setLoading(true);
    try {
      let url = `${API_URL}/api/search/?`;
      if (query) url += `q=${encodeURIComponent(query)}&`;
      if (category) url += `category=${encodeURIComponent(category)}&`;
      const res = await axios.get(url);
      setDocuments(res.data || []);
    } catch (err) {
      console.error("Error searching documents:", err);
      setDocuments([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mt-4">
      <h1 className="text-center mb-4">Knowledge Discovery Dashboard</h1>

      <SearchBar
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        selectedCategory={selectedCategory}
        setSelectedCategory={setSelectedCategory}
        onSearch={handleSearch}
      />

      {loading ? (
        <p className="text-center">Loading...</p>
      ) : (
        <DocumentList documents={documents} />
      )}
    </div>
  );
};

export default Dashboard;
