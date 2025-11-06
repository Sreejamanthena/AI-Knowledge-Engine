# alerts_scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import time
import os
import json
from gap_analysis import compute_and_write_reports

ALERTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "alerts.log")

# thresholds
MIN_COVERAGE = 70.0  # percent
MIN_CTR = 10.0  # percent

def check_and_alert():
    try:
        result = compute_and_write_reports()
        summary = result.get("summary", {})
        low_ctr = result.get("low_ctr", [])

        alerts = []
        if summary.get("coverage_percent", 100) < MIN_COVERAGE:
            alerts.append(f"Low coverage: {summary.get('coverage_percent')}%")

        if len(low_ctr) > 0:
            alerts.append(f"{len(low_ctr)} low-CTR articles (CTR < {MIN_CTR}%)")

        # write to alerts log
        if alerts:
            with open(ALERTS_FILE, "a", encoding="utf-8") as f:
                f.write(f"{datetime.utcnow().isoformat()} ALERTS: {json.dumps(alerts)}\n")
        else:
            # record healthy status
            with open(ALERTS_FILE, "a", encoding="utf-8") as f:
                f.write(f"{datetime.utcnow().isoformat()} OK: No alerts\n")
    except Exception as e:
        with open(ALERTS_FILE, "a", encoding="utf-8") as f:
            f.write(f"{datetime.utcnow().isoformat()} ERROR running checks: {e}\n")

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    # run every 24 hours; for testing you may use 'interval' with seconds=60
    scheduler.add_job(check_and_alert, "interval", hours=24, next_run_time=datetime.utcnow())
    scheduler.start()
    print("Alerts scheduler started. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Scheduler stopped.")
