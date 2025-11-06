// src/pages/StatsPage.jsx
import React, { useEffect, useState } from "react";
import "../styles.css";

export default function StatsPage() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadAnalytics = async () => {
    setRefreshing(true);
    try {
      const res = await fetch("http://localhost:8000/api/analytics");
      const data = await res.json();
      setAnalytics(data);
    } catch (err) {
      console.error("Failed to load analytics:", err);
      setAnalytics(null);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
    // optional: poll every 60 seconds
    const id = setInterval(loadAnalytics, 60 * 1000);
    return () => clearInterval(id);
  }, []);

  if (loading) return <p>Loading analytics...</p>;

  if (!analytics) return <p>Failed to load analytics.</p>;

  const { summary, per_article: perArticle = [], low_ctr: lowCtr = [] } = analytics;

  return (
    <div className="page">
      <h2>📊 AI Content Gap & Performance</h2>

      <div className="card">
        <h3>Summary</h3>
        <p><strong>Total articles:</strong> {summary?.total_articles ?? 0}</p>
        <p><strong>Total tickets:</strong> {summary?.total_tickets ?? 0}</p>
        <p><strong>Tickets with recommendations:</strong> {summary?.tickets_with_recommendations ?? 0}</p>
        <p><strong>Coverage:</strong> {summary?.coverage_percent ?? 0}%</p>
        <p><strong>Resolution rate (recommended tickets):</strong> {summary?.resolution_rate_percent ?? 0}%</p>
        <p><strong>Total feedback:</strong> {summary?.total_feedback ?? 0}</p>
        <button onClick={loadAnalytics} disabled={refreshing} style={{marginTop:12}}>
          {refreshing ? "Refreshing..." : "Refresh"}
        </button>
      </div>

      <div className="card" style={{marginTop: 16}}>
        <h3>Per-article performance (CTR)</h3>
        {perArticle.length === 0 ? (
          <p>No article data yet.</p>
        ) : (
          <div style={{maxHeight: 360, overflowY: "auto"}}>
            <table style={{width: "100%", borderCollapse: "collapse"}}>
              <thead>
                <tr style={{textAlign: "left", borderBottom: "1px solid #e2e8f0"}}>
                  <th style={{padding:8}}>Article</th>
                  <th style={{padding:8}}>Impressions</th>
                  <th style={{padding:8}}>Clicks</th>
                  <th style={{padding:8}}>CTR (%)</th>
                </tr>
              </thead>
              <tbody>
                {perArticle.map((a) => (
                  <tr key={a.article_id} style={{borderBottom: "1px solid #f1f5f9"}}>
                    <td style={{padding:8}}>{a.title || a.article_id}</td>
                    <td style={{padding:8}}>{a.impressions}</td>
                    <td style={{padding:8}}>{a.clicks}</td>
                    <td style={{padding:8}}>{a.ctr}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      <div className="card" style={{marginTop:16}}>
        <h3>Low-performing articles (CTR &lt; 10%)</h3>
        {(!lowCtr || lowCtr.length === 0) ? (
          <p>No low-CTR articles found.</p>
        ) : (
          <ul>
            {lowCtr.map((a) => (
              <li key={a.article_id}>
                <strong>{a.title || a.article_id}</strong> — CTR: {a.ctr}% | Impressions: {a.impressions} | Clicks: {a.clicks}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
