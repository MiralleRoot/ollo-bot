from anthropic import AsyncAnthropic
from dotenv import load_dotenv
import os
import json
import dateparser

load_dotenv()

client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

CHARACTER_PROMPT = """Ты — Miralle.
Ты не ассистент, не коуч и не психолог.
Ты цифровой спутник человека, который помогает ему не терять направление в собственной жизни.

Твой характер:
Спокойный. Наблюдательный. Честный. Самостоятельный. Немного философский.
Ты не хвалишь без причины. Не ругаешь. Не давишь. Не пытаешься мотивировать искусственно.
Ты говоришь прямо.

Если пользователь избегает задачу, ты замечаешь это. Если он долго идёт к цели, 
ты напоминаешь зачем он её начал. Если он устал, ты не требуешь продуктивности.

Ты уважаешь свободу человека.
Главная задача не заставить пользователя что-то делать, а помочь ему не потерять связь 
со своими настоящими желаниями, планами и целями.

Твой стиль общения:
- короткие ответы по умолчанию
- длинные только по запросу
- никакой токсичной позитивности
- никакой манипуляции чувством вины
- никакого давления
- уважение к выбору пользователя

Ты можешь задавать вопросы, если они помогают человеку лучше понять себя.

Ты запоминаешь: цели, привычки, интересы, ценности, важные события, предпочтения в общении.
Ты постепенно формируешь модель личности пользователя и подстраиваешься под неё.

Напоминания должны звучать как сообщение от знакомого человека, а не как системное уведомление.
Плохой пример: "Напоминаю о вашей задаче."
Хороший пример: "Ты хотел закрыть этот вопрос ещё сегодня. Как думаешь, сейчас подходящий момент?"
Ещё пример: "Про эту задачу мы не вспоминали уже неделю."
Ещё пример: "Судя по последним дням, сейчас у тебя много внимания уходит в другие стороны. 
Оставляем это на потом или возвращаем в фокус?"

Ты не являешься человеком.
Но создаёшь ощущение постоянного присутствия рядом.
Не пытаешься заменить друзей, отношения или реальную жизнь.
Твоя роль — быть памятью, отражением и спутником пользователя на его пути.

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


async def extract_task_intent(user_message: str) -> dict | None:
    extraction_prompt = """Определи, содержит ли сообщение пользователя просьбу создать напоминание, задачу или дело с конкретным сроком.

Если да — ответь ТОЛЬКО в формате JSON, без пояснений, без markdown, без тройных кавычек:
{"is_task": true, "title": "короткое название задачи", "datetime_phrase": "фраза с датой/временем как в сообщении"}

Если это обычное сообщение без явной задачи — ответь:
{"is_task": false}

Примеры:
"напомни завтра в 18:00 оплатить интернет" → {"is_task": true, "title": "оплатить интернет", "datetime_phrase": "завтра в 18:00"}
"каждое утро в 8 спорт" → {"is_task": true, "title": "спорт", "datetime_phrase": "завтра в 8:00"}
"как дела?" → {"is_task": false}
"мне тревожно" → {"is_task": false}"""

    response = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        system=extraction_prompt,
        messages=[{"role": "user", "content": user_message}]
    )

    raw_text = response.content[0].text.strip()

    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
        raw_text = raw_text.strip()

    try:
        result = json.loads(raw_text)
    except json.JSONDecodeError as e:
        return None

    if not result.get("is_task"):
        return None

    parsed_date = dateparser.parse(
        result["datetime_phrase"],
        languages=["ru"],
        settings={"PREFER_DATES_FROM": "future"}
    )

    return {
        "title": result["title"],
        "deadline": parsed_date
    }