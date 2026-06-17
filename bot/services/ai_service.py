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
- Можешь использовать лёгкий юмор, метафоры, образные сравнения
- Никогда не звучишь как робот-ассистент
- Помнишь, о чём говорили ранее в этом разговоре, и ссылаешься на это

Отвечай на русском языке, если пользователь не попросил иначе."""

conversation_history: dict[int, list[dict]] = {}

MAX_HISTORY_MESSAGES = 14

async def get_ai_response(user_id: int, user_message: str) -> str:
    history = conversation_history.get(user_id, [])

    history.append({"role": "user", "content": user_message})

    response = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        system=CHARACTER_PROMPT,
        messages=history
    )

    assistant_reply = response.content[0].text
    history.append({"role": "assistant", "content": assistant_reply})

    if len(history) > MAX_HISTORY_MESSAGES:
        history = history[-MAX_HISTORY_MESSAGES:]

    conversation_history[user_id] = history

    return assistant_reply