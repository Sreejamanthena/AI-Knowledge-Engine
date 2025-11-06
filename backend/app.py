from fastapi import FastAPI, Query, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from datetime import datetime
from typing import Dict, Any, List
import csv
import requests  # ✅ for Slack webhook

from recommender import recommend_articles, get_embedding, generate_tags_with_llama, classify_category
from models import KnowledgeCreate, TicketCreate, Ticket
from evaluator import compute_metrics_from_feedback, evaluate_dataset_file

# ---------- App init ----------
app = FastAPI(title="AI Ticket Resolution API")

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Paths ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

DATA_TICKETS = os.path.join(DATA_DIR, "tickets.json")
DATA_KNOWLEDGE = os.path.join(DATA_DIR, "knowledge.json")
DATA_FEEDBACK = os.path.join(DATA_DIR, "feedback.json")
PREDICT_LOG = os.path.join(LOGS_DIR, "recommendation_logs.csv")
SYSTEM_LOG = os.path.join(LOGS_DIR, "system_monitor.log")
ALERTS_LOG = os.path.join(LOGS_DIR, "alerts.log")
COVERAGE_REPORT_CSV = os.path.join(REPORTS_DIR, "coverage_report.csv")

# ---------- Slack ----------
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_message(message: str):
    """Send a formatted message to Slack if webhook is configured."""
    if SLACK_WEBHOOK_URL:
        try:
            payload = {"text": f":rotating_light: *AI Support Alert*\n{message}"}
            requests.post(SLACK_WEBHOOK_URL, json=payload, timeout=5)
        except Exception as e:
            print(f"[Slack Error] {e}")

# ---------- Ensure directories & files exist ----------
def ensure_files():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)

    for p in [DATA_TICKETS, DATA_KNOWLEDGE, DATA_FEEDBACK]:
        if not os.path.exists(p):
            with open(p, "w", encoding="utf-8") as f:
                json.dump([], f)

    if not os.path.exists(PREDICT_LOG):
        with open(PREDICT_LOG, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "ticket_id", "description", "recommended_ids"])

    if not os.path.exists(SYSTEM_LOG):
        open(SYSTEM_LOG, "a", encoding="utf-8").close()

    if not os.path.exists(ALERTS_LOG):
        with open(ALERTS_LOG, "w", encoding="utf-8") as f:
            json.dump([], f)

    if not os.path.exists(COVERAGE_REPORT_CSV):
        with open(COVERAGE_REPORT_CSV, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["article_id", "impressions", "clicks", "ctr"])

ensure_files()

# ---------- Helpers ----------
def load_json(path: str):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_json(path: str, data):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def append_predict_log(ticket_id: str, description: str, recommended_ids: List[str]):
    with open(PREDICT_LOG, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.utcnow().isoformat(), ticket_id or "", description, json.dumps(recommended_ids)])

def log_system(message: str):
    with open(SYSTEM_LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.utcnow().isoformat()} {message}\n")

def log_alert(message: str):
    alerts = []
    if os.path.exists(ALERTS_LOG):
        try:
            with open(ALERTS_LOG, "r", encoding="utf-8") as f:
                alerts = json.load(f)
        except json.JSONDecodeError:
            alerts = []

    new_alert = {"timestamp": datetime.utcnow().isoformat(), "message": message}
    alerts.append(new_alert)
    with open(ALERTS_LOG, "w", encoding="utf-8") as f:
        json.dump(alerts, f, indent=2)

    sent_to_slack = False
    try:
        if SLACK_WEBHOOK_URL:
            payload = {"text": f"🚨 *AI Monitoring Alert* 🚨\n{message}"}
            resp = requests.post(SLACK_WEBHOOK_URL, json=payload)

            if resp.status_code == 200:
                # remove alert after successful send
                updated_alerts = [a for a in alerts if a["message"] != message]
                with open(ALERTS_LOG, "w", encoding="utf-8") as f:
                    json.dump(updated_alerts, f, indent=2)
                sent_to_slack = True
    except Exception as e:
        print("Slack send failed:", e)

    return {"message": message, "sent_to_slack": sent_to_slack}
# ---------- Health ----------
@app.get("/")
def health():
    return {"message": "AI Ticket Resolution API — running"}

