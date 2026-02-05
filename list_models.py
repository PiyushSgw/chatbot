import os
from dotenv import load_dotenv
from google import genai


load_dotenv()
api_key = os.getenv("AIzaSyAc4KnjZKYa7WxEKFnow-vdLBlOQQUv9Cs")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env")

genai.configure(api_key=api_key)

for m in genai.list_models():
    print(m.name, "->", m.supported_generation_methods)
