import React, { useState } from "react";
import "../styles.css";

export default function PredictPage() {
  const [desc, setDesc] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async (e) => {
    e.preventDefault();
    if (!desc.trim()) {
      alert("Please describe your issue before submitting.");
      return;
    }

    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description: desc }),
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("Prediction failed:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="predict-container">
      <h1 className="page-title">⚡ Real-time Prediction</h1>

      <form onSubmit={handlePredict} className="predict-form">
        <textarea
          className="predict-textarea"
          placeholder="Describe your issue..."
          value={desc}
          onChange={(e) => setDesc(e.target.value)}
          rows={5}
        />
        <button type="submit" className="predict-btn" disabled={loading}>
          {loading ? "Processing..." : "Get Recommendations"}
        </button>
      </form>

      {result && (
        <div className="predict-results">
          <h3>Top Recommendations</h3>
          <ul>
            {result.results.map((r) => (
              <li key={r.id}>
                <strong>{r.title}</strong> — {r.score.toFixed(3)}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
