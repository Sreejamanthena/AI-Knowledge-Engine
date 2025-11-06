import React, { useState } from "react";
import "../styles.css"; // Ensure global CSS is applied

export default function EvaluatePage() {
  const [path, setPath] = useState("data/dataset.json");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleEvaluate = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/admin/evaluate_dataset", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ dataset_path: path }),
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("Evaluation failed:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="evaluate-container">
      <h1 className="page-title">🧩 Evaluate Dataset</h1>

      {/* Input Section */}
      <div className="evaluate-section">
        <input
          type="text"
          className="dataset-input"
          value={path}
          onChange={(e) => setPath(e.target.value)}
          placeholder="Enter dataset file path"
        />
        <button
          className="run-evaluation-btn"
          onClick={handleEvaluate}
          disabled={loading}
        >
          {loading ? "Evaluating..." : "Run Evaluation"}
        </button>
      </div>

      {/* Results Section */}
      {result && (
        <div className="evaluation-results">
          <h3>📊 Evaluation Results</h3>
          <p>
            <strong>Dataset Size:</strong> {result.dataset_size}
          </p>
          <p>
            <strong>Accuracy:</strong>{" "}
            {result.accuracy ? result.accuracy.toFixed(2) + "%" : "N/A"}
          </p>
        </div>
      )}
    </div>
  );
}
