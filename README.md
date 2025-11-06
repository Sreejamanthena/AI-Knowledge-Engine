# 🤖 AI-Powered Support Ticket Resolution System

### 🚀 Project Overview

The **AI-Powered Support Ticket Resolution System** is a full-stack intelligent automation platform that helps customer support teams classify tickets, recommend the most relevant knowledge base (KB) articles, and track system performance in real time.

This project uses **FastAPI (Python)** for the backend, **React.js** for the frontend, and integrates **Groq-powered LLaMA** for AI-driven classification, tagging, and recommendations.  
It’s designed to improve support efficiency, accuracy, and proactive issue detection through real-time alerts and analytics.

---

## 🧠 Key Features

✅ **AI Ticket Classification**  
Automatically identifies the type of ticket (Billing, Account, Technical, Product, etc.) using **LLaMA (Groq API)**.  

✅ **Smart Knowledge Recommendations**  
Finds and recommends the most relevant KB article based on text similarity, embeddings, and intent.  

✅ **Feedback Learning System**  
Overwrites previous feedback to maintain accurate, up-to-date evaluation metrics.  

✅ **Slack Alerts**  
Automatically triggers and sends alerts when accuracy drops below a set threshold (e.g. 60%) and deletes them locally once sent.  

✅ **Admin Evaluation Module**  
Allows dataset accuracy evaluation and system performance checks.  

✅ **Real-Time React Dashboard**  
A modern web interface to manage tickets, run evaluations, check alerts, and view analytics.  

---

## 🏗️ System Architecture

Frontend (React)
│
▼
FastAPI Backend (app.py)
│
▼
Recommender Engine (Groq-powered LLaMA)
│
▼
JSON Data Storage (tickets, feedback, knowledge, alerts)

yaml
Copy code

---

## 📂 Project Structure

### 🖥️ Frontend — `/frontend`
src/
├── pages/
│ ├── TicketPage.jsx
│ ├── KnowledgePage.jsx
│ ├── PredictPage.jsx
│ ├── EvaluatePage.jsx
│ ├── AlertsPage.jsx
│ ├── StatsPage.jsx
│ └── ArticleDetailPage.jsx
├── components/
│ ├── Sidebar.jsx
│ ├── TicketCard.jsx
│ └── Loader.jsx
├── App.jsx
├── index.js
└── styles.css

shell
Copy code

### ⚙️ Backend — `/backend`
backend/
├── app.py # Main FastAPI application
├── recommender.py # AI logic (LLaMA, embeddings, similarity)
├── evaluator.py # Accuracy & metrics evaluation
├── models.py # Pydantic schemas
├── data/
│ ├── tickets.json # Tickets data
│ ├── knowledge.json # Knowledge articles
│ ├── feedback.json # Feedback data
├── logs/
│ ├── alerts.log
│ ├── system_monitor.log
│ ├── recommendation_logs.csv
├── reports/
│ └── coverage_report.csv
└── .env # API keys and config

yaml
Copy code

---

## ⚙️ Installation & Setup

### 🧩 1️⃣ Clone the Repository
```bash
git clone https://github.com/Sreejamanthena/AI-Knowledge-Engine.git
cd AI-Knowledge-Engine
⚙️ 2️⃣ Backend Setup
bash
Copy code
cd backend
pip install -r requirements.txt
Create a .env file inside backend/:

env
Copy code
GROQ_API_KEY=your_groq_api_key_here
SLACK_WEBHOOK_URL=your_slack_webhook_url_here
Run the backend:

bash
Copy code
uvicorn app:app --reload
📍 Visit API Docs → http://127.0.0.1:8000/docs

💻 3️⃣ Frontend Setup
bash
Copy code
cd frontend
npm install
npm start
The React app will launch automatically at http://localhost:3000

🧠 How It Works
Ticket Creation:

User submits a new support ticket.

The backend classifies and tags the issue using Groq’s LLaMA model.

Relevant KB articles are recommended instantly.

Feedback Tracking:

Feedback per ticket-article pair is recorded.

If new feedback is given, old feedback is overwritten.

Accuracy Monitoring:

System calculates real-time accuracy based on feedback.

If accuracy < 60%, Slack alerts are triggered.

Alert Management:

Alerts are auto-removed once successfully sent to Slack.

Evaluation:

Admins can run dataset evaluations to verify system accuracy and coverage.

🧾 Sample Ticket Examples
Customer Name	Issue	Description
Rahul Sharma	Refund not received	I returned my jacket 5 days ago but still haven’t got my refund.
Neha Patel	Delayed delivery	My order has been marked dispatched for a week but not delivered.
Arjun Verma	Payment failed	Payment failed during checkout but amount was deducted.
Sneha Reddy	Wrong product delivered	I received the wrong size and color of shoes.
Rakesh Gupta	Unable to cancel order	I want to cancel my order placed today but can’t find the option.

📊 Evaluation Metrics
Metric	Description
Accuracy	% of correct feedback vs total feedback
Coverage	% of tickets with valid recommendations
Resolution Rate	% of resolved tickets among recommended
Alerts	Triggered when accuracy < threshold

🔔 Slack Alert System
If system accuracy < 60%, an alert is logged locally.

The same message is automatically sent to a configured Slack channel.

After a successful send, the alert entry is deleted from the local JSON file.

🧰 Tech Stack
Layer	Technology
Frontend	React.js, Tailwind, CSS
Backend	FastAPI, Python 3.10+
AI/ML	spaCy, NumPy, Groq LLaMA
Storage	JSON, CSV
Integration	Slack Webhooks
Deployment	Render / Localhost

🧩 Future Enhancements
Add multilingual support (Hindi + regional)

Integrate FAISS / ChromaDB for advanced semantic retrieval

Add auto-learning feedback re-ranking

Deploy as a cloud-native microservice

👩‍💻 Author
Manthena Sai Phani Sreeja
💡 Full-Stack Developer & AI Engineer
📧 GitHub Profile

🪪 License
This project is licensed under the MIT License.

🙌 Acknowledgements
Groq API — LLaMA-3 model for smart classification

FastAPI — high-performance backend framework

React.js — modern frontend UI

Slack API — real-time notifications

spaCy + NumPy — NLP and embeddings

🌟 Feedback
If you found this project helpful, please ⭐ the repository and share your feedback!

yaml
Copy code

---

Would you like me to include **badges** (e.g., Python version, FastAPI, React, license, and build status) at the top?  
It’ll make your GitHub page look even more professional (like a portfolio-ready project).
