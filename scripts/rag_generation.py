import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_answer(query:str,context_chunks : list[str])->str:
    context_block = "\n\n---\n\n".join(context_chunks)
   
    system_prompt = f"""You are a helpful assistant answering questions based only on the provided context.
If the context doesn't contain the answer, say so — don't make things up.

Context : 
{context_block}"""
    
    response = client.chat.completions.create(
      messages=[
        {"role":"system","content":system_prompt},
        {"role":"user","content":query}
      ],model = "openai/gpt-oss-20b",
      max_tokens=1024
    )
    
    return response.choices[0].message.content