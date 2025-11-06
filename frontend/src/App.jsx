// src/App.jsx
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import TicketPage from "./pages/TicketPage";
import StatsPage from "./pages/StatsPage";
import PredictPage from "./pages/PredictPage";
import KnowledgePage from "./pages/KnowledgePage";
import EvaluatePage from "./pages/EvaluatePage";
import AlertsPage from "./pages/AlertsPage";
import ArticleDetailPage from "./pages/ArticleDetailPage";  


export default function App() {
  return (
    <Router>
      <div className="app-container">
        <Sidebar />
        <div className="main-content">
          <Routes>
            <Route path="/" element={<TicketPage />} />
            <Route path="/tickets" element={<TicketPage />} />
            <Route path="/stats" element={<StatsPage />} />
            <Route path="/predict" element={<PredictPage />} />
            <Route path="/knowledge" element={<KnowledgePage />} />
            <Route path="/knowledge/:id" element={<ArticleDetailPage />} />
            <Route path="/evaluate" element={<EvaluatePage />} />
            <Route path="/alerts" element={<AlertsPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}
