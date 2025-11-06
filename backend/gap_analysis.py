# gap_analysis.py
import os
import json
from datetime import datetime, date
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

DATA_TICKETS = os.path.join(DATA_DIR, "tickets.json")
DATA_KNOWLEDGE = os.path.join(DATA_DIR, "knowledge.json")
DATA_FEEDBACK = os.path.join(DATA_DIR, "feedback.json")
PREDICT_LOG = os.path.join(LOGS_DIR, "recommendation_logs.csv")
COVERAGE_REPORT_CSV = os.path.join(REPORTS_DIR, "coverage_report.csv")
DAILY_SUMMARY_TEMPLATE = os.path.join(REPORTS_DIR, "daily_summary_{}.json")
ALERTS_LOG = os.path.join(LOGS_DIR, "alerts.log")

def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []

def compute_and_write_reports():
    kb = load_json(DATA_KNOWLEDGE)
    tickets = load_json(DATA_TICKETS)
    fb = load_json(DATA_FEEDBACK)

    # impressions
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

    # clicks
    clicks = {}
    for entry in fb:
        if entry.get("correct") is True:
            aid = str(entry.get("article_id"))
            clicks[aid] = clicks.get(aid, 0) + 1

    per_article = []
    all_ids = [str(a.get("id")) for a in kb]
    for aid in all_ids:
        imp = impressions.get(aid, 0)
        clk = clicks.get(aid, 0)
        ctr = round((clk / imp) * 100, 2) if imp > 0 else 0.0
        per_article.append({"article_id": aid, "title": next((a.get("title") for a in kb if str(a.get("id")) == aid), None), "impressions": imp, "clicks": clk, "ctr": ctr})

    # write coverage report CSV
    with open(COVERAGE_REPORT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["article_id", "title", "impressions", "clicks", "ctr"])
        for a in per_article:
            writer.writerow([a["article_id"], a["title"], a["impressions"], a["clicks"], a["ctr"]])

    # summary
    total_tickets = len(tickets)
    tickets_with_recs = sum(1 for t in tickets if t.get("recommendedArticleIds"))
    coverage = round((tickets_with_recs / total_tickets) * 100, 2) if total_tickets > 0 else 0.0
    recommended_tickets = [t for t in tickets if t.get("recommendedArticleIds")]
    if recommended_tickets:
        resolved_with_recs = sum(1 for t in recommended_tickets if t.get("status") in ("resolved", "closed"))
        resolution_rate = round((resolved_with_recs / len(recommended_tickets)) * 100, 2)
    else:
        resolution_rate = 0.0

    summary = {
        "date": datetime.utcnow().isoformat(),
        "total_articles": len(all_ids),
        "total_tickets": total_tickets,
        "tickets_with_recommendations": tickets_with_recs,
        "coverage_percent": coverage,
        "resolution_rate_percent": resolution_rate,
        "total_feedback": len(fb)
    }

    # write daily summary JSON
    filename = DAILY_SUMMARY_TEMPLATE.format(datetime.utcnow().strftime("%Y-%m-%d"))
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "per_article": per_article}, f, indent=2)

    # identify low CTR
    low_ctr = [a for a in per_article if a["impressions"] > 0 and a["ctr"] < 10.0]

    # write low ctr file
    low_ctr_file = os.path.join(REPORTS_DIR, "low_ctr_{}.json".format(datetime.utcnow().strftime("%Y-%m-%d")))
    with open(low_ctr_file, "w", encoding="utf-8") as f:
        json.dump({"low_ctr": low_ctr}, f, indent=2)

    # log summary
    with open(ALERTS_LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.utcnow().isoformat()} GAP_ANALYSIS summary coverage={coverage} resolution_rate={resolution_rate} low_ctr_count={len(low_ctr)}\n")

    return {"summary": summary, "low_ctr": low_ctr, "per_article_count": len(per_article)}

if __name__ == "__main__":
    r = compute_and_write_reports()
    print("Gap analysis complete:", r)
