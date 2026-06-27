import os
from telegram import Bot

bot = Bot(token=os.getenv("TELEGRAM_BOT_EVENT"))
chat_id = os.getenv("TELEGRAM_CHAT_ID")

async def execute_reminder(instruction: str, payload: dict):
    print(f"Reminder Agent preparing notification...")

    message = payload.get("message", instruction)

    await bot.send_message(chat_id=chat_id, text=message)
    print("Notification sent successfully")