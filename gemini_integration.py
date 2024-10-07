from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def generate_summary(input_text: str) -> str:
    model = genai.GenerativeModel('gemini-1.5-pro')
    prompt = f"Summarize the following book content: {input_text}"
    response = model.generate_content([prompt])
    return response.text
