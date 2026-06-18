from aiogram import Router, types, F
from bot.services.ai_service import get_ai_response, extract_task_intent
from bot.services.task_service import add_task

router = Router()

@router.message(F.text)
async def handle_text(message: types.Message):
    await message.bot.send_chat_action(message.chat.id, "typing")

    task_data = await extract_task_intent(message.text)

    if task_data:
        task = add_task(
            user_id=message.from_user.id,
            title=task_data["title"],
            deadline=task_data["deadline"]
        )
        deadline_str = task["deadline"].strftime("%d.%m в %H:%M") if task["deadline"] else "без срока"
        await message.answer(f"Записал: «{task['title']}» — {deadline_str}.")
        return

    response = await get_ai_response(message.from_user.id, message.text)
    await message.answer(response)