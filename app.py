# app.py
import streamlit as st
from llm_handler import LLMHandler
from pdf_generator import generate_pdf_report
import os

# Set page configuration first
st.set_page_config(
    page_title="Interview Prep Coach",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium CSS styling (Dark Theme / Glassmorphism)
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

/* Main App Font and Colors */
html, body, [class*="css"], .stApp {
    font-family: 'Outfit', sans-serif;
    background: radial-gradient(circle at 10% 20%, #1e1e2f 0%, #111119 90%) !important;
    color: #e2e8f0 !important;
}

/* Sidebar Custom Styling */
section[data-testid="stSidebar"] {
    background-color: #151522 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}
section[data-testid="stSidebar"] .stMarkdown h1, 
section[data-testid="stSidebar"] .stMarkdown h2, 
section[data-testid="stSidebar"] .stMarkdown h3 {
    color: #a78bfa !important;
}

/* Cards & Containers */
.custom-card {
    background: rgba(255, 255, 255, 0.03) !important;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    padding: 24px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
}

/* Bubble Styling */
.chat-bubble {
    padding: 16px 20px;
    border-radius: 16px;
    margin-bottom: 12px;
    line-height: 1.5;
    font-size: 1.05rem;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
.interviewer-bubble {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border-left: 5px solid #6366f1;
    color: #e2e8f0;
}
.candidate-bubble {
    background: linear-gradient(135deg, #312e81 0%, #1e1b4b 100%);
    border-right: 5px solid #a855f7;
    color: #f3e8ff;
    text-align: left;
}

/* Evaluation Card */
.eval-card {
    background: rgba(16, 185, 129, 0.04) !important;
    border: 1px solid rgba(16, 185, 129, 0.2) !important;
    border-left: 6px solid #10b981 !important;
    border-radius: 12px;
    padding: 20px;
    margin-top: 10px;
    margin-bottom: 20px;
}

.eval-card-warning {
    background: rgba(239, 68, 68, 0.04) !important;
    border: 1px solid rgba(239, 68, 68, 0.2) !important;
    border-left: 6px solid #ef4444 !important;
    border-radius: 12px;
    padding: 20px;
    margin-top: 10px;
    margin-bottom: 20px;
}

/* Badges */
.score-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 1.1rem;
    margin-bottom: 10px;
}
.score-high {
    background: rgba(16, 185, 129, 0.2);
    color: #34d399;
    border: 1px solid #10b981;
}
.score-medium {
    background: rgba(245, 158, 11, 0.2);
    color: #fbbf24;
    border: 1px solid #f59e0b;
}
.score-low {
    background: rgba(239, 68, 68, 0.2);
    color: #f87171;
    border: 1px solid #ef4444;
}

/* Typography styles */
.gradient-text {
    background: linear-gradient(135deg, #a855f7 0%, #6366f1 50%, #3b82f6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800;
}

/* Custom buttons */
.stButton>button {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
}
.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
}

/* Custom secondary buttons (Skip / Start Over) */
div[data-testid="column"] .stButton>button[key*="skip"], 
div[data-testid="column"] .stButton>button[key*="reset"],
div[data-testid="stSidebar"] .stButton>button {
    background: rgba(255, 255, 255, 0.05) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: none !important;
}
div[data-testid="column"] .stButton>button[key*="skip"]:hover,
div[data-testid="stSidebar"] .stButton>button:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
}

/* Custom Progress tracker steps */
.progress-container {
    display: flex;
    justify-content: space-between;
    margin-bottom: 25px;
    background: rgba(255,255,255,0.02);
    padding: 12px 20px;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.05);
}
.progress-node {
    display: flex;
    align-items: center;
    gap: 8px;
    font-weight: 500;
}
.node-circle {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    font-weight: 700;
}
.node-circle.active {
    background: #6366f1;
    color: white;
    box-shadow: 0 0 12px #6366f1;
}
.node-circle.completed {
    background: #10b981;
    color: white;
}
.node-circle.pending {
    background: #334155;
    color: #94a3b8;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

def render_html(html_str):
    """Renders HTML by stripping leading/trailing whitespace from each line
    and joining them without newlines, preventing Streamlit markdown code blocks."""
    clean_html = "".join(line.strip() for line in html_str.split('\n'))
    st.markdown(clean_html, unsafe_allow_html=True)

# ----------------- SESSION STATE INITS -----------------
if "initialized" not in st.session_state:
    st.session_state.initialized = False
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_question_idx" not in st.session_state:
    st.session_state.current_question_idx = 0
if "stage" not in st.session_state:
    st.session_state.stage = "main_question"  # main_question, main_evaluated, follow_up_evaluated, completed
if "transcript" not in st.session_state:
    st.session_state.transcript = []
if "hint_used" not in st.session_state:
    st.session_state.hint_used = False
if "hint_text" not in st.session_state:
    st.session_state.hint_text = ""
if "summary_report" not in st.session_state:
    st.session_state.summary_report = ""

# Temporary holds for the current active step before committing to transcript
if "current_main_answer" not in st.session_state:
    st.session_state.current_main_answer = ""
if "current_main_eval" not in st.session_state:
    st.session_state.current_main_eval = None
if "current_follow_up_question" not in st.session_state:
    st.session_state.current_follow_up_question = ""
if "current_follow_up_answer" not in st.session_state:
    st.session_state.current_follow_up_answer = ""
if "current_follow_up_eval" not in st.session_state:
    st.session_state.current_follow_up_eval = None

# Predefined topics lookup mapping
TOPICS_BY_ROLE = {
    "Software Development Engineer (SDE)": ["Data Structures & Algorithms", "System Design", "Operating Systems & Concurrency", "Databases (SQL/NoSQL)", "Web Architectures"],
    "Machine Learning Engineer (ML)": ["Machine Learning Theory", "Deep Learning & NLP", "ML System Design & MLOps", "Feature Engineering & Data Prep", "Computer Vision"],
    "Data Analyst": ["SQL & Data Manipulation", "A/B Testing & Statistics", "Cohort & Customer Analytics", "Data Visualization & Metrics", "Excel & Dashboard Design"]
}

# ----------------- SIDEBAR CONFIG -----------------
st.sidebar.markdown("<h2 style='text-align: center; margin-bottom: 20px;'>🛠️ Interview Setup</h2>", unsafe_allow_html=True)

role = st.sidebar.selectbox(
    "Select Target Role",
    options=["Software Development Engineer (SDE)", "Machine Learning Engineer (ML)", "Data Analyst"]
)

difficulty = st.sidebar.selectbox(
    "Select Difficulty Level",
    options=["Easy", "Medium", "Hard"]
)

# Select predefined topic or choose custom
predefined_topics = TOPICS_BY_ROLE[role]
topic_choice = st.sidebar.selectbox(
    "Select Topic Area",
    options=predefined_topics + ["Custom (Type below)..."]
)

if topic_choice == "Custom (Type below)...":
    topic = st.sidebar.text_input("Enter Custom Topic", value="Python programming")
else:
    topic = topic_choice

num_questions = st.sidebar.slider(
    "Number of Questions",
    min_value=1,
    max_value=5,
    value=3
)

# Secure API Key input
api_key_input = st.sidebar.text_input(
    "Groq API Key (Optional)",
    type="password",
    help="Enter your Groq API key here. If left blank, the app will run in Interactive Mock Mode with realistic, pre-scripted questions and answers.",
    value=os.getenv("GROQ_API_KEY", "")
)

# Initialize handler inside session state if not already set or key changed
if "llm_handler" not in st.session_state or st.session_state.get("last_api_key") != api_key_input:
    st.session_state.llm_handler = LLMHandler(api_key=api_key_input)
    st.session_state.last_api_key = api_key_input

handler = st.session_state.llm_handler

# Session management buttons
if not st.session_state.initialized:
    if st.sidebar.button("🚀 Start Mock Interview", use_container_width=True):
        with st.spinner("Generating customized question set..."):
            questions = handler.generate_questions(role, difficulty, topic, num_questions)
            if questions:
                st.session_state.questions = questions
                st.session_state.current_question_idx = 0
                st.session_state.stage = "main_question"
                st.session_state.transcript = []
                st.session_state.initialized = True
                st.session_state.hint_used = False
                st.session_state.hint_text = ""
                st.session_state.summary_report = ""
                st.session_state.current_main_answer = ""
                st.session_state.current_main_eval = None
                st.session_state.current_follow_up_question = ""
                st.session_state.current_follow_up_answer = ""
                st.session_state.current_follow_up_eval = None
                st.rerun()
            else:
                st.sidebar.error("Failed to generate questions. Please verify your API key or connection.")
else:
    if st.sidebar.button("🛑 End & Start Over", use_container_width=True):
        st.session_state.initialized = False
        st.session_state.questions = []
        st.session_state.current_question_idx = 0
        st.session_state.stage = "main_question"
        st.session_state.transcript = []
        st.session_state.hint_used = False
        st.session_state.hint_text = ""
        st.session_state.summary_report = ""
        st.rerun()

# ----------------- SIDEBAR INFOPANEL -----------------
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Session Info")
if handler.is_mock_mode():
    st.sidebar.warning("⚡ **Mode:** Interactive Mock Mode (No Groq key provided. Running pre-scripted high-quality interview flows).")
else:
    st.sidebar.success("🔥 **Mode:** Live LLaMA 3.3 API Mode (Connected to Groq).")

st.sidebar.markdown(
    """
    **Rubric evaluated:**
    1. **Correctness:** Technical accuracy & constraints.
    2. **Clarity:** Explanation flow & structure.
    3. **Completeness:** Core issues addressed.
    """
)


# ----------------- MAIN APP WINDOW -----------------

# Header Card
st.markdown("<h1 style='margin-bottom: 0px;'>🎙️ <span class='gradient-text'>Interview Prep Coach</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 1.15rem; color: #94a3b8; margin-top: 5px; margin-bottom: 25px;'>Tailored AI interview simulations with real-time feedback & multi-turn dialogue.</p>", unsafe_allow_html=True)

if not st.session_state.initialized:
    # ----------------- LANDING SCREEN -----------------
    render_html(
        """
        <div class='custom-card'>
            <h2>Welcome to your personal AI Interview Coach!</h2>
            <p style='font-size: 1.1rem; line-height: 1.6; color: #cbd5e1;'>
                Prepare for technical roles dynamically. Unlike static question sheets, this system builds a real <b>multi-turn conversation</b>. 
                After each response, the coach evaluates your feedback and asks a targeted <b>follow-up question</b> to check your depth of knowledge, just like a real engineering interviewer.
            </p>
            <h3 style='margin-top: 25px;'>How to get started:</h3>
            <ol style='font-size: 1.05rem; line-height: 1.8; color: #cbd5e1;'>
                <li>Configure your target role, difficulty, and focus topic in the sidebar.</li>
                <li>Enter your <b>Groq API Key</b> if you want real-time LLM-generated questions. <i>(Otherwise, leave it blank to run in <b>Interactive Mock Mode</b> with pre-compiled technical questions).</i></li>
                <li>Click <b>Start Mock Interview</b> to begin!</li>
            </ol>
        </div>
        """
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        render_html(
            """
            <div class='custom-card' style='text-align: center; height: 180px;'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>🚀</div>
                <h4>Domain Tailored</h4>
                <p style='font-size: 0.95rem; color: #94a3b8;'>Specific questions generated dynamically for SDE, ML, or Data Analyst tracks.</p>
            </div>
            """
        )
    with col2:
        render_html(
            """
            <div class='custom-card' style='text-align: center; height: 180px;'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>📊</div>
                <h4>Real-Time Rubric</h4>
                <p style='font-size: 0.95rem; color: #94a3b8;'>Get a Confidence Score (1-10) and structured tips on accuracy and communication.</p>
            </div>
            """
        )
    with col3:
        render_html(
            """
            <div class='custom-card' style='text-align: center; height: 180px;'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>🔁</div>
                <h4>Multi-Turn Probe</h4>
                <p style='font-size: 0.95rem; color: #94a3b8;'>Contextual follow-ups challenge your assertions, trade-offs, and scalability concepts.</p>
            </div>
            """
        )

else:
    # ----------------- ACTIVE INTERVIEW -----------------
    
    questions = st.session_state.questions
    q_idx = st.session_state.current_question_idx
    stage = st.session_state.stage
    
    # Progress Node Display
    progress_html = "<div class='progress-container'>"
    for i in range(len(questions)):
        if i < q_idx:
            status_class = "completed"
            symbol = "✔"
        elif i == q_idx:
            status_class = "active"
            symbol = "▶"
        else:
            status_class = "pending"
            symbol = str(i + 1)
        progress_html += (
            f"<div class='progress-node'>"
            f"<div class='node-circle {status_class}'>{symbol}</div>"
            f"<span style='color: {'#818cf8' if i == q_idx else ('#34d399' if i < q_idx else '#64748b')}; "
            f"font-weight: {'600' if i == q_idx else '400'};'>Q{i+1}</span>"
            f"</div>"
        )
    progress_html += "</div>"
    st.markdown(progress_html, unsafe_allow_html=True)
    
    # Check if completed
    if stage == "completed":
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("## 🎉 Interview Completed!")
        st.markdown("The recruiter has compiled your final performance score card and review roadmap below:")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown(st.session_state.summary_report)
        
        # Download summary PDF
        try:
            pdf_data = generate_pdf_report(
                role=role,
                difficulty=difficulty,
                topic=topic,
                transcript_list=st.session_state.transcript
            )
            st.download_button(
                label="💾 Download Session Summary Report (PDF)",
                data=pdf_data,
                file_name=f"interview_summary_{role.lower().replace(' ', '_')}_{difficulty.lower()}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Error compiling PDF: {e}")
        
        if st.button("🔄 Start a New Interview"):
            st.session_state.initialized = False
            st.rerun()
            
    else:
        # Show Current Question Information
        active_q = questions[q_idx]["question"]
        expected_concepts = questions[q_idx].get("expected_topics", [])
        
        # Render Chat History (Completed questions)
        if len(st.session_state.transcript) > 0:
            st.markdown("### 💬 Interview Dialogue History")
            for i, entry in enumerate(st.session_state.transcript):
                st.markdown(f"**Interviewer (Question {i+1}):**")
                st.markdown(f"<div class='chat-bubble interviewer-bubble'>{entry['question']}</div>", unsafe_allow_html=True)
                
                st.markdown(f"**Candidate:**")
                st.markdown(f"<div class='chat-bubble candidate-bubble'>{entry['answer']}</div>", unsafe_allow_html=True)
                
                # Render Main Evaluation
                score = entry["score"]
                score_class = "score-high" if score >= 8 else ("score-medium" if score >= 5 else "score-low")
                eval_html = f"""
                <div class='eval-card'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <strong style='font-size: 1.15rem; color: #10b981;'>📊 Question {i+1} Evaluation</strong>
                        <span class='score-badge {score_class}'>Score: {score}/10</span>
                    </div>
                    <p style='margin-top: 10px;'><b>Technical Accuracy:</b> {entry['feedback'].split('Communication:')[0].replace('Correctness:', '').strip()}</p>
                    <p><b>Communication Quality:</b> {entry['feedback'].split('Communication:')[1].strip() if 'Communication:' in entry['feedback'] else ''}</p>
                    <div style='margin-top: 10px;'>
                        <b>🌟 Strengths:</b>
                        <ul>{"".join([f"<li>{s}</li>" for s in entry['strengths']])}</ul>
                    </div>
                    <div>
                        <b>💡 Areas for Improvement:</b>
                        <ul>{"".join([f"<li>{tip}</li>" for tip in entry['improvement_tips']])}</ul>
                    </div>
                </div>
                """
                render_html(eval_html)
                
                # Render Follow up if present
                if entry.get("follow_up_question"):
                    st.markdown(f"**Interviewer (Follow-up Question):**")
                    st.markdown(f"<div class='chat-bubble interviewer-bubble'>{entry['follow_up_question']}</div>", unsafe_allow_html=True)
                    
                    st.markdown(f"**Candidate (Follow-up Answer):**")
                    st.markdown(f"<div class='chat-bubble candidate-bubble'>{entry['follow_up_answer']}</div>", unsafe_allow_html=True)
                    
                    fu_score = entry["follow_up_score"]
                    fu_score_class = "score-high" if fu_score >= 8 else ("score-medium" if fu_score >= 5 else "score-low")
                    fu_eval_html = f"""
                    <div class='eval-card'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <strong style='font-size: 1.15rem; color: #10b981;'>📊 Follow-up Evaluation</strong>
                            <span class='score-badge {fu_score_class}'>Score: {fu_score}/10</span>
                        </div>
                        <p style='margin-top: 10px;'><b>Technical Accuracy:</b> {entry['follow_up_feedback'].split('Communication:')[0].replace('Correctness:', '').strip()}</p>
                        <p><b>Communication Quality:</b> {entry['follow_up_feedback'].split('Communication:')[1].strip() if 'Communication:' in entry['follow_up_feedback'] else ''}</p>
                        <div style='margin-top: 10px;'>
                            <b>🌟 Strengths:</b>
                            <ul>{"".join([f"<li>{s}</li>" for s in entry.get('follow_up_strengths', [])])}</ul>
                        </div>
                        <div>
                            <b>💡 Areas for Improvement:</b>
                            <ul>{"".join([f"<li>{tip}</li>" for tip in entry.get('follow_up_improvement_tips', [])])}</ul>
                        </div>
                    </div>
                    """
                    render_html(fu_eval_html)
            st.markdown("---")

        # ----------------- CURRENT PHASE -----------------
        st.markdown(f"### 🎯 Active Question: Question {q_idx + 1} of {len(questions)}")
        
        # Render interviewer active bubble
        if stage == "main_question":
            st.markdown(f"<div class='chat-bubble interviewer-bubble'><b>Interviewer:</b> {active_q}</div>", unsafe_allow_html=True)
        elif stage == "main_evaluated":
            st.markdown(f"<div class='chat-bubble interviewer-bubble'><b>Interviewer:</b> {active_q}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='chat-bubble candidate-bubble'><b>Candidate:</b> {st.session_state.current_main_answer}</div>", unsafe_allow_html=True)
            
            # Display current main evaluation
            score = st.session_state.current_main_eval["score"]
            score_class = "score-high" if score >= 8 else ("score-medium" if score >= 5 else "score-low")
            main_eval_html = f"""
            <div class='eval-card'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <strong style='font-size: 1.15rem; color: #10b981;'>📊 Question {q_idx+1} Evaluation</strong>
                    <span class='score-badge {score_class}'>Score: {score}/10</span>
                </div>
                <p style='margin-top: 10px;'><b>Technical Accuracy:</b> {st.session_state.current_main_eval['correctness_feedback']}</p>
                <p><b>Communication Quality:</b> {st.session_state.current_main_eval['communication_feedback']}</p>
                <div style='margin-top: 10px;'>
                    <b>🌟 Strengths:</b>
                    <ul>{"".join([f"<li>{s}</li>" for s in st.session_state.current_main_eval['strengths']])}</ul>
                </div>
                <div>
                    <b>💡 Areas for Improvement:</b>
                    <ul>{"".join([f"<li>{tip}</li>" for tip in st.session_state.current_main_eval['improvement_tips']])}</ul>
                </div>
            </div>
            """
            render_html(main_eval_html)
            
            # Display Follow-up Question
            st.markdown(f"<div class='chat-bubble interviewer-bubble'><b>Interviewer (Follow-up):</b> {st.session_state.current_follow_up_question}</div>", unsafe_allow_html=True)
            
        elif stage == "follow_up_evaluated":
            st.markdown(f"<div class='chat-bubble interviewer-bubble'><b>Interviewer:</b> {active_q}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='chat-bubble candidate-bubble'><b>Candidate:</b> {st.session_state.current_main_answer}</div>", unsafe_allow_html=True)
            
            # Render evaluation
            score = st.session_state.current_main_eval["score"]
            score_class = "score-high" if score >= 8 else ("score-medium" if score >= 5 else "score-low")
            render_html(f"""
            <div class='eval-card'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <strong style='font-size: 1.15rem; color: #10b981;'>📊 Question {q_idx+1} Evaluation</strong>
                    <span class='score-badge {score_class}'>Score: {score}/10</span>
                </div>
                <p>{st.session_state.current_main_eval['correctness_feedback']}</p>
            </div>
            """)
            
            st.markdown(f"<div class='chat-bubble interviewer-bubble'><b>Interviewer (Follow-up):</b> {st.session_state.current_follow_up_question}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='chat-bubble candidate-bubble'><b>Candidate:</b> {st.session_state.current_follow_up_answer}</div>", unsafe_allow_html=True)
            
            # Display follow up evaluation
            fu_score = st.session_state.current_follow_up_eval["score"]
            fu_score_class = "score-high" if fu_score >= 8 else ("score-medium" if fu_score >= 5 else "score-low")
            fu_eval_html = f"""
            <div class='eval-card'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <strong style='font-size: 1.15rem; color: #10b981;'>📊 Follow-up Evaluation</strong>
                    <span class='score-badge {fu_score_class}'>Score: {fu_score}/10</span>
                </div>
                <p style='margin-top: 10px;'><b>Technical Accuracy:</b> {st.session_state.current_follow_up_eval['correctness_feedback']}</p>
                <p><b>Communication Quality:</b> {st.session_state.current_follow_up_eval['communication_feedback']}</p>
                <div style='margin-top: 10px;'>
                    <b>🌟 Strengths:</b>
                    <ul>{"".join([f"<li>{s}</li>" for s in st.session_state.current_follow_up_eval['strengths']])}</ul>
                </div>
                <div>
                    <b>💡 Areas for Improvement:</b>
                    <ul>{"".join([f"<li>{tip}</li>" for tip in st.session_state.current_follow_up_eval['improvement_tips']])}</ul>
                </div>
            </div>
            """
            render_html(fu_eval_html)

        # ----------------- USER INPUT & CONTROLS -----------------
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Hint Panel
        if stage in ["main_question", "main_evaluated"]:
            is_fu = (stage == "main_evaluated")
            
            # Custom styled Expanders for Hints
            with st.expander("💡 Need a hint? (Click to expand)"):
                if not st.session_state.hint_used:
                    if st.button("Generate Hint", key=f"hint_btn_{q_idx}_{is_fu}"):
                        with st.spinner("Compiling hint..."):
                            hint = handler.get_hint(
                                role=role,
                                difficulty=difficulty,
                                question=st.session_state.current_follow_up_question if is_fu else active_q,
                                answer_so_far="",
                                question_id=questions[q_idx]["id"],
                                is_follow_up=is_fu
                            )
                            st.session_state.hint_text = hint
                            st.session_state.hint_used = True
                            st.rerun()
                else:
                    st.info(st.session_state.hint_text)

        # Answer text area
        if stage == "main_question":
            user_input = st.text_area(
                "Write your technical answer below:",
                placeholder="Explain key concepts, algorithms, data structures, and trade-offs. Mention time/space complexity if applicable.",
                key="answer_input_main",
                height=150
            )
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("Submit Answer", key="submit_main", use_container_width=True):
                    if user_input.strip() == "":
                        st.error("Please enter an answer before submitting.")
                    else:
                        with st.spinner("Interviewer is analyzing your response and formulating a follow-up..."):
                            # 1. Evaluate answer
                            evaluation = handler.evaluate_answer(
                                role=role,
                                difficulty=difficulty,
                                question=active_q,
                                user_answer=user_input,
                                question_id=questions[q_idx]["id"],
                                is_follow_up=False
                            )
                            # 2. Generate follow-up
                            follow_up = handler.generate_follow_up(
                                role=role,
                                difficulty=difficulty,
                                question=active_q,
                                user_answer=user_input,
                                question_id=questions[q_idx]["id"]
                            )
                            
                            # 3. Store in temp session state
                            st.session_state.current_main_answer = user_input
                            st.session_state.current_main_eval = evaluation
                            st.session_state.current_follow_up_question = follow_up
                            
                            # 4. Progress stage
                            st.session_state.stage = "main_evaluated"
                            st.session_state.hint_used = False
                            st.session_state.hint_text = ""
                            st.rerun()
            with col2:
                if st.button("Skip Question ➡️", key="skip_q", use_container_width=True):
                    # Create a skipped entry
                    skipped_entry = {
                        "question": active_q,
                        "answer": "[Skipped]",
                        "score": 0,
                        "feedback": "Correctness: Question was skipped by candidate.\nCommunication: N/A",
                        "strengths": [],
                        "improvement_tips": ["Skipping questions prevents assessment. Try writing even basic conceptual points to get partial feedback."],
                        "follow_up_question": "",
                        "follow_up_answer": "[N/A]",
                        "follow_up_score": 0,
                        "follow_up_feedback": "Correctness: N/A\nCommunication: N/A",
                        "follow_up_strengths": [],
                        "follow_up_improvement_tips": []
                    }
                    st.session_state.transcript.append(skipped_entry)
                    
                    # Advance index or complete
                    if q_idx < len(questions) - 1:
                        st.session_state.current_question_idx += 1
                        st.session_state.stage = "main_question"
                    else:
                        st.session_state.stage = "completed"
                        with st.spinner("Generating final session summary..."):
                            summary = handler.generate_session_summary(role, difficulty, topic, st.session_state.transcript)
                            st.session_state.summary_report = summary
                    st.session_state.hint_used = False
                    st.session_state.hint_text = ""
                    st.rerun()

        elif stage == "main_evaluated":
            user_input_fu = st.text_area(
                f"Write your response to the follow-up question:",
                placeholder="Elaborate on the specific constraints, trade-offs, or optimization points raised.",
                key="answer_input_fu",
                height=150
            )
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("Submit Follow-up Answer", key="submit_fu", use_container_width=True):
                    if user_input_fu.strip() == "":
                        st.error("Please enter a response before submitting.")
                    else:
                        with st.spinner("Interviewer is evaluating your follow-up..."):
                            # 1. Evaluate follow-up
                            fu_evaluation = handler.evaluate_answer(
                                role=role,
                                difficulty=difficulty,
                                question=st.session_state.current_follow_up_question,
                                user_answer=user_input_fu,
                                question_id=questions[q_idx]["id"],
                                is_follow_up=True
                            )
                            
                            # 2. Store in temp state
                            st.session_state.current_follow_up_answer = user_input_fu
                            st.session_state.current_follow_up_eval = fu_evaluation
                            
                            # 3. Progress stage
                            st.session_state.stage = "follow_up_evaluated"
                            st.session_state.hint_used = False
                            st.session_state.hint_text = ""
                            st.rerun()
            with col2:
                if st.button("Skip Follow-up ➡️", key="skip_fu", use_container_width=True):
                    # Store main answer + evaluation, but skip follow up
                    entry = {
                        "question": active_q,
                        "answer": st.session_state.current_main_answer,
                        "score": st.session_state.current_main_eval["score"],
                        "feedback": f"Correctness: {st.session_state.current_main_eval['correctness_feedback']}\nCommunication: {st.session_state.current_main_eval['communication_feedback']}",
                        "strengths": st.session_state.current_main_eval["strengths"],
                        "improvement_tips": st.session_state.current_main_eval["improvement_tips"],
                        "follow_up_question": st.session_state.current_follow_up_question,
                        "follow_up_answer": "[Skipped]",
                        "follow_up_score": 0,
                        "follow_up_feedback": "Correctness: Follow-up question was skipped by candidate.\nCommunication: N/A",
                        "follow_up_strengths": [],
                        "follow_up_improvement_tips": ["Try attempting follow-up questions to demonstrate depth of thinking."]
                    }
                    st.session_state.transcript.append(entry)
                    
                    # Advance or complete
                    if q_idx < len(questions) - 1:
                        st.session_state.current_question_idx += 1
                        st.session_state.stage = "main_question"
                    else:
                        st.session_state.stage = "completed"
                        with st.spinner("Generating final session summary..."):
                            summary = handler.generate_session_summary(role, difficulty, topic, st.session_state.transcript)
                            st.session_state.summary_report = summary
                    st.session_state.hint_used = False
                    st.session_state.hint_text = ""
                    st.rerun()

        elif stage == "follow_up_evaluated":
            # Both questions have been answered and evaluated for this index.
            # Package this step into transcript
            entry = {
                "question": active_q,
                "answer": st.session_state.current_main_answer,
                "score": st.session_state.current_main_eval["score"],
                "feedback": f"Correctness: {st.session_state.current_main_eval['correctness_feedback']}\nCommunication: {st.session_state.current_main_eval['communication_feedback']}",
                "strengths": st.session_state.current_main_eval["strengths"],
                "improvement_tips": st.session_state.current_main_eval["improvement_tips"],
                "follow_up_question": st.session_state.current_follow_up_question,
                "follow_up_answer": st.session_state.current_follow_up_answer,
                "follow_up_score": st.session_state.current_follow_up_eval["score"],
                "follow_up_feedback": f"Correctness: {st.session_state.current_follow_up_eval['correctness_feedback']}\nCommunication: {st.session_state.current_follow_up_eval['communication_feedback']}",
                "follow_up_strengths": st.session_state.current_follow_up_eval["strengths"],
                "follow_up_improvement_tips": st.session_state.current_follow_up_eval["improvement_tips"]
            }
            
            if entry not in st.session_state.transcript:
                st.session_state.transcript.append(entry)
            
            if q_idx < len(questions) - 1:
                if st.button("Proceed to Next Question ➡️"):
                    st.session_state.current_question_idx += 1
                    st.session_state.stage = "main_question"
                    st.session_state.hint_used = False
                    st.session_state.hint_text = ""
                    st.session_state.current_main_answer = ""
                    st.session_state.current_main_eval = None
                    st.session_state.current_follow_up_question = ""
                    st.session_state.current_follow_up_answer = ""
                    st.session_state.current_follow_up_eval = None
                    st.rerun()
            else:
                if st.button("🏁 Compile Final Session Summary Report"):
                    with st.spinner("Generating comprehensive feedback report..."):
                        summary = handler.generate_session_summary(role, difficulty, topic, st.session_state.transcript)
                        st.session_state.summary_report = summary
                        st.session_state.stage = "completed"
                        st.rerun()
