import React from "react";

const SearchBar = ({
  searchQuery = "",
  setSearchQuery,
  selectedCategory = "",
  setSelectedCategory,
  onSearch = () => {},
}) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    // Trigger search only when Search button is clicked
    onSearch(searchQuery, selectedCategory);
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setSearchQuery(value);

    // If input is cleared, automatically fetch all documents
    if (value === "") {
      onSearch("", selectedCategory);
    }
  };

  const handleCategoryChange = (e) => {
    const category = e.target.value;
    setSelectedCategory(category);
    // Do NOT trigger search automatically here
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="d-flex justify-content-center mb-4 gap-2"
    >
      <input
        type="text"
        className="form-control"
        placeholder="Search documents..."
        value={searchQuery}
        onChange={handleInputChange}
        style={{ maxWidth: "300px" }}
      />

      <select
        className="form-select"
        value={selectedCategory}
        onChange={handleCategoryChange}
        style={{ maxWidth: "200px" }}
      >
        <option value="">All Categories</option>
        <option value="Project/Hackathon">Project/Hackathon</option>
        <option value="Marketing">Marketing</option>
        <option value="Finance/Sales">Finance/Sales</option>
        <option value="Tech">Tech</option>
        <option value="General">General</option>
      </select>

      <button type="submit" className="btn btn-primary">
        Search
      </button>
    </form>
  );
};

export default SearchBar;