# ---------- Ticket Management ----------
@app.post("/api/tickets", response_model=Ticket)
def create_ticket(ticket: TicketCreate):
    if not ticket.customer_name or len(ticket.customer_name.strip()) < 2:
        raise HTTPException(status_code=400, detail="customer_name must be at least 2 characters")
    if not ticket.title or len(ticket.title.strip()) < 3:
        raise HTTPException(status_code=400, detail="title must be at least 3 characters")
    if not ticket.description or len(ticket.description.strip()) < 5:
        raise HTTPException(status_code=400, detail="description must be at least 5 characters")

    tickets = load_json(DATA_TICKETS)
    kb = load_json(DATA_KNOWLEDGE)

    new = ticket.dict()
    new["id"] = f"t_{len(tickets)+1}"
    new["status"] = "open"
    new["createdAt"] = datetime.utcnow().isoformat()

    try:
        new["category"] = classify_category(new["description"])
    except Exception:
        new["category"] = "Other"
    try:
        new["tags"] = generate_tags_with_llama(new["description"])
    except Exception:
        new["tags"] = []

    try:
        recs = recommend_articles(new["description"], kb, top_k=1, category=new.get("category"))
    except Exception:
        recs = []

    new["recommendedArticleIds"] = [str(r) for r in recs] if recs else []
    tickets.append(new)
    save_json(DATA_TICKETS, tickets)
    append_predict_log(new["id"], new["description"], new["recommendedArticleIds"])
    return new

@app.get("/api/tickets")
def list_tickets():
    return load_json(DATA_TICKETS)

@app.patch("/api/tickets/{ticket_id}")
def update_ticket(ticket_id: str, data: Dict[str, Any] = Body(...)):
    tickets = load_json(DATA_TICKETS)
    for t in tickets:
        if t.get("id") == ticket_id:
            t["status"] = data.get("status", t["status"])
            t["updatedAt"] = datetime.utcnow().isoformat()
            save_json(DATA_TICKETS, tickets)
            return t
    raise HTTPException(status_code=404, detail="Ticket not found")

# ---------- Knowledge Base ----------
@app.get("/api/knowledge")
def list_knowledge():
    return load_json(DATA_KNOWLEDGE)

@app.post("/api/knowledge")
def add_knowledge(article: KnowledgeCreate):
    kb = load_json(DATA_KNOWLEDGE)
    art = article.dict()
    art["id"] = f"art_{len(kb)+1}"
    art["category"] = classify_category(art.get("title", ""))
    art["tags"] = generate_tags_with_llama(art.get("content", ""))
    art["embedding"] = get_embedding(art.get("title", "") + " " + art.get("content", ""))
    kb.append(art)
    save_json(DATA_KNOWLEDGE, kb)
    return {"message": "Article added", "article": art}

# ---------- Prediction ----------
@app.post("/api/predict")
def predict(payload: Dict[str, Any]):
    desc = payload.get("description")
    if not desc:
        raise HTTPException(status_code=400, detail="description required")

    kb = load_json(DATA_KNOWLEDGE)
    ids_scores = recommend_articles(desc, kb, top_k=3, return_scores=True)
    rec_ids = [str(r[0]) for r in ids_scores]
    append_predict_log("", desc, rec_ids)

    results = []
    for art_id, score in ids_scores:
        art = next((a for a in kb if a["id"] == art_id), None)
        if art:
            results.append({
                "id": art_id,
                "title": art["title"],
                "score": round(float(score), 3),
                "snippet": art["content"][:200] + "..."
            })
    return {"query": desc, "results": results}

# ---------- Feedback & Stats ----------
@app.post("/api/feedback")
def submit_feedback(entry: Dict[str, Any]):
    fb = load_json(DATA_FEEDBACK)

    if "article_id" not in entry or "correct" not in entry:
        raise HTTPException(status_code=400, detail="article_id and correct are required")

    # 🟢 Check for existing feedback for this ticket_id + article_id
    existing_index = next(
        (i for i, f in enumerate(fb)
         if f.get("ticket_id") == entry.get("ticket_id")
         and f.get("article_id") == entry["article_id"]),
        None
    )

    new_feedback = {
        "id": f"fb_{len(fb)+1}" if existing_index is None else fb[existing_index]["id"],
        "ticket_id": entry.get("ticket_id"),
        "article_id": entry["article_id"],
        "correct": bool(entry["correct"]),
        "notes": entry.get("notes", ""),
        "timestamp": datetime.utcnow().isoformat()
    }

    if existing_index is not None:
        # 🟡 Overwrite previous feedback (update existing entry)
        fb[existing_index] = new_feedback
    else:
        # 🟢 New feedback
        fb.append(new_feedback)

    save_json(DATA_FEEDBACK, fb)
    log_system(f"Feedback recorded/updated: {new_feedback}")

    # --- Accuracy calculation ---
    total = len(fb)
    correct = sum(1 for f in fb if f.get("correct"))
    accuracy = round((correct / total) * 100, 2) if total else 0

    if accuracy < 60:
        log_alert(f"⚠️ Accuracy dropped to {accuracy}% — please review recommendations!")

    return {"feedback": new_feedback, "metrics": {"accuracy": accuracy}}


