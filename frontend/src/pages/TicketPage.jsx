// src/pages/TicketPage.jsx
import React, { useEffect, useState } from "react";
import TicketForm from "../components/TicketForm";
import TicketList from "../components/TicketList";

export default function TicketPage() {
  const [tickets, setTickets] = useState([]);
  const [knowledge, setKnowledge] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/tickets")
      .then((res) => res.json())
      .then(setTickets)
      .catch(console.error);

    fetch("http://localhost:8000/api/knowledge")
      .then((res) => res.json())
      .then(setKnowledge)
      .catch(console.error);
  }, []);

  const handleAddTicket = async (newTicket) => {
    const res = await fetch("http://localhost:8000/api/tickets", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newTicket),
    });
    const saved = await res.json();
    setTickets([...tickets, saved]);
  };

  const handleUpdateStatus = async (id, newStatus) => {
    const res = await fetch(`http://localhost:8000/api/tickets/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: newStatus }),
    });
    const updated = await res.json();
    setTickets((prev) =>
      prev.map((t) => (t.id === id ? { ...t, status: updated.status } : t))
    );
  };

  return (
    <div>
      <h1>🎫 Ticket Management</h1>
      <TicketForm onAddTicket={handleAddTicket} />
      <TicketList
        tickets={tickets}
        onUpdateStatus={handleUpdateStatus}
        knowledge={knowledge}
      />
    </div>
  );
}
