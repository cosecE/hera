import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from claude_module import generate_nudge
import requests
from white_circle import evaluate_parent_text
import os


mock_scenarios = [
    (
        "Stable routine",
        {
            "baseline": {"screen_time": 4.5, "late_night_minutes": 15, "social_time": 2.5},
            "current": {"screen_time": 4.8, "late_night_minutes": 18, "social_time": 2.7},
            "delta": {"screen_time_change": 0.3, "late_night_change": 3, "social_time_change": 0.2}
        }
    ),
    (
        "Slight increase in screen time",
        {
            "baseline": {"screen_time": 4.0, "late_night_minutes": 20, "social_time": 2.0},
            "current": {"screen_time": 5.2, "late_night_minutes": 25, "social_time": 2.1},
            "delta": {"screen_time_change": 1.2, "late_night_change": 5, "social_time_change": 0.1}
        }
    ),
    (
        "Social withdrawal",
        {
            "baseline": {"screen_time": 5.0, "late_night_minutes": 30, "social_time": 3.0},
            "current": {"screen_time": 5.5, "late_night_minutes": 35, "social_time": 1.2},
            "delta": {"screen_time_change": 0.5, "late_night_change": 5, "social_time_change": -1.8}
        }
    ),
    (
        "Heavy late-night usage spike",
        {
            "baseline": {"screen_time": 4.5, "late_night_minutes": 20, "social_time": 2.2},
            "current": {"screen_time": 6.5, "late_night_minutes": 120, "social_time": 2.0},
            "delta": {"screen_time_change": 2.0, "late_night_change": 100, "social_time_change": -0.2}
        }
    ),
    (
        "Sudden digital isolation",
        {
            "baseline": {"screen_time": 5.5, "late_night_minutes": 40, "social_time": 3.5},
            "current": {"screen_time": 3.2, "late_night_minutes": 10, "social_time": 0.8},
            "delta": {"screen_time_change": -2.3, "late_night_change": -30, "social_time_change": -2.7}
        }
    ),
    (
        "Gaming binge period",
        {
            "baseline": {"screen_time": 4.0, "late_night_minutes": 20, "social_time": 1.8},
            "current": {"screen_time": 8.5, "late_night_minutes": 90, "social_time": 1.5},
            "delta": {"screen_time_change": 4.5, "late_night_change": 70, "social_time_change": -0.3}
        }
    ),
    (
        "Academic crunch (more screen, less social)",
        {
            "baseline": {"screen_time": 4.8, "late_night_minutes": 25, "social_time": 2.6},
            "current": {"screen_time": 7.0, "late_night_minutes": 60, "social_time": 1.2},
            "delta": {"screen_time_change": 2.2, "late_night_change": 35, "social_time_change": -1.4}
        }
    ),
    (
        "Major concern pattern",
        {
            "baseline": {"screen_time": 4.0, "late_night_minutes": 20, "social_time": 2.5},
            "current": {"screen_time": 9.5, "late_night_minutes": 180, "social_time": 0.6},
            "delta": {"screen_time_change": 5.5, "late_night_change": 160, "social_time_change": -1.9}
        }
    )
]


scenario_names = [s[0] for s in mock_scenarios]

selected_name = st.selectbox(
    "Choose behavior scenario",
    scenario_names
)
selected_input = next(
    data for name, data in mock_scenarios if name == selected_name
)


def generate_safety_alerts(data):
    alerts = []

    baseline = data["baseline"]
    current = data["current"]
    delta = data["delta"]

    # Late-night spike
    if delta["late_night_change"] > 60:
        alerts.append("Late-night phone usage has increased significantly.")

    # Screen time spike
    if delta["screen_time_change"] > 2:
        alerts.append("Daily screen time is much higher than usual.")

    # Social withdrawal
    if delta["social_time_change"] < -1:
        alerts.append("Social app engagement has dropped noticeably.")

    # Social spike (possible conflict/drama)
    if delta["social_time_change"] > 2:
        alerts.append("Sudden increase in social activity detected.")

    # No alerts
    if not alerts:
        alerts.append("No major behavior shifts detected.")

    return alerts

WHITE_CIRCLE_API_KEY = os.getenv("wc-84c153b2d35476ab4e32b652a40b3a58")
WHITE_CIRCLE_URL = "https://us.whitecircle.ai/api/session/check"
WHITE_CIRCLE_DEPLOYMENT_ID = "455439b6-aec6-4198-a639-23441f32e8f8"



