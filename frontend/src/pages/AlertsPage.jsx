import React, { useEffect, useState } from "react";

export default function AlertsPage() {
  const [alerts, setAlerts] = useState([]);

  const fetchAlerts = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/alerts");
      const data = await res.json();
      setAlerts(data.alerts || []);
    } catch (err) {
      console.error("Error fetching alerts:", err);
    }
  };

  const deleteAlert = async (index) => {
    try {
      const res = await fetch("http://localhost:8000/api/alerts/delete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ index }),
      });
      const data = await res.json();
      if (data.success) {
        // Smoothly fade out before removing
        setAlerts((prev) =>
          prev.map((a, i) =>
            i === index ? { ...a, fading: true } : a
          )
        );
        setTimeout(() => {
          setAlerts((prev) => prev.filter((_, i) => i !== index));
        }, 400); // match fade-out duration
      }
    } catch (err) {
      console.error("Error deleting alert:", err);
    }
  };

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="page">
      <h2>🚨 System Alerts</h2>
      {alerts.length === 0 ? (
        <p>No alerts yet.</p>
      ) : (
        <div className="alerts-list">
          {alerts.map((alert, i) => (
            <div
              key={i}
              className={`alert-card ${alert.fading ? "fade-out" : ""}`}
            >
              <div className="alert-header">
                <p><strong>⚠️ {alert.message}</strong></p>
                <button
                  className="delete-alert-btn"
                  onClick={() => deleteAlert(i)}
                >
                  ✖
                </button>
              </div>
              <small>{new Date(alert.timestamp).toLocaleString()}</small>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
