# evaluator.py
from typing import List, Dict
import json
from recommender import recommend_articles

def compute_metrics_from_feedback(feedback: List[Dict]) -> Dict:
    """
    Compute simple precision/recall/F1 from stored feedback entries.

    feedback: list of {"article_id": "...", "correct": bool}
    Precision = TP / (TP + FP)
    Recall (pseudo) = TP / total_feedback_count
    F1 = harmonic mean
    """
    if not feedback:
        return {}

    tp = sum(1 for f in feedback if f.get("correct") is True)
    fp = sum(1 for f in feedback if f.get("correct") is False)
    total = len(feedback)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / total if total > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "count_feedback": total,
        "true_positives": tp,
        "false_positives": fp,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4)
    }

def evaluate_dataset_file(dataset_path: str, kb: List[Dict], top_k: int = 1) -> Dict:
    """
    Evaluate recommender on labeled dataset:
    dataset: list of {"description": "...", "ground_truth_article_id": "art_5"}
    Returns aggregated metrics + per-item details.
    """
    with open(dataset_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = len(data)
    tp = 0
    fp = 0
    fn = 0
    details = []

    for rec in data:
        desc = rec.get("description", "")
        gt = rec.get("ground_truth_article_id")
        preds_with_scores = recommend_articles(desc, kb, top_k=top_k, return_scores=True)
        preds = [p[0] for p in preds_with_scores] if preds_with_scores else []
        hit = gt in preds
        if hit:
            tp += 1
        else:
            fn += 1
            if preds:
                fp += 1

        details.append({
            "description": desc,
            "ground_truth": gt,
            "preds": preds,
            "hit": hit
        })

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "count": total,
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "details": details
    }
