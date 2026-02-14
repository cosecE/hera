import requests

WHITE_CIRCLE_API_KEY = "wc-84c153b2d35476ab4e32b652a40b3a58"
WHITE_CIRCLE_URL = "https://us.whitecircle.ai/api/session/check"
WHITE_CIRCLE_DEPLOYMENT_ID = "455439b6-aec6-4198-a639-23441f32e8f8"


def classify_behavior(user_messages: list):
    """
    Sends messages to White Circle session check endpoint.
    Returns normalized Anchor risk format.
    """

    headers = {
        "Authorization": f"Bearer {WHITE_CIRCLE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "deployment_id": WHITE_CIRCLE_DEPLOYMENT_ID,
        "external_session_id": "anchor-session-001",
        "include_context": False,
        "messages": user_messages
    }

    try:
        response = requests.post(
            WHITE_CIRCLE_URL,
            headers=headers,
            json=payload,
            timeout=10
        )

        response.raise_for_status()
        raw = response.json()

        return normalize_response(raw)

    except Exception as e:
        print("White Circle API Error:", e)
        return fallback_response()


def normalize_response(raw: dict):
    """
    Map White Circle response into Anchor risk structure.
    NOTE: You must adjust keys below to match actual response structure.
    """

   
    risk_score = raw.get("risk_score", 0)
    risk_category = raw.get("risk_category", "Low")
    patterns = raw.get("flags", [])
    volatility_index = raw.get("volatility_index", 0.0)

    return {
        "risk_score": risk_score,
        "risk_category": risk_category,
        "patterns": patterns,
        "volatility_index": volatility_index,
        "message_frequency": len(raw.get("messages", [])),
        "confidence": raw.get("confidence", 0.0)
    }


def fallback_response():
    return {
        "risk_score": 0,
        "risk_category": "Low",
        "patterns": [],
        "volatility_index": 0.0,
        "message_frequency": 0,
        "confidence": 0.0
    }

def evaluate_parent_text(parent_text: str):
    """
    Sends a single parent message to White Circle
    Returns moderation result (flagged or not).
    """

    headers = {
        "Authorization": f"Bearer {WHITE_CIRCLE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "deployment_id": WHITE_CIRCLE_DEPLOYMENT_ID,
        "external_session_id": "practice-mode-session",
        "include_context": False,
        "messages": [
            {"role": "user", "content": parent_text}
        ]
    }

    try:
        response = requests.post(
            WHITE_CIRCLE_URL,
            headers=headers,
            json=payload,
            timeout=10
        )

        response.raise_for_status()
        raw = response.json()

        # Return raw moderation result
        return raw

    except Exception as e:
        print("White Circle Practice Mode Error:", e)
        return {"flagged": False}
