import streamlit as st
from pypdf import PdfReader
import ollama

st.title("📚 AI Study Assistant")

pdf = st.file_uploader("📄 Upload PDF", type="pdf")

if pdf:

    reader = PdfReader(pdf)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    st.success("PDF uploaded!")


    # ASK AI
    question = st.text_input("💬 Ask a question")

    if st.button("🤖 Ask AI"):

        r = ollama.chat(
            model="llama3.2:latest",
            messages=[{
                "role": "user",
                "content": text +
                "\n\nQuestion: " + question +
                "\nAnswer simply."
            }]
        )

        st.write(r["message"]["content"])


    # SUMMARY
    if st.button("📝 Summary"):

        r = ollama.chat(
            model="llama3.2:latest",
            messages=[{
                "role": "user",
                "content":
                "Summarize this in simple points:\n" + text
            }]
        )

        st.write(r["message"]["content"])


    # QUIZ
    st.subheader("❓ Quiz")

    if "quiz" not in st.session_state:
        st.session_state.quiz = []

    if "number" not in st.session_state:
        st.session_state.number = 0

    if "score" not in st.session_state:
        st.session_state.score = 0

    if st.button("Generate Quiz"):

        r = ollama.chat(
            model="llama3.2:latest",
            messages=[{
                "role": "user",
                "content": """
Create exactly 5 MCQs from this PDF.

Use ONLY this format:
Question|A|B|C|D|Correct

Example:
What is Python?|Language|Database|Browser|Game|A

Give only 5 lines.

""" + text
            }]
        )

        st.session_state.quiz = []

        for line in r["message"]["content"].splitlines():

            x = line.split("|")

            if len(x) == 6:
                st.session_state.quiz.append(x)

        st.session_state.number = 0
        st.session_state.score = 0


    # SHOW QUIZ
    if st.session_state.quiz:

        q = st.session_state.quiz[
            st.session_state.number
        ]

        st.write(
            "### Question",
            st.session_state.number + 1,
            "/",
            len(st.session_state.quiz)
        )

        st.write("**" + q[0] + "**")

        answer = st.radio(
            "Choose your answer:",
            [
                "A) " + q[1],
                "B) " + q[2],
                "C) " + q[3],
                "D) " + q[4]
            ]
        )

        if st.button("Submit"):

            selected = answer[0]

            if selected == q[5].strip():

                st.success("✅ Correct!")

                st.session_state.score += 1

            else:

                st.error(
                    "❌ Wrong! Correct answer: "
                    + q[5]
                )


        if st.button("Next"):

            if st.session_state.number < len(
                st.session_state.quiz
            ) - 1:

                st.session_state.number += 1
                st.rerun()

            else:

                st.success(
                    "🎉 Quiz Completed!"
                )

                st.write(
                    "🏆 Score:",
                    st.session_state.score,
                    "/",
                    len(st.session_state.quiz)
                )