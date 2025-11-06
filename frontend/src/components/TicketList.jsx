// TicketList.jsx
import React, { useState, useEffect } from "react";

export default function TicketList({ tickets, onUpdateStatus, knowledge }) {
  const [expanded, setExpanded] = useState(null);
  const [articlesMap, setArticlesMap] = useState({});

  useEffect(() => {
    if (knowledge && knowledge.length > 0) {
      const map = {};
      knowledge.forEach((k) => {
        map[String(k.id)] = k;
      });
      setArticlesMap(map);
    }
  }, [knowledge]);

  const getArticleById = (id) => {
    if (!id) return null;
    return articlesMap[String(id)] || null;
  };

  const handleExpand = (ticketId, articleId) => {
    const key = `${ticketId}_${articleId}`;
    setExpanded(expanded === key ? null : key);
  };

  return (
    <div>
      <h2>🎫 Tickets</h2>
      {tickets.length === 0 && <p>No tickets yet</p>}

      <div className="ticket-list">
        {tickets.map((t) => (
          <div key={t.id} className="ticket-card">
            <div className="ticket-header">
              <span className="ticket-emoji">🎟️</span>
              <h3>{t.title}</h3>
            </div>

            <p><strong>Description:</strong> {t.description}</p>

            <p>
              <strong>Status:</strong>{" "}
              <span className={`status-badge ${t.status.toLowerCase()}`}>
                {t.status}
              </span>
            </p>

            <p><small>{new Date(t.createdAt).toLocaleString()}</small></p>

            {/* 🔍 Recommendations */}
            <div className="recommendations">
  <strong>Recommended Articles:</strong>
  {t.recommendedArticleIds && t.recommendedArticleIds.length > 0 ? (
    <ul>
      {t.recommendedArticleIds.map((id) => {
        const art = getArticleById(id);
        const key = `${t.id}_${id}`;
        return (
          <li key={id}>
            <button className="link-button" onClick={() => handleExpand(t.id, id)}>
              {art ? art.title : `Article ${id}`}
            </button>

            {expanded === key && art && (
              <div className="article-preview">
                <p>{art.content}</p>
                {art.tags && <small>Tags: {art.tags.join(", ")}</small>}
                {/* 🧠 Feedback Buttons */}
                <div className="feedback-actions">
                  <button
                    className="thumb-btn correct"
                    onClick={async () => {
                      await fetch("http://localhost:8000/api/feedback", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                          ticket_id: t.id,
                          article_id: id,
                          correct: true,
                          notes: "Relevant recommendation",
                        }),
                      });
                      alert("✅ Feedback recorded as correct!");
                    }}
                  >
                    👍
                  </button>
                  <button
                    className="thumb-btn incorrect"
                    onClick={async () => {
                      await fetch("http://localhost:8000/api/feedback", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                          ticket_id: t.id,
                          article_id: id,
                          correct: false,
                          notes: "Not a relevant suggestion",
                        }),
                      });
                      alert("❌ Feedback recorded as incorrect!");
                    }}
                  >
                    👎
                  </button>
                </div>
              </div>
            )}
          </li>
        );
      })}
    </ul>
  ) : (
    <p>No recommendations</p>
  )}
</div>

            <div className="actions">
              {t.status !== "closed" && (
                <button
                  className="close-btn"
                  onClick={() => onUpdateStatus(t.id, "closed")}
                >
                  Close Ticket
                </button>
              )}
              {t.status !== "resolved" && (
                <button
                  className="resolve-btn"
                  onClick={() => onUpdateStatus(t.id, "resolved")}
                >
                  Mark Resolved
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
