// src/pages/ArticleDetailPage.jsx
import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

export default function ArticleDetailPage() {
  const { id } = useParams();
  const [article, setArticle] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/knowledge")
      .then((res) => res.json())
      .then((data) => {
        const found = data.find((a) => a.id === id);
        setArticle(found);
      });
  }, [id]);

  if (!article) return <p>Loading article...</p>;

  return (
    <div className="knowledge-container">
      <h1 className="page-title">📘 {article.title}</h1>
      <div className="article-card">
        <p className="article-content">{article.content}</p>
        <div className="article-footer">
          <span className="category-badge">{article.category}</span>
        </div>
        <Link to="/knowledge">
          <button className="read-more-btn" style={{ marginTop: "15px" }}>
            ← Back to Knowledge Base
          </button>
        </Link>
      </div>
    </div>
  );
}
