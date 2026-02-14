import os
import anthropic
import json

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

def generate_nudge(input_payload):
    risk = input_payload["risk_level"]
    baseline = input_payload["baseline"]
    current = input_payload["current"]
    delta = input_payload["delta"]

    prompt = f"""
You are an expert Child Psychologist and AI Behavioral Analyst.

You are given:
Risk Level: {risk}

Baseline behavior:
- Screen time: {baseline["screen_time"]} hours/day
- Late night usage: {baseline["late_night_minutes"]} minutes
- Social app time: {baseline["social_time"]} hours/day

Current behavior:
- Screen time: {current["screen_time"]} hours/day
- Late night usage: {current["late_night_minutes"]} minutes
- Social app time: {current["social_time"]} hours/day

Behavioral change:
- Screen time change: {delta["screen_time_change"]} hours
- Late night change: {delta["late_night_change"]} minutes
- Social time change: {delta["social_time_change"]} hours

Your tasks:
1. Identify the core emotional need.
2. Generate a 2-sentence empathy nudge.
3. Provide a short conversation starter.

Rules:
- Do NOT diagnose.
- Do NOT suggest punishment or surveillance.
- Keep tone warm, calm, and supportive.

Return JSON only:
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

#added new   
def rewrite_parent_response(parent_text):
    prompt = f"""
You are a child psychologist coaching a parent.

The parent said:
"{parent_text}"

This phrasing may feel confrontational or invalidating.

Rewrite it to:
- Reduce judgment
- Increase warmth
- Increase curiosity
- Keep it concise
- Do not shame the parent

Return JSON only:
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


def roleplay_child_response(parent_text):
    prompt = f"""
You are roleplaying a teenager responding to a parent.

The parent says:
"{parent_text}"

Respond as a realistic teen might respond.
Keep it short and emotionally authentic.
Do not escalate unnecessarily.
"""

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text


if __name__ == "__main__":
    test_input = {
        "risk_level": "Warning",
        "baseline": {
            "screen_time": 4.0,
            "late_night_minutes": 10,
            "social_time": 2.1
        },
        "current": {
            "screen_time": 7.8,
            "late_night_minutes": 140,
            "social_time": 0.4
        },
        "delta": {
            "screen_time_change": 3.8,
            "late_night_change": 130,
            "social_time_change": -1.7
        }
    }

    result = generate_nudge(test_input)
    print(json.dumps(result, indent=2))



#     - tracking certain patterns, seasonal depression, adhd symptoms, etc. and then providing more personalized nudges based on those patterns.
# -resolution part where they followed up 
