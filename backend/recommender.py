# recommender.py — Final Optimized Version for E-commerce Ticket Recommendation

import os
import json
import numpy as np
import requests
import spacy
import re
from typing import List, Dict
from dotenv import load_dotenv
from prompt_templates import TAG_PROMPT, CATEGORY_PROMPT

# ---------- Initialization ----------
load_dotenv()
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = spacy.blank("en")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# ---------- Text Preprocessing ----------
def preprocess_text(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize_text(text: str) -> List[str]:
    if not nlp:
        return text.split()
    doc = nlp(text)
    return [t.lemma_ for t in doc if not t.is_stop and not t.is_punct]

# ---------- Embeddings ----------
def get_embedding(text: str) -> List[float]:
    np.random.seed(abs(hash(text)) % (10**6))
    emb = np.random.rand(256)
    return (emb / np.linalg.norm(emb)).tolist()

def cosine_similarity(a, b):
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)
    if not a.size or not b.size:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

# ---------- Groq LLM (optional) ----------
def call_groq_llm(prompt: str) -> str:
    if not GROQ_API_KEY:
        return "LLM not configured"
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,
            },
            timeout=30,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("⚠️ call_groq_llm failed:", e)
        return "LLM error"

# ---------- Tags & Category ----------
def generate_tags_with_llama(text: str) -> List[str]:
    try:
        out = call_groq_llm(TAG_PROMPT.format(text=text))
        out = out.replace("\n", " ").replace("Tags:", "").strip()
        tags = re.split(r"[\n,•\-]\s*", out)
        tags = [t.strip(" .").lower() for t in tags if len(t.strip()) > 1][:3]
        return tags or ["support", "help", "order"]
    except Exception:
        return ["support", "help", "order"]

def classify_category(text: str) -> str:
    """Classify ticket category using rules and LLM fallback."""
    text = text.lower()

    # --- Rule-based detection for e-commerce tickets ---
    if any(k in text for k in ["refund", "return", "exchange", "replacement", "damaged", "defective", "wrong item", "incorrect product"]):
        return "Product"
    if any(k in text for k in ["delivery", "delay", "courier", "tracking", "dispatched", "not received", "late", "order status"]):
        return "Shipping"
    if any(k in text for k in ["payment", "invoice", "charged", "credit card", "billing", "transaction", "failed payment"]):
        return "Billing"

    # --- Fallback: LLM classification ---
    if GROQ_API_KEY:
        try:
            resp = call_groq_llm(CATEGORY_PROMPT.format(text=text))
            category = resp.split("\n")[0].replace("Category:", "").strip().title()
            valid = ["Billing", "Account", "Technical", "Product", "Other", "Shipping"]
            for v in valid:
                if v.lower() in category.lower():
                    return v
        except Exception:
            pass

    return "Other"

# ---------- Text Similarity ----------
def simple_score(query: str, text: str) -> float:
    q = set(preprocess_text(query).split())
    t = set(preprocess_text(text).split())
    return len(q & t) / (len(q) + 1e-6)

# ---------- Recommendation Engine ----------
def recommend_articles(query: str, articles: List[Dict], top_k: int = 1, category: str = None, return_scores: bool = False):
    query_emb = get_embedding(query)
    query_lower = preprocess_text(query)
    scored = []

    # --- Intent Detection ---
    intent_groups = {
        "refund": {"refund", "return", "replacement", "exchange", "damaged", "broken", "defective", "replace", "wrong item"},
        "shipping": {"delivery", "delayed", "delay", "not received", "shipped", "courier", "tracking", "dispatch", "order delay"},
        "billing": {"payment", "invoice", "card", "failed", "charged", "chargeback", "transaction"},
        "product": {"size", "color", "feature", "quality", "stock", "availability", "out of stock"},
    }

    detected_intents = set()
    for intent, keywords in intent_groups.items():
        for kw in keywords:
            if kw in query_lower:
                detected_intents.add(intent)

    # --- Filter Knowledge Base by Category (if exists) ---
    filtered = [
        art for art in articles
        if not category or category.lower() in art.get("category", "other").lower()
    ]
    if not filtered:
        filtered = articles

    # --- Compute Scores ---
    for art in filtered:
        content = preprocess_text(art.get("title", "") + " " + art.get("content", ""))
        emb = art.get("embedding", [])
        emb_score = cosine_similarity(query_emb, emb) if emb else 0.0
        text_score = simple_score(query, content)

        # --- Intent-based Boosts ---
        boost = 0.0
        if "shipping" in detected_intents and any(k in content for k in ["delivery", "tracking", "delay", "dispatched", "order status"]):
            boost += 0.35
        if "refund" in detected_intents and any(k in content for k in ["refund", "return", "replace", "exchange", "damaged"]):
            boost += 0.3
        if "billing" in detected_intents and any(k in content for k in ["payment", "billing", "card", "charge", "invoice"]):
            boost += 0.25
        if "product" in detected_intents and any(k in content for k in ["product", "size", "color", "quality", "stock"]):
            boost += 0.15

        # --- Final Weighted Score ---
        score = (emb_score * 0.4) + (text_score * 0.5) + boost
        scored.append((art.get("id"), round(score, 3)))

    # --- Fallback ---
    if not scored and articles:
        for art in articles:
            content = preprocess_text(art.get("title", "") + " " + art.get("content", ""))
            emb = art.get("embedding", [])
            emb_score = cosine_similarity(query_emb, emb) if emb else 0.0
            text_score = simple_score(query, content)
            score = (emb_score * 0.3) + (text_score * 0.7)
            scored.append((art.get("id"), round(score, 3)))

    # --- Sort & Return ---
    scored.sort(key=lambda x: x[1], reverse=True)
    if return_scores:
        return scored[:top_k]
    return [a[0] for a in scored[:top_k]]
