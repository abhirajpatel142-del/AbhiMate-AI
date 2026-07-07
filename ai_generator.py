import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

def generate_content(topic, platform):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user",
                "content": f"""
Create viral content for:
Topic: {topic}
Platform: {platform}

Give:
- 10 video ideas
- 5 hooks
- 5 titles
- Description
- Hashtags
"""
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    result = response.json()

    return result["choices"][0]["message"]["content"]
def generate_script(topic):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a professional YouTube Shorts script writer.

Create a viral Shorts script for:

Topic: {topic}

Give:

1. Strong Hook (first 3 seconds)
2. Scene by scene script
3. Voiceover lines
4. Ending CTA

Make it engaging and around 30-60 seconds.
"""


    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }


    response = requests.post(
        url,
        headers=headers,
        json=data
    )


    result = response.json()

    return result["choices"][0]["message"]["content"]

def generate_thumbnail(topic):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are a YouTube thumbnail expert.

Create a clickable thumbnail idea for:

Topic: {topic}

Give:

1. Thumbnail Text (short and powerful)
2. Background Idea
3. Face Expression Idea
4. Main Object
5. Why people will click it
"""

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    result = response.json()

    return result["choices"][0]["message"]["content"]
