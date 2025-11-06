# backend/prompt_templates.py
"""
Central place to define all prompt templates for the LLM.
"""

TAG_PROMPT = """
You are a smart support assistant. 
Given the following customer issue, extract exactly 3 short and relevant tags (1–3 words each).

Issue:
"{text}"

Respond only with a JSON list of tags, like:
["login issue", "password reset", "account access"]
"""

CATEGORY_PROMPT = """
You are a classifier for customer support tickets. 
Given this issue description, classify it into one of these categories:
["Billing", "Account", "Technical", "Product", "Other"]

Issue:
"{text}"

Respond only with the category name.
"""
