from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, filters, CallbackContext
import os 
BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = Bot(token=BOT_TOKEN)
CHAT_ID = os.getenv('CHAT_ID')
async def get_chat_id(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    print(f"Group Chat ID: {chat_id}")
    await update.message.reply_text(f"The chat ID for this group is: {chat_id}")

async def send_messages():
    bot.send_message(chat_id=CHAT_ID, text="Hello! This is a scheduled message.")



# async def main():
#     # Create an application with your bot token
#     application = Application.builder().token(TOKEN).build()

#     # Add a handler for any message
#     application.add_handler(MessageHandler(filters.TEXT, get_chat_id))

#     # Start polling
#     await application.start_polling()

# if __name__ == '__main__':
#     import asyncio
#     asyncio.run(main())