# ---------- Alerts ----------
@app.get("/api/alerts")
def get_alerts():
    if not os.path.exists(ALERTS_LOG):
        with open(ALERTS_LOG, "w", encoding="utf-8") as f:
            json.dump([], f)
    with open(ALERTS_LOG, "r", encoding="utf-8") as f:
        try:
            alerts = json.load(f)
        except json.JSONDecodeError:
            alerts = []
    return {"alerts": sorted(alerts, key=lambda x: x["timestamp"], reverse=True)}

@app.post("/api/alerts/delete")
def delete_alert(payload: Dict[str, Any]):
    index = payload.get("index")
    alerts = load_json(ALERTS_LOG)

    if index is not None and 0 <= index < len(alerts):
        removed = alerts.pop(index)
        save_json(ALERTS_LOG, alerts)
        return {"success": True, "deleted": removed}
    return {"success": False, "error": "Invalid index"}


@app.post("/api/delete_alert")
def delete_alert(data: Dict[str, Any]):
    timestamp = data.get("timestamp")
    if not timestamp:
        raise HTTPException(status_code=400, detail="timestamp required")

    alerts = load_json(ALERTS_LOG)
    updated_alerts = [a for a in alerts if a.get("timestamp") != timestamp]
    save_json(ALERTS_LOG, updated_alerts)

    return {"message": "Alert deleted", "remaining": len(updated_alerts)}


@app.post("/api/trigger_alert")
def trigger_alert(data: Dict[str, Any]):
    msg = data.get("message", "Manual alert triggered")
    log_alert(msg)
    send_slack_message(msg)
    return {"message": "Alert logged & sent to Slack", "alert": msg}

# ---------- Analytics ----------
@app.get("/api/analytics")
def get_analytics():
    kb = load_json(DATA_KNOWLEDGE)
    tickets = load_json(DATA_TICKETS)
    fb = load_json(DATA_FEEDBACK)

    impressions = {}
    if os.path.exists(PREDICT_LOG):
        with open(PREDICT_LOG, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    recs = json.loads(row.get("recommended_ids") or "[]")
                except:
                    recs = []
                for rid in recs:
                    impressions[str(rid)] = impressions.get(str(rid), 0) + 1

    clicks = {}
    for entry in fb:
        if entry.get("correct"):
            aid = str(entry.get("article_id"))
            clicks[aid] = clicks.get(aid, 0) + 1

    total_tickets = len(tickets)
    tickets_with_recs = sum(1 for t in tickets if t.get("recommendedArticleIds"))
    coverage = round((tickets_with_recs / total_tickets) * 100, 2) if total_tickets else 0

    recommended_tickets = [t for t in tickets if t.get("recommendedArticleIds")]
    resolved_with_recs = sum(1 for t in recommended_tickets if t.get("status") in ("resolved", "closed"))
    resolution_rate = round((resolved_with_recs / len(recommended_tickets)) * 100, 2) if recommended_tickets else 0

    summary = {
        "total_articles": len(kb),
        "total_tickets": total_tickets,
        "tickets_with_recommendations": tickets_with_recs,
        "coverage_percent": coverage,
        "resolution_rate_percent": resolution_rate,
        "total_feedback": len(fb)
    }

    return {"summary": summary}

# ---------- Admin Dataset Evaluation ----------
@app.post("/api/admin/evaluate_dataset")
def admin_evaluate_dataset(payload: Dict[str, Any]):
    path = payload.get("dataset_path")
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=400, detail="dataset_path missing or not found")
    kb = load_json(DATA_KNOWLEDGE)
    return evaluate_dataset_file(path, kb, top_k=1)
