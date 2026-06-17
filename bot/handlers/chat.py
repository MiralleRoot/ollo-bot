from aiogram import Router, types, F
from bot.services.ai_service import get_ai_response

router = Router()

@router.message(F.text)
async def handle_text(message: types.Message):
    await message.chat.do("typing")
    response = await get_ai_response(message.text)
    await message.answer(response)