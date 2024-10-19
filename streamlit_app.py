import streamlit as st
import time
from youtube_transcript_api import YouTubeTranscriptApi
import json
import os

from dotenv import load_dotenv
import os
from openai import OpenAI

# Load environment variables from the .env file
load_dotenv()

API_KEY = os.environ.get('OPENAI_API_KEY')
MODEL_NAME = os.environ.get('MODEL_NAME')

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)


def extract_youtube_id(url):
    # Simple extraction, assumes standard YouTube URL format
    return url.split("v=")[1]

def extract_knowledge(youtube_url):
    try:
        video_id = extract_youtube_id(youtube_url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine all text from the transcript
        document = " ".join([entry['text'] for entry in transcript])
        
        return document, "Done analyzing the video!"
    except Exception as e:
        return None, f"Error: {str(e)}"

def create_question_prompt(document):
    return f"""
You are a seasoned professor with over 20 years of experience in designing assessments that measure both breadth and depth of knowledge in candidates across various subjects. You have a proven track record of creating questions that thoroughly evaluate a candidate’s understanding and analytical skills.

Your approach is characterized by:

- Comprehensive analysis of the entire document to ensure no relevant concepts are overlooked.
- Crafting clear and focused questions that assess both basic comprehension and deeper insights.
- Ethical and inclusive question design, ensuring fairness and accessibility to all students.
- A focus on evaluating long-term mastery of the material, not just rote memorization.

Given the following document, generate a list of relevant questions that comprehensively cover the material from the beginning, middle, and end of the document. Ensure that no important concept addressed in the document is missed, and that the questions assess both the breadth and depth of understanding. Do not refer directly to the document itself, but base your questions on its contents.

DOCUMENT:
{document}

Your list of questions should reflect your expertise and adhere to your characteristic approach. Precisely analyze the document and ask as many questions as needed. You don't want to leave out questions. There exist no stupid questions. NEVER EVER refer to the document or talk. Your questions should be independent.

Please generate as many precise questions as possible, and do not include any introductory sentences in your answers—only the questions.
DON'T ADD INTRODUCTORY PARAGRAPHS NOR OUTRODUCTORY PARAGRAPHS JUST PROVIDE QUESTIONS AND ANSWERS.
"""

def create_answer_prompt(document, questions):
    return f"""
You are a seasoned professor with over 20 years of experience in evaluating candidates’ knowledge across various subjects. Your proven track record includes providing precise, well-thought-out answers that address both the basic and deeper insights required for mastery.

Your approach is characterized by:

- Comprehensive analysis of questions to ensure no essential concept is missed.
- Crafting clear and detailed answers that demonstrate a solid understanding of the subject.
- Ethical and inclusive response design, ensuring clarity and accessibility to all.
- A focus on promoting long-term mastery of the material, ensuring answers go beyond surface-level knowledge.

Given the following list of questions, and using the document provided below, provide precise and comprehensive answers that demonstrate expertise and address the key concepts from the beginning, middle, and end of the document. Ensure that no important aspect of the material is overlooked, and that both the breadth and depth of understanding are reflected in your responses. You must answer from the document, and the answer needs to be provided in the document.

DOCUMENT:
{document}
QUESTIONS:
{questions}

Your answers should reflect your deep understanding and adhere to your characteristic approach. 
Analyze each question carefully and provide as many details as needed. 
There are no irrelevant questions, so respond thoroughly to every question. 
Don't forget any question and generate a complete list of all questions and all answers. 
You must answer from the document.
You must answer from the document.

DON'T ADD INTRODUCTORY PARAGRAPHS NOR OUTRODUCTORY PARAGRAPHS JUST PROVIDE QUESTIONS AND ANSWERS.
"""

def query_openai_question(prompt):
    try:
        response = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": prompt,
            }],
            model=MODEL_NAME,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return ''

def process_video(youtube_url):
    document, result = extract_knowledge(youtube_url)
    if not document:
        return None, result
    
    with st.spinner("Extracting knowledge..."):
        questions = query_openai_question(create_question_prompt(document))
    
    with st.spinner("Preparing QA-catalogue..."):
        qa_catalogue = query_openai_question(create_answer_prompt(document, questions))
    
    data = {
        "questions": questions,
        "qa_catalogue": qa_catalogue
    }
    
    return data, "Done analyzing the video!"

# Add this helper function at the top of your script
def text_to_clipboard(text):
    st.write(f'<p hidden>{text}</p>', unsafe_allow_html=True)
    st.markdown("""
    <script>
        const text = document.querySelector('p[hidden]').textContent;
        navigator.clipboard.writeText(text);
    </script>
    """, unsafe_allow_html=True)

# Custom CSS for a more modern look
st.markdown("""
<style>
    .stButton > button {
        width: 100%;
        background-color: #0b5351;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border: none;
        border-radius: 4px;
        transition-duration: 0.4s;
    }
    .stButton > button:hover {
        background-color: #0b5351;
    }
    .stSpinner > div {
        text-align: center;
        color: #9ac5d3;
    }
</style>
""", unsafe_allow_html=True)

st.title("Knowledge Extractor")

# Initialize session state
if 'extraction_complete' not in st.session_state:
    st.session_state.extraction_complete = False
if 'document' not in st.session_state:
    st.session_state.document = ""

# YouTube URL input
youtube_url = st.text_input("Enter YouTube URL", key="youtube_url")

# Extract Knowledge button
if st.button("Extract Knowledge", key="extract"):
    if youtube_url:
        data, result = process_video(youtube_url)
        if data:
            st.success(result)
            st.session_state.extraction_complete = True
            
            st.markdown(data['questions'])

            # Store the QA catalogue in session state
            st.session_state.qa_catalogue = data['qa_catalogue']

            # Move the Reveal Answers button outside the if statement
        else:
            st.error(result)
    else:
        st.warning("Please enter a YouTube URL")

# Reveal Answers button (outside the previous if statement)
if st.session_state.get('extraction_complete', False):
    if st.button("Reveal Answers", key="reveal_answers"):
        st.subheader("QA Catalogue")
        st.markdown(st.session_state.qa_catalogue)

# Add some space
st.markdown("<br>", unsafe_allow_html=True)

# Display extraction status
extraction_status = st.empty()
