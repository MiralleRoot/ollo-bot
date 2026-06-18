from aiogram import Router, types
from aiogram.filters import Command
from bot.services.task_service import get_tasks

router = Router()

@router.message(Command("tasks"))
async def cmd_tasks(message: types.Message):
    tasks = get_tasks(message.from_user.id)

    if not tasks:
        await message.answer("Пока ничего не записано.")
        return

    lines = []
    for task in tasks:
        status = "✓" if task["done"] else "○"
        deadline_str = task["deadline"].strftime("%d.%m %H:%M") if task["deadline"] else "без срока"
        lines.append(f"{status} {task['title']} — {deadline_str}")

    await message.answer("\n".join(lines))