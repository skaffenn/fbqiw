from concurrent.futures import ThreadPoolExecutor
from amplitude import Amplitude, BaseEvent
import base64
import requests
from aiogram import types, Bot
from data import config
import os

executor = ThreadPoolExecutor(max_workers=1)
amplitude_client = Amplitude(config.amplitude_api_key)
bot = Bot(token=config.bot_token)
api_key = config.openai_api_token


async def determine_mood(message: types.Message) -> str:
    photo_file_path = await download_image(message)
    base64_image = encode_image(photo_file_path)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Какое настроение у человека на фото?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    os.remove(photo_file_path)
    return response.json()['choices'][0]['message']['content']


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


async def download_image(message: types.Message):
    photo = message.photo[-1].file_id
    photo_file_path = f"cache/img{photo}.png"
    await bot.download(photo, destination=photo_file_path)
    return photo_file_path


def send_amplitude_event(user_id: str, event_type: str, event_properties: dict):
    def send_event_in_thread():
        event = BaseEvent(event_type=event_type, user_id=user_id, event_properties=event_properties)
        amplitude_client.track(event)
        executor.submit(send_event_in_thread)


async def log_user_action(user_id: str, action: str):
    event_type = "user_action"
    event_properties = {"action": action}
    send_amplitude_event(user_id, event_type, event_properties)