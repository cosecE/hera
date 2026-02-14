

# 🛟 HERA

**Digital safety, grounded.**

HERA is an AI-powered emotional safety layer designed to help parents approach sensitive conversations with empathy rather than confrontation.

Instead of monitoring raw messages, HERA translates behavioral signals into emotional insight, and provides guided practice before difficult conversations happen.

---

## 🌟 Core Features

### 🟣 Family Health Score

A visual summary of digital wellbeing based on:

* Screen time changes
* Late-night activity
* Social engagement drift

This helps parents see trends — not spy on messages.

---

### 🧠 Nudge Center

Powered by Claude (Anthropic).

Given behavioral shifts, HERA:

* Identifies the likely **core emotional need**
* Generates a 2-sentence **Empathy Nudge**
* Provides a **Conversation Starter** script

Tone is:

* Warm
* Non-judgmental
* Supportive
* Non-surveillant

---

### 🗣 Practice Mode (White Circle + Claude)

Before speaking to their child, parents can rehearse what they want to say.

Flow:

1. Parent types a message.
2. **White Circle** evaluates tone and safety.
3. If flagged → Claude rewrites it to reduce judgment.
4. If safe → Claude roleplays a realistic teen response.

This prevents escalation before it happens.

---

## 🏗 Architecture

<img width="1024" height="1536" alt="ChatGPT Image Feb 14, 2026, 04_32_46 PM" src="https://github.com/user-attachments/assets/80d2a1ec-9624-4ba4-860a-5431b2e6e689" />



### 🛡 White Circle

* Used only in Practice Mode
* Evaluates tone and emotional risk
* Flags confrontational or harmful phrasing

### 🧠 Claude (Anthropic)

* Generates empathy nudges
* Rewrites unsafe phrasing
* Simulates teen responses for roleplay

---

## 🧪 How to Run Locally

### 1️⃣ Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/hera-anchor-ai.git
cd hera-anchor-ai
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set environment variables

Mac/Linux:

```bash
export ANTHROPIC_API_KEY="your_key"
export WHITE_CIRCLE_API_KEY="your_key"
export WHITE_CIRCLE_DEPLOYMENT_ID="your_id"
```

Windows (PowerShell):

```powershell
setx ANTHROPIC_API_KEY "your_key"
setx WHITE_CIRCLE_API_KEY "your_key"
setx WHITE_CIRCLE_DEPLOYMENT_ID "your_id"
```

Restart your terminal.

### 4️⃣ Run the app

```bash
streamlit run app.py
```

---

## 🔐 Security & Privacy Philosophy

HERA is built around three principles:

1. **No raw message storage**
2. **Signal abstraction over surveillance**
3. **Connection over control**

White Circle acts as a safety firewall.
Claude translates signals into emotional insight.
The parent remains the decision-maker.

---

## 🎯 Hackathon Focus

This prototype demonstrates:

* Behavioral drift modeling
* AI-assisted emotional translation
* Layered moderation (LLM + rule-based)
* Preventative conversation coaching

Future extensions could include:

* Longitudinal baseline tracking
* Voice coaching (ElevenLabs integration)
* Multi-turn adaptive roleplay
* Escalation-aware safety routing

---

## 👥 Team

Built for Iterate x Columbia AI Club Hackathon Spring 2026


By: Team xyz (Kaushiki, Sneha, Imaan)
