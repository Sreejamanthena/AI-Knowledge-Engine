// src/pages/KnowledgePage.jsx
import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles.css";

export default function KnowledgePage() {
  const [articles, setArticles] = useState([]);
  const [search, setSearch] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("All");
  const navigate = useNavigate();

  // Fetch knowledge base articles
  useEffect(() => {
    fetch("http://localhost:8000/api/knowledge")
      .then((res) => res.json())
      .then(setArticles)
      .catch(console.error);
  }, []);

  // Collect unique categories from articles
  const categories = [
    "All",
    ...Array.from(new Set(articles.map((a) => a.category))).filter(Boolean),
  ];

  // Apply both text and category filters
  const filtered = articles.filter((a) => {
    const matchesText =
      a.title.toLowerCase().includes(search.toLowerCase()) ||
      a.content.toLowerCase().includes(search.toLowerCase()) ||
      a.category.toLowerCase().includes(search.toLowerCase());

    const matchesCategory =
      categoryFilter === "All" || a.category === categoryFilter;

    return matchesText && matchesCategory;
  });

  return (
    <div className="knowledge-container">
      <h1 className="page-title">💡 Knowledge Base</h1>

      {/* 🔍 Search + Category Filter Row */}
      <div className="search-filter-row">
        <input
          type="text"
          className="search-input"
          placeholder="Search articles..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        <select
          className="category-dropdown"
          value={categoryFilter}
          onChange={(e) => setCategoryFilter(e.target.value)}
        >
          {categories.map((cat) => (
            <option key={cat} value={cat}>
              {cat}
            </option>
          ))}
        </select>
      </div>

      {/* 📰 Articles Section */}
      {filtered.length === 0 ? (
        <p className="no-data">No matching articles found.</p>
      ) : (
        <div className="articles-grid">
          {filtered.map((a) => (
            <div key={a.id} className="article-card">
              <h3 className="article-title">{a.title}</h3>

              <p className="article-content">
                {a.content.length > 200
                  ? `${a.content.slice(0, 200)}...`
                  : a.content}
              </p>

              <div className="article-footer">
                <span className="category-badge">{a.category}</span>

                <button
                  className="read-more-btn"
                  onClick={() => navigate(`/knowledge/${a.id}`)}
                >
                  Read More →
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
