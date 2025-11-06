import React, { useState, useEffect } from "react";

export default function TicketForm({ onAddTicket }) {
  const [customerName, setCustomerName] = useState("");
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [recommendation, setRecommendation] = useState(null);
  const [expanded, setExpanded] = useState(false);
  const [errors, setErrors] = useState({});

  // 🧩 Validation
  const validate = () => {
    const newErrors = {};
    if (!customerName.trim() || customerName.trim().length < 2)
      newErrors.customerName = "Name must be at least 2 characters";
    if (!title.trim()) newErrors.title = "Title is required";
    if (!description.trim()) newErrors.description = "Description is required";
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // 🧠 Real-time Recommendation (debounced)
  useEffect(() => {
    const handler = setTimeout(async () => {
      if (description.trim().length > 5) {
        try {
          const res = await fetch("http://localhost:8000/api/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ description, top_k: 1 }),
          });
          const data = await res.json();
          if (data.results && data.results.length > 0) {
            setRecommendation(data.results[0]);
          } else {
            setRecommendation(null);
          }
        } catch (err) {
          console.error("Recommendation error:", err);
        }
      } else {
        setRecommendation(null);
      }
    }, 800); // debounce
    return () => clearTimeout(handler);
  }, [description]);

  // 📝 Submit Ticket
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validate()) return;

    const newTicket = {
      customer_name: customerName,
      title,
      description,
      status: "open",
      createdAt: new Date().toISOString(),
    };

    onAddTicket(newTicket);

    setCustomerName("");
    setTitle("");
    setDescription("");
    setRecommendation(null);
  };

  return (
    <div className="ticket-form">
      <h2>📝 Create Ticket</h2>
      <form onSubmit={handleSubmit}>
        {/* 👤 Customer Name */}
        <div className="form-group">
          <input
            type="text"
            placeholder="Your Name"
            value={customerName}
            onChange={(e) => setCustomerName(e.target.value)}
          />
          {errors.customerName && (
            <small className="error">{errors.customerName}</small>
          )}
        </div>

        {/* 🎫 Title */}
        <div className="form-group">
          <input
            type="text"
            placeholder="Ticket Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
          {errors.title && <small className="error">{errors.title}</small>}
        </div>

        {/* 🧾 Description */}
        <div className="form-group">
          <textarea
            placeholder="Describe your issue..."
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          ></textarea>
          {errors.description && (
            <small className="error">{errors.description}</small>
          )}
        </div>

        {/* 💡 Real-time Recommendation */}
        {recommendation && (
          <div className="recommendation-box">
            <strong>💡 Suggested Article:</strong>
            <p>
              <button
                type="button"
                className="recommend-btn"
                onClick={() => setExpanded(!expanded)}
              >
                {recommendation.title}
              </button>
            </p>
            {expanded && (
              <div className="article-snippet">
                <p>{recommendation.snippet}</p>
                <small>
                  Relevance Score: {recommendation.score.toFixed(2)}
                </small>
              </div>
            )}
          </div>
        )}

        <button type="submit" className="submit-btn">
          Submit Ticket
        </button>
      </form>
    </div>
  );
}
