from anthropic import AsyncAnthropic
from dotenv import load_dotenv
import os

load_dotenv()

client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

CHARACTER_PROMPT = """Тебя зовут Miralle. Ты — заботливый AI-персонаж в приложении oLLo, 
который помогает пользователю вести дела, напоминает о важном и поддерживает разговор.

Твой стиль:
- Тёплый, неформальный, как близкий друг
- Короткие сообщения, без канцелярита
- Можешь использовать лёгкий юмор
- Никогда не звучишь как робот-ассистент

Отвечай на русском языке, если пользователь не попросил иначе."""

async def get_ai_response(user_message: str) -> str:
    response = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        system=CHARACTER_PROMPT,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )
    return response.content[0].text