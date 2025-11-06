// src/components/Sidebar.jsx
import React from "react";
import { NavLink } from "react-router-dom";
import "./../styles.css";

export default function Sidebar() {
  return (
    <div className="sidebar">
      <h2>🧠 AI Support</h2>
      <ul>
        <li>
          <NavLink to="/tickets" className="nav-link">
            🎫 Tickets
          </NavLink>
        </li>
        <li>
          <NavLink to="/knowledge" className="nav-link">
            💡 Knowledge Base
          </NavLink>
        </li>
        <li>
          <NavLink to="/stats" className="nav-link">
            📊 AI Stats
          </NavLink>
        </li>
        <li>
          <NavLink to="/predict" className="nav-link">
            ⚡ Predict
          </NavLink>
        </li>
        <li>
          <NavLink to="/evaluate" className="nav-link">
            🧩 Evaluate Dataset
          </NavLink>
        </li>
        <li>
        <NavLink to="/alerts" className="nav-link">
            🚨 Alerts
        </NavLink>
        </li>
      </ul>
    </div>
  );
}
