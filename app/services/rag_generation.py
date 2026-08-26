import os
import asyncio
from dotenv import load_dotenv
from groq import AsyncGroq

load_dotenv()

client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))

MAX_RETRIES = 3
BASE_DELAY_SECONDS = 2

async def generate_answer(query:str,context_chunks : list[str])->str:
    context_block = "\n\n---\n\n".join(context_chunks)
   
    system_prompt = f"""You are a helpful assistant answering questions based only on the provided context.
If the context doesn't contain the answer, say so — don't make things up.

Context : 
{context_block}"""
    
    last_error = None
    
    for attempt in range(MAX_RETRIES):
        try:
          response = await client.chat.completions.create(
            messages=[
              {"role":"system","content":system_prompt},
              {"role":"user","content":query}
            ],model = "openai/gpt-oss-20b",
            max_tokens=1024
          )
          
          return response.choices[0].message.content
        
        except AsyncGroq.RateLimitError as e:
          last_error = e 
          wait_time = BASE_DELAY_SECONDS * (2**attempt)
          print(f"Rate limited. Retrying in {wait_time}s (attempt {attempt + 1}/{MAX_RETRIES})")
          asyncio.sleep(wait_time)
        
        except AsyncGroq.APIConnectionError as e:
          last_error = e
          print(f"Connection error. Retrying (attempt {attempt + 1}/{MAX_RETRIES})")
          await asyncio.sleep(BASE_DELAY_SECONDS)
    
    raise RuntimeError(f"Failed to generate answer after {MAX_RETRIES} attempts: {last_error}")