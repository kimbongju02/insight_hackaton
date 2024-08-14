import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
GPT_API_KEY = os.environ.get('GPT_API_KEY')

client = OpenAI(
  GPT_API_KEY=GPT_API_KEY
)

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is a LLM?"}
  ]
)
message = response.choices[0].message.content
print(message)