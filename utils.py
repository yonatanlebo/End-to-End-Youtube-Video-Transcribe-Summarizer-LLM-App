# הסרה של google.generativeai וייבוא של localai במקום
# (נניח שיש לך client של localAI מותקן)

from youtube_transcript_api import YouTubeTranscriptApi
from config import load_config
import requests  # localAI מתבקש פה

# load configuration
load_config()

# setup prompt
prompt = """You are Youtube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split('=')[1].split('&')[0]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ''
        for i in transcript_text:
            transcript += ' ' + i['text']

        return transcript

    except Exception as e:
        raise e


def generate_localai_content(transcript_text, prompt):
    """
    שולח את הפקודה ל-localAI דרך REST API
    - מניח שה-localAI רץ בכתובת http://localhost:8080
    """

    url = "http://localhost:8080/v1/chat/completions"  # תלוי בגרסה
    headers = {"Content-Type": "application/json"}

    data = {
        "model": "localai-model-name",  # תשנה לשם הדגם שלך ב-localAI
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt + transcript_text}
        ],
        "max_tokens": 500,
        "temperature": 0.7,
    }

    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    result = response.json()

    # במבנה תגובה סטנדרטי של OpenAI-compatible API
    return result['choices'][0]['message']['content']
