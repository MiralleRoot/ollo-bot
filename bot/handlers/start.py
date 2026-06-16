from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я oLLo — точнее, пока меня зовут Miralle.\n\n"
        "Я помогу тебе планировать дела и буду рядом, чтобы напоминать о важном.\n\n"
        "Как тебя зовут?"
    )