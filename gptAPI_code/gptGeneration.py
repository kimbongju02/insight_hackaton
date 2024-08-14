import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('API_KEY')

client = OpenAI(
  api_key=API_KEY
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