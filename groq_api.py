import os
import httpx
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
AI_PROMPT = os.getenv("AI_PROMPT", "Create a short, stream-friendly quest that any streamer (VTuber or not) can perform live — whether they are gaming, chatting, or streaming in real life. The quest should not depend on a specific game or platform. Keep the quest neutral, practical, and under 20 lines. It should involve tasks or goals the streamer can act out or complete naturally during their stream, without needing to copy or paste anything into chat or games. any name written with out a special name like Oliver the Moderator is the streamer like help lumizap free the moderator oliver means lumizap is the streamer and most important keep the quest on max 20 lines")

async def generate_quest(idea: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"{AI_PROMPT}\n\"{idea}\""

    json_data = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=json_data,
                timeout=30.0
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error calling GROQ API: {e}")
            return "Failed to generate quest. Please try again later."
