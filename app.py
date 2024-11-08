

import os
import requests
from dotenv import load_dotenv
import uuid 
load_dotenv()
import time
BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
username = os.getenv('TELEGRAM_USERNAME')
import os
import json
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from autorization import is_authorized
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# Define states for the conversation
import schedule
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

from database import start, ask_name, ask_age, ask_phone, ask_address, ask_address, handle_photo, cancel, view_data, search, find, remove
from send_message import get_chat_id, send_messages
CHAT_ID = os.getenv('CHAT_ID')



ASK_NAME, ASK_AGE, ASK_PHONE, ASK_ADDRESS, ASK_PHOTO, LOGIN_ID, LOGIN_PASS, VIEW_DATA, PRINT_DATA, SEARCH,DELETE = range(11)
SAVE_FOLDER = "data"
os.makedirs(SAVE_FOLDER, exist_ok=True)


with open(f"{SAVE_FOLDER}/user_db.json", "r") as f:
    existing_data = json.load(f)
user_ids = []
for ids in existing_data:
    user_ids.append(int(ids))
user_id = max(user_ids) + 1


# Temporary dictionary to hold user data
user_data = {}
# admin_data = {}
with open(f"{SAVE_FOLDER}/admin_data.json", "r") as f:
    admin_data = json.load(f)

bot = Bot(token=BOT_TOKEN)



async def send_message():
    await bot.send_message(chat_id=CHAT_ID, text="This is a scheduled message sent every minute.")
    print("Message sent successfully.")

def main():
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()
    # bot = Bot(token=BOT_TOKEN)
    # await bot.send_message(chat_id=CHAT_ID, text="Hello! This is a scheduled message.")
    # Define the conversation handler with states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)],
            ASK_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_age)],
            ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
            ASK_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_address)],
            ASK_PHOTO: [MessageHandler(filters.PHOTO, handle_photo)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    view_data_handler = ConversationHandler(
    entry_points=[CommandHandler("view_data", view_data)],  # Starts view_data process
    states={
    VIEW_DATA: [MessageHandler(filters.TEXT & ~filters.COMMAND, view_data)],  # Handle both admin ID and password
        # PRINT_DATA: [MessageHandler(filters.TEXT & ~filters.COMMAND, print_data)],  # Handle both admin ID and password
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
    delete_handler = ConversationHandler(
    entry_points=[CommandHandler("search", search)],  # Starts view_data process
    states={
    DELETE: [MessageHandler(filters.TEXT & ~filters.COMMAND, find)],  # Handle both admin ID and password
},
    fallbacks=[CommandHandler("cancel", cancel)],
)
    search_handler = ConversationHandler(
    entry_points=[CommandHandler("search", search)],  # Starts view_data process
    states={
    SEARCH: [MessageHandler(filters.TEXT & ~filters.COMMAND, find)],  # Handle both admin ID and password
},
    fallbacks=[CommandHandler("cancel", cancel)],
)


    # application.add_handler(send_scheduled_message)
    # Add conversation handler to the application
    application.add_handler(conv_handler)
    # application.add_handler(CommandHandler("view_data", view_data))  # Add command to view user data
    application.add_handler(view_data_handler)
    # application.add_handler(MessageHandler(filters.TEXT, get_chat_id))
    application.add_handler(search_handler)
    # Start the bot
    application.run_polling()
 
    
    # scheduler = AsyncIOScheduler()
    # scheduler = BlockingScheduler()
    # Schedule the job every 12 hours, for example
    # scheduler.add_job(send_messages, 'interval', minutes=1)
    # scheduler.start()
if __name__ == "__main__":
    main()
    # send_message()

    # # Keep the script running
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
