// src/pages/FeedbackPage.jsx
import React, { useEffect, useState } from "react";

export default function FeedbackPage() {
  const [feedback, setFeedback] = useState([]);
  const [ticketId, setTicketId] = useState("");
  const [articleId, setArticleId] = useState("");
  const [correct, setCorrect] = useState(true);
  const [notes, setNotes] = useState("");

  // Load all feedback entries
  const fetchFeedback = async () => {
    const res = await fetch("http://localhost:8000/data/feedback.json");
    const data = await res.json().catch(() => []);
    setFeedback(data);
  };

  useEffect(() => {
    fetchFeedback();
  }, []);

  // Submit feedback
  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = { ticket_id: ticketId, article_id: articleId, correct, notes };

    const res = await fetch("http://localhost:8000/api/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (res.ok) {
      alert("✅ Feedback submitted!");
      setTicketId("");
      setArticleId("");
      setNotes("");
      fetchFeedback();
    } else {
      alert("❌ Failed to submit feedback");
    }
  };

  return (
    <div className="page">
      <h2>🗳️ Feedback</h2>

      <form className="feedback-form" onSubmit={handleSubmit}>
        <input
          placeholder="Ticket ID (e.g., t_1)"
          value={ticketId}
          onChange={(e) => setTicketId(e.target.value)}
        />
        <input
          placeholder="Article ID (e.g., art_2)"
          value={articleId}
          onChange={(e) => setArticleId(e.target.value)}
        />
        <select value={correct} onChange={(e) => setCorrect(e.target.value === "true")}>
          <option value="true">Correct</option>
          <option value="false">Incorrect</option>
        </select>
        <textarea
          placeholder="Add optional notes..."
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
        ></textarea>
        <button type="submit">Submit Feedback</button>
      </form>

      <h3>📋 Submitted Feedback</h3>
      <ul className="feedback-list">
        {feedback.map((f) => (
          <li key={f.id}>
            <strong>{f.ticket_id || "—"}</strong> → {f.article_id} |{" "}
            {f.correct ? "✅ Correct" : "❌ Wrong"} <br />
            <small>{f.notes}</small>
          </li>
        ))}
      </ul>
    </div>
  );
}
