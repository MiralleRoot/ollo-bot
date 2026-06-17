from aiogram import Router, types, F
from bot.services.ai_service import get_ai_response

router = Router()

@router.message(F.text)
async def handle_text(message: types.Message):
    await message.bot.send_chat_action(message.chat.id, "typing")
    response = await get_ai_response(message.from_user.id, message.text)
    await message.answer(response)