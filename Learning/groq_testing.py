import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
  api_key=os.environ.get("GROQ_API_KEY")
)


chat_completion = client.chat.completions.create(
  messages =[
    {
      "role":"user",
      "content" : "What is the significance of LLMS?"
    }
  ],model="openai/gpt-oss-20b"
)

print(chat_completion.choices[0].message.content)