st.markdown(
    """
    <style>
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a, #1e293b);
        color: white;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Sidebar title */
    .sidebar-title {
        font-size: 22px;
        font-weight: 600;
        padding: 10px 0 20px 0;
    }

    /* Card styling */
    .card {
        background: #ffffff;
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
        text-align: center;
        color: #111111;   /* force readable text */
    }


    /* Main title styling */
    .main-title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 16px;
        color: #666;
        margin-bottom: 30px;
    }

    /* Center container */
    .center-container {
        text-align: center;
        margin-top: 40px;
    }

    /* Orb styling */
    .orb {
        width: 180px;
        height: 180px;
        margin: 30px auto;
        border-radius: 50%;
        background: radial-gradient(circle at 30% 30%, #ffffff, var(--orb-color));
        box-shadow:
            0 0 40px var(--orb-glow),
            0 0 80px var(--orb-glow);
        animation: pulse 3.5s ease-in-out infinite;
    }

    /* Gentle pulsing animation */
    @keyframes pulse {
        0% {
            transform: scale(1);
            box-shadow:
                0 0 30px var(--orb-glow),
                0 0 60px var(--orb-glow);
        }
        50% {
            transform: scale(1.05);
            box-shadow:
                0 0 50px var(--orb-glow),
                0 0 100px var(--orb-glow);
        }
        100% {
            transform: scale(1);
            box-shadow:
                0 0 30px var(--orb-glow),
                0 0 60px var(--orb-glow);
        }
    }


    /* Status text */
    .status-text {
        font-size: 20px;
        font-weight: 600;
        margin-top: 10px;
    }



    </style>
    """,
    unsafe_allow_html=True
)


st.set_page_config(page_title="Hera", layout="wide")

# ---------------------------
# Sidebar navigation
# ---------------------------
with st.sidebar:
    st.markdown(
        '<div class="sidebar-title">HERA</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        ["Family Health Score", "Nudge Center", "Practice Mode"],
        label_visibility="collapsed"
    )




# Store AI results in session state
if "nudge_result" not in st.session_state:
    st.session_state.nudge_result = None

# ---------------------------
# Page 1: Family Health Score
# ---------------------------
if page == "Family Health Score":

    baseline = selected_input["baseline"]
    current = selected_input["current"]

    # Sleep score (based on late-night minutes)
    late_night = current["late_night_minutes"]
    sleep_score = max(0, 100 - late_night * 0.5)

    # Social score (compare to baseline)
    social_ratio = current["social_time"] / baseline["social_time"]
    social_score = max(0, min(100, int(social_ratio * 100)))

    # Screen balance score
    screen_ratio = current["screen_time"] / baseline["screen_time"]
    screen_score = max(0, min(100, int(100 - (screen_ratio - 1) * 50)))


    overall = int((sleep_score + social_score + screen_score) / 3)

    # Determine status and colors
    if overall >= 75:
        status = "Steady"
        orb_color = "#6EE7B7"   # soft green
        glow = "rgba(110,231,183,0.6)"
    elif overall >= 60:
        status = "Active"
        orb_color = "#FBBF24"   # warm amber
        glow = "rgba(251,191,36,0.6)"
    else:
        status = "Clouded"
        orb_color = "#A78BFA"   # soft purple
        glow = "rgba(167,139,250,0.6)"



    # Page title
    st.markdown(
        """
        <div class="center-container">
            <div style="font-size:48px; font-weight:700; letter-spacing:3px;">
                HERA
            </div>
            <div style="color:#888; margin-top:5px;">
                Digital safety, grounded.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Orb
    st.markdown(
        f"""
        <div class="center-container">
            <div class="orb"
                style="
                    --orb-color: {orb_color};
                    --orb-glow: {glow};
                ">
            </div>
            <div class="status-text" style="color:{orb_color};">
                {status}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Small explanatory text
    st.markdown(
        """
        <div class="center-container" style="color:#888; font-size:14px;">
            Based on sleep rhythm, social media engagement, and screen balance.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # Secondary metrics (optional)
    def ring(label, value, description):
        if value >= 70:
            color = "#6EE7B7"
        elif value >= 50:
            color = "#FBBF24"
        else:
            color = "#A78BFA"

        # Create a circular progress chart using matplotlib
        fig, ax = plt.subplots()
        ax.pie(
            [value, 100 - value],
            colors=[color, "#E5E7EB"],
            startangle=90,
            counterclock=False,
            wedgeprops=dict(width=0.35)
        )

        ax.text(0, 0, f"{value}", ha="center", va="center", fontsize=16, fontweight="bold")
        ax.axis("equal")

        st.pyplot(fig)

        st.markdown(f"**{label}**")
        st.caption(description)

    st.divider()

    col1, col2, col3 = st.columns(3)


    with col1:
        ring(
            "Sleep Rhythm",
            sleep_score,
            "Phone use during typical sleep hours"
        )

    with col2:
        ring(
            "Social Media Engagement",
            social_score,
            "Time spent connecting with friends online"
        )

    with col3:
        ring(
            "Screen Balance",
            screen_score,
            "Overall screen time compared to usual habits"
        )




# ---------------------------
# Page 2: Nudge Center
# ---------------------------

elif page == "Nudge Center":
    st.title("Nudge Center")
    st.caption("AI-generated empathy nudges and conversation starters.")

    col1, col2 = st.columns([2, 1])

    with col1:
        if st.button("Analyze Family Pulse"):
            with st.spinner("Analyzing with Claude..."):
                result = generate_nudge(selected_input)
                st.session_state.nudge_result = result

        if st.session_state.nudge_result:
            result = st.session_state.nudge_result

            st.subheader("Core Emotional Need")
            st.info(result.get("core_emotional_need", "N/A"))

            st.subheader("Empathy Nudge")
            st.write(result.get("empathy_nudge", "N/A"))

            st.subheader("Conversation Starter")
            st.write(result.get("conversation_starter", "N/A"))

            # Reflect & Refine button
            if st.button("Reflect & Refine"):
                with st.spinner("Refining message..."):
                    refine_payload = selected_input.copy()
                    refined = generate_nudge(refine_payload)

                st.subheader("Refined Conversation Starter")
                st.success(refined.get("conversation_starter", "N/A"))

    with col2:
        st.subheader("Safety Alerts")

        alerts = generate_safety_alerts(selected_input)

        for alert in alerts:
            if "No major" in alert:
                st.info(alert)
            else:
                st.warning(alert)



# ---------------------------
# Page 3: Practice Mode
# ---------------------------
elif page == "Practice Mode":
    st.title("Practice Mode")
    st.caption("Rehearse the conversation before approaching your child.")

    from claude_module import rewrite_parent_response, roleplay_child_response

    if "practice_mode" not in st.session_state:
        st.session_state.practice_mode = "idle"

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    parent_input = st.text_input("What would you say to your child?")

    if st.button("Send"):
        if parent_input:

            wc_result = evaluate_parent_text(parent_input)
            flagged = wc_result and wc_result.get("flagged", False)

            if flagged:
                st.session_state.practice_mode = "coaching"

                st.error("⚠ Coaching Mode Activated: This phrasing may escalate the situation.")

                improved = rewrite_parent_response(parent_input)
                suggestion = improved.get("improved_response")

                st.success("Suggested Rewrite:")
                st.write(suggestion)

                if st.button("Use Suggested Rewrite"):
                    st.session_state.practice_mode = "roleplay"

                    child_reply = roleplay_child_response(suggestion)

                    st.session_state.chat_history.append(("Parent", suggestion))
                    st.session_state.chat_history.append(("Teen", child_reply))

            else:
                st.session_state.practice_mode = "roleplay"

                child_reply = roleplay_child_response(parent_input)

                st.session_state.chat_history.append(("Parent", parent_input))
                st.session_state.chat_history.append(("Teen", child_reply))

    # MODE INDICATOR 
    if st.session_state.practice_mode == "roleplay":
        st.markdown(
            """
            <div style="padding:12px; border-radius:12px; 
            background: linear-gradient(90deg,#D1FAE5,#A7F3D0);
            font-weight:600;">
            🎭 Teen Roleplay Mode Active
            </div>
            """,
            unsafe_allow_html=True
        )

    elif st.session_state.practice_mode == "coaching":
        st.markdown(
            """
            <div style="padding:12px; border-radius:12px; 
            background: linear-gradient(90deg,#FECACA,#FCA5A5);
            font-weight:600;">
            🧠 Coaching Mode — Rewrite Required
            </div>
            """,
            unsafe_allow_html=True
        )




    # Display conversation
    for role, msg in st.session_state.chat_history:
        if role == "Parent":
            st.markdown(f"**You:** {msg}")
        else:
            st.markdown(f"**Teen:** {msg}")

    st.button("Play audio (ElevenLabs integration here)")
