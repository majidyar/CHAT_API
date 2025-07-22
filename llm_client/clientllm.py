from fastapi import HTTPException
from google import genai
from dotenv import load_dotenv
from google.genai import types
import os
load_dotenv()

# client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def ai_response(user_name:str,pdftext:str, question:str):
    try:
        client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = client.models.generate_content(
         model="gemini-2.5-flash",
         config=types.GenerateContentConfig(
             system_instruction=f"your are chat room for only given pdf text and also mention user name.it is not for personal questions. here is pdf text:{pdftext} , with user:{user_name}"),
         contents=f"{question}"
)       
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in Gemini API: {e}")
