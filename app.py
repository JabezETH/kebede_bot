

import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
username = os.getenv('TELEGRAM_USERNAME')
import os
import json
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Define states for the conversation
ASK_NAME, ASK_AGE, ASK_PHONE, ASK_ADDRESS, ASK_PHOTO = range(5)

# Specify the folder to save images and data
SAVE_FOLDER = "data"
os.makedirs(SAVE_FOLDER, exist_ok=True)


# Temporary dictionary to hold user data
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Initiate the conversation and ask for the user's name."""
    await update.message.reply_text("Hi! What's your name?")
    return ASK_NAME

async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store name and ask for age."""
    user_data['name'] = update.message.text
    await update.message.reply_text("Great! What's your age?")
    return ASK_AGE

async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store age and ask for phone number."""
    user_data['age'] = update.message.text
    await update.message.reply_text("What's your phone number?")
    return ASK_PHONE

async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store phone number and ask for address."""
    user_data['phone'] = update.message.text
    await update.message.reply_text("What's your address?")
    return ASK_ADDRESS

async def ask_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store address and ask for a photo."""
    user_data['address'] = update.message.text
    await update.message.reply_text("Please take a picture and send it to me.")
    return ASK_PHOTO

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save the photo and user data in a JSON file."""
    user_name = user_data['name']
    photo_file = await update.message.photo[-1].get_file()
    photo_path = f"{SAVE_FOLDER}/{user_name}.jpg"
    await photo_file.download_to_drive(photo_path)

    # Save the user data as a JSON file
    json_path = f"{SAVE_FOLDER}/{user_name}.json"
    with open(json_path, "w") as f:
        json.dump(user_data, f)

    await update.message.reply_text("Thank you! Your information and photo have been saved.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle cancellation."""
    await update.message.reply_text("Process cancelled.")
    return ConversationHandler.END

def main():
    """Start the bot."""
    application = Application.builder().token(BOT_TOKEN).build()

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

    # Add conversation handler to the application
    application.add_handler(conv_handler)

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
