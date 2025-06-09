from dotenv import load_dotenv
import os

load_dotenv()

print("Anthropic:", os.getenv("ANTHROPIC_API_KEY")[:10])
print("OpenAI:", os.getenv("OPENAI_API_KEY")[:10])
print("Gemini:", os.getenv("GOOGLE_API_KEY")[:10])
