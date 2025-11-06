🤖 AI-Powered Support Ticket Resolution System
🚀 Project Overview

The AI-Powered Support Ticket Resolution System is a full-stack intelligent automation platform designed to help customer support teams efficiently resolve issues by automatically classifying incoming tickets, recommending the most relevant knowledge base articles, and providing actionable analytics.

It combines FastAPI, React, and Groq-powered LLaMA intelligence to deliver real-time insights, accuracy tracking, and alert management.

🧩 Key Features

✅ AI-Based Ticket Classification
Automatically identifies the category of customer issues (Billing, Account, Technical, Product, etc.) using LLaMA (via Groq API).

✅ Semantic Article Recommendation
Uses intelligent text similarity, embeddings, and intent-based matching to recommend relevant KB articles.

✅ Feedback-Driven Accuracy Learning
Supports user feedback for each recommendation. If a user updates feedback, the latest input overwrites the previous one to ensure accuracy in evaluation.

✅ Alert System with Slack Integration
Triggers alerts when accuracy drops below threshold (e.g. 60%), automatically sends them to Slack, and deletes them locally after successful delivery.

✅ Dataset Evaluation for Admins
Allows administrators to evaluate any dataset (JSON format) and calculate system accuracy and coverage metrics.

✅ Real-Time Dashboard
A clean React-based interface to manage tickets, monitor analytics, check alerts, and perform predictions.

🏗️ System Architecture
Frontend (React)
      │
      ▼
FastAPI Backend (app.py)
      │
      ▼
Recommender Engine (Groq-powered LLaMA)
      │
      ▼
JSON Data Store (tickets, feedback, knowledge, alerts)

📂 Project Structure
🖥️ Frontend — /frontend
src/
├── pages/
│   ├── Dashboard.jsx
│   ├── TicketsPage.jsx
│   ├── KnowledgePage.jsx
│   ├── PredictPage.jsx
│   ├── EvaluatePage.jsx
│   ├── AlertsPage.jsx
│   └── AnalyticsPage.jsx
├── components/
│   ├── Navbar.jsx
│   ├── TicketCard.jsx
│   ├── ArticleCard.jsx
│   ├── FeedbackForm.jsx
│   └── Loader.jsx
├── App.jsx
├── index.js
└── App.css

⚙️ Backend — /backend
backend/
├── app.py                 # Main FastAPI server
├── recommender.py         # Core ML logic (LLaMA, embeddings, similarity)
├── evaluator.py           # Accuracy, metrics & dataset evaluation
├── models.py              # Pydantic data models
├── data/
│   ├── tickets.json       # Stored support tickets
│   ├── knowledge.json     # Knowledge base articles
│   ├── feedback.json      # User feedback data
├── logs/
│   ├── recommendation_logs.csv
│   ├── alerts.log
│   ├── system_monitor.log
├── reports/
│   └── coverage_report.csv
└── .env                   # Environment variables (Groq & Slack)

🧠 How It Works

Ticket Creation:
Users submit an issue through the frontend.
→ Backend classifies the ticket using Groq LLaMA.
→ Tags are generated and matching KB articles are recommended.

Feedback Update:
Feedback is stored per ticket & article combination.
If feedback is submitted again, it overwrites the previous one.

Accuracy Monitoring:
System computes real-time accuracy based on feedback.
If accuracy < threshold, an alert is triggered & sent to Slack.

Alert Management:
Alerts are automatically deleted from local logs once confirmed as sent to Slack.

Evaluation:
Admin can run offline evaluations on datasets to validate model accuracy and coverage.

🧰 Tech Stack
Layer	Technology
Frontend	React.js, CSS, Tailwind
Backend	FastAPI (Python 3.10+)
AI/ML	spaCy, NumPy, Groq API (LLaMA)
Data Storage	JSON, CSV Logs
Integration	Slack Webhooks
Deployment	Render / Localhost
⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/ai-support-engine.git
cd ai-support-engine

2️⃣ Backend Setup
cd backend
pip install -r requirements.txt


Create a .env file in the backend folder:

GROQ_API_KEY=your_groq_api_key_here
SLACK_WEBHOOK_URL=your_slack_webhook_url_here


Run the FastAPI backend:

uvicorn app:app --reload


Visit API docs:
➡️ http://127.0.0.1:8000/docs

3️⃣ Frontend Setup
cd frontend
npm install
npm start

🧩 Sample Ticket Examples
Name	Issue	Description
Rahul Sharma	Refund not received	I returned my jacket 5 days ago, but I haven’t received any refund yet.
Neha Patel	Delayed delivery	My parcel shows dispatched since last week, but it hasn’t reached me yet.
Arjun Verma	Payment failure	Payment failed, but the amount was deducted from my bank account.
📊 Evaluation Metrics
Metric	Description
Accuracy	% of correct feedback from total feedback
Coverage	% of tickets with recommendations
Resolution Rate	% of resolved tickets after recommendations
Alerts	Triggered if accuracy < 60%
🔔 Slack Integration

Whenever accuracy drops below 60%, the backend:

Logs the alert locally

Sends a notification to the configured Slack channel

Deletes the alert from local storage after confirmation


👩‍💻 Author

Manthena Sai Phani Sreeja
📧 Full-Stack Developer & AI Engineer

🪪 License

This project is licensed under the MIT License.

🙌 Acknowledgements

Groq API for fast LLaMA model inference

FastAPI for the backend framework

React.js for frontend

Slack API for real-time alerting

spaCy and NumPy for text processing and embeddings
