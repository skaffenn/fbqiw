from aiogram import types, F, Router
from aiogram.filters import CommandStart
from functions import determine_mood, log_action

router = Router()


@router.message(CommandStart())
async def starting(message: types.Message):
    id_usr = str(message.from_user.id)
    await message.answer("Привет. Пришли мне фотографию человека и я определю его настроение на ней")
    await log_action(id_usr, "bot_start")


@router.message(F.photo)
async def handle_photo(message: types.Message):
    id_usr = str(message.from_user.id)
    await log_action(id_usr, "photo_sent")
    mood_description = await determine_mood(message)
    await message.answer(mood_description)

