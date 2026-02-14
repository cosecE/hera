import os
import anthropic
import json

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# -----------------------
# Nudge Generator
# -----------------------

def generate_nudge(input_payload):
    baseline = input_payload["baseline"]
    current = input_payload["current"]
    delta = input_payload["delta"]

    prompt = f"""
You are an expert Child Psychologist and AI Behavioral Analyst.

Baseline:
Screen time: {baseline["screen_time"]}
Late night: {baseline["late_night_minutes"]}
Social time: {baseline["social_time"]}

Current:
Screen time: {current["screen_time"]}
Late night: {current["late_night_minutes"]}
Social time: {current["social_time"]}

Changes:
Screen delta: {delta["screen_time_change"]}
Late night delta: {delta["late_night_change"]}
Social delta: {delta["social_time_change"]}

Return JSON:
{{
  "core_emotional_need": "...",
  "empathy_nudge": "...",
  "conversation_starter": "..."
}}
"""

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text

    try:
        return json.loads(text)
    except:
        return {"raw_output": text}


# -----------------------
# Practice Mode - Rewrite
# -----------------------

def rewrite_parent_response(parent_text):
    prompt = f"""
Rewrite this parent message to be warm, curious, and non-judgmental:

"{parent_text}"

Return JSON:
{{
  "improved_response": "..."
}}
"""

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text

    try:
        return json.loads(text)
    except:
        return {"improved_response": text}


# -----------------------
# Practice Mode - Roleplay
# -----------------------

def roleplay_child_response(parent_text):
    prompt = f"""
You are a realistic teenager.

Respond to:
"{parent_text}"

Keep it emotionally authentic and short.
"""

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text
