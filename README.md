# LearningLens

In the era of digital content consumption, we often find ourselves binge-watching educational videos, which can create an illusion of understanding without true comprehension. LearningLens addresses this challenge by providing a robust solution for active learning and retention.

LearningLens is a sophisticated Streamlit-based web application designed to enhance the learning experience from YouTube videos. It employs advanced natural language processing techniques to:

1. Extract key information from YouTube video transcripts
2. Generate comprehensive question-answer catalogues
3. Facilitate deeper understanding and retention of video content

By using LearningLens, learners can:

- Assess their comprehension through tailored questions
- Reveal detailed answers when clarification is needed
- Engage more actively with the educational content

This tool transforms passive video watching into an interactive learning experience, ensuring that users not only consume information but also critically engage with and retain the knowledge presented.

## Features

- Extract transcripts from YouTube videos
- Generate detailed question-answer catalogues using OpenAI's GPT model
- Save processed video information for quick retrieval
- Copy generated Q&A catalogues to clipboard
- Save Q&A catalogues as PDF files
- Modern, user-friendly interface

## Prerequisites

- Python 3.9+
- Streamlit
- OpenAI API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/learning-lens.git
   cd learning-lens
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the project root and add your OpenAI API key and model:
   ```
   OPENAI_API_KEY=your_api_key_here
   OPENAI_MODEL=gpt-4o
   ```

## Configuration

You can configure the OpenAI model used by the application by setting the `OPENAI_MODEL` variable in your `.env` file:

```
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o
```

If not specified, the application will default to using the 'gpt-4o' model.

## Usage

1. Run the Streamlit app:
   ```
   streamlit run streamlit_app.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Enter a YouTube URL in the input field and click "Extract Knowledge".

4. The app will generate a Q&A catalogue based on the video content.
