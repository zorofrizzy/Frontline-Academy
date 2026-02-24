import json
import requests
import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()

BACKEND_URL_DEFAULT = os.getenv("BACKEND_URL_DEFAULT", "http://127.0.0.1:8000")

st.set_page_config(page_title="Frontline Academy", page_icon="🧠", layout="centered")

st.title("Frontline Academy 🧠")
st.caption("Upload a document OR type a topic prompt to generate an MCQ quiz via Gemini.")

# ---- Session state ----
if "quiz" not in st.session_state:
    st.session_state.quiz = None
if "last_error" not in st.session_state:
    st.session_state.last_error = None
if "score" not in st.session_state:
    st.session_state.score = None


with st.sidebar:
    st.header("Settings")
    st.text(BACKEND_URL_DEFAULT[7:25])
    backend_url = BACKEND_URL_DEFAULT
    #backend_url = st.text_input("Backend URL", value=BACKEND_URL_DEFAULT[:10])
    st.write("Health check:")
    try:
        r = requests.get(f"{backend_url}/health", timeout=3)
        st.success(r.json())
    except Exception as e:
        st.error(f"Backend not reachable: {e}")


with st.form("quiz_form"):
    uploaded_files = st.file_uploader("Upload files (PDF/images/etc)", accept_multiple_files=True)
    user_prompt = st.text_area("Or enter a prompt/topic", height=140, placeholder="e.g., Infection control basics for nurses")

    difficulty = st.select_slider("Difficulty", options=["Easy", "Medium", "Hard"], value="Medium")
    number_of_questions = st.slider("Number of questions", min_value=5, max_value=50, value=10)

    submitted = st.form_submit_button("Generate Quiz")

if submitted:
    st.session_state.last_error = None
    st.session_state.quiz = None
    st.session_state.score = None

    try:
        data = {
            "difficulty": difficulty,
            "number_of_questions": str(number_of_questions),
            "user_prompt": user_prompt or "",
        }

        files_payload = []
        if uploaded_files:
            for f in uploaded_files:
                files_payload.append(("files", (f.name, f.getvalue(), f.type or "application/octet-stream")))

        resp = requests.post(
            f"{backend_url}/generate-quiz/",
            data=data,
            files=files_payload if files_payload else None,
            timeout=120,
        )

        if resp.status_code != 200:
            st.session_state.last_error = resp.text
        else:
            payload = resp.json()
            # backend returns {"quiz": [...], "raw": {...}}
            st.session_state.quiz = payload.get("quiz", [])
        print("resp:", resp.json())
    except Exception as e:
        st.session_state.last_error = str(e)

# ---- Errors ----
if st.session_state.last_error:
    st.error("Failed to generate quiz")
    st.code(st.session_state.last_error)

# ---- Render quiz ----
quiz = st.session_state.quiz
if quiz:
    st.subheader("Your Quiz")

    with st.form("answers_form"):
        user_answers = []
        correct_answers = []

        for i, q in enumerate(quiz):
            question = q.get("question", f"Question {i+1}")
            options = q.get("options", [])
            answer = q.get("answer", "")

            choice = st.radio(
                f"Q{i+1}. {question}",
                options,
                index=None,
                key=f"q_{i}",
            )

            user_answers.append(choice)
            correct_answers.append(answer)

        submitted_answers = st.form_submit_button("Submit Answers")

    if submitted_answers:
        correct = 0
        total = len(correct_answers)

        review = []
        for i, (q, ua, ca) in enumerate(zip(quiz, user_answers, correct_answers), start=1):
            is_correct = (ua == ca)
            if is_correct:
                correct += 1

            review.append(
                {
                    "qnum": i,
                    "question": q.get("question", f"Question {i}"),
                    "selected": ua,  # can be None
                    "correct": ca,
                    "justification": q.get("justification", ""),
                    "is_correct": is_correct,
                }
            )

        st.session_state.score = {"correct": correct, "total": total, "review": review}

    # After submission: show score + colored answers + justification
    if st.session_state.score:
        c = st.session_state.score["correct"]
        t = st.session_state.score["total"]
        st.success(f"Score: {c}/{t}")

        st.subheader("Review")

        for item in st.session_state.score["review"]:
            qnum = item["qnum"]
            qtext = item["question"]
            selected = item["selected"]
            correct_ans = item["correct"]
            justification = item["justification"]

            icon = "✅" if item["is_correct"] else "❌"
            st.markdown(f"### {icon} Q{qnum}. {qtext}")

            # Show incorrect selected in red ONLY if it's wrong and not None
            if selected is not None and selected != correct_ans:
                st.markdown(f"**Your answer:** :red[{selected}]")
            elif selected is None:
                st.markdown("**Your answer:** :red[(no answer)]")
            else:
                # selected == correct
                st.markdown(f"**Your answer:** :green[{selected}]")

            # Always show correct answer in green
            st.markdown(f"**Correct answer:** :green[{correct_ans}]")

            # Show justification only after submit
            if justification:
                st.markdown(f"**Justification:** {justification}")
            else:
                st.markdown("**Justification:** (not provided)")

            st.divider()

    # Keep your existing raw JSON expander
    with st.expander("Show raw quiz JSON"):
        st.json({"quiz": quiz})