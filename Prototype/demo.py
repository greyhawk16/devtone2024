from openai import OpenAI
import openai
import json
from dotenv import load_dotenv
import os

load_dotenv()

# API 예제
API_KEY = os.getenv("OPENAI_API_KEY_2")

# Define the prompt you want to send

client = OpenAI()
OpenAI.api_key = API_KEY

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "당신은 텍스트 게임 진행자 입니다."},
        {
            "role": "user",
            "content": "Introduce yourself and tell me how you can help me today.",
        }
    ]
)

print(completion.choices[0].message.content)
