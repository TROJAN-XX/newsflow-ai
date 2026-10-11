import React from "react";

function SearchBar({ query, onQueryChange }) {
  return (
    <div className="search-bar">
      <span className="search-icon">🔍</span>
      <input
        id="search-input"
        className="search-input"
        type="text"
        placeholder="Search articles by title, keyword, or source..."
        value={query}
        onChange={(e) => onQueryChange(e.target.value)}
        autoComplete="off"
      />
    </div>
  );
}

export default SearchBar;
