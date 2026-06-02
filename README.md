---
title: ZenithCore
emoji: 🎯
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.38.0
app_file: app.py
pinned: false
---


# 🎙️ Interview Prep Coach

Interview Prep Coach is an AI-driven role-specific interview simulation system built using Streamlit, LangChain, and the Groq API. It helps software engineering, machine learning, and data analytics candidates prepare for interviews by conducting realistic, multi-turn technical dialogues with instant scoring, rubric evaluations, and progressive follow-ups.

---

## 🌟 Key Features

1. **Role-Specific Scenarios:** Choose SDE, ML Engineer, or Data Analyst tracks.
2. **Multi-Turn Dialogue:** Simulates actual mock interviews. After you answer a question, the AI evaluates it and asks a contextual, deep-dive follow-up question before proceeding.
3. **Interactive Hint System:** Collapsible hints that nudge you toward the right answer without giving away code or full solutions.
4. **Real-Time Rubric Evaluation:** Shows strengths, improvement areas, and a quality score (1-10) for both main and follow-up answers.
5. **Interactive Mock Mode:** Runs immediately **without API keys**, using pre-scripted high-quality interview flows across SDE, ML, and Data Analyst domains.
6. **Session Summary Card:** Download a markdown-formatted recruiter performance report at the end of the session.

---

## 🚀 Installation & Local Setup

### 1. Prerequisites
Make sure you have **Python 3.10+** installed on your system.

### 2. Clone/Copy Code & Install Dependencies
Navigate to the project root directory and run:

```bash
pip install -r requirements.txt
```

### 3. API Configuration (Optional)
To use the live LLM mode, obtain an API key from [Groq Console](https://console.groq.com/).

* **Option A (Environment File):** Copy `.env.example` to `.env` and paste your key:
  ```bash
  GROQ_API_KEY=gsk_your_actual_key_here
  ```
* **Option B (UI Input):** Paste the key directly in the sidebar inside the Streamlit app.
* **Option C (Fallback):** If no key is entered, the app automatically runs in **Interactive Mock Mode**, allowing full testing of the interview flow.

---

## 🎙️ Running the Web App

To launch the Streamlit server locally, run the following command in your terminal:

```bash
streamlit run app.py
```

The application will automatically launch in your default web browser (usually at `http://localhost:8501`).

---

## 📂 File Structure

* `app.py`: Main Streamlit app containing UI layout, state machine transitions, and custom CSS styling.
* `llm_handler.py`: Interface to Groq API via LangChain; houses the mock database for offline fallback.
* `prompts.py`: LangChain prompt templates (generation, hint, evaluation, follow-up, summary).
* `requirements.txt`: Python package dependencies.
* `.env.example`: Template for environment setup.
