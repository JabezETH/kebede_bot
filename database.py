import os
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
import logging 
# Set up logging
logging.basicConfig(
    filename='bot_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filemode='w'
)


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


ASK_NAME, ASK_AGE, ASK_PHONE, ASK_ADDRESS, ASK_PHOTO, LOGIN_ID, LOGIN_PASS, VIEW_DATA, PRINT_DATA, SEARCH,DELETE = range(11)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.message.from_user.id):
        await update.message.reply_text("You are not authorized to use this bot.")
        logging.info(f"User: {update.message.from_user.full_name} ID: {update.message.from_user.id}")
        return ConversationHandler.END
    """Initiate the conversation and ask for the user's name."""
    logging.info(f"User: {update.message.from_user.full_name} ID: {update.message.from_user.id}")
    await update.message.reply_text("Hi! What's your name?")
    logging.info("Program Started...")
    logging.info("Asking user's name...")

    return ASK_NAME

async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store name and ask for age."""
    user_data['name'] = update.message.text.lower()
    await update.message.reply_text("Great! What's your age?")
    logging.info("Asking user's age...")
    return ASK_AGE

async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store age and ask for phone number."""
    user_data['age'] = update.message.text
    await update.message.reply_text("What's your phone number?")
    logging.info("Asking user's phone number...")
    return ASK_PHONE

async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store phone number and ask for address."""
    user_data['phone'] = update.message.text
    await update.message.reply_text("What's your address?")
    print("Asking user's address...")
    return ASK_ADDRESS

async def ask_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store address and ask for a photo."""
    user_data['address'] = update.message.text
    await update.message.reply_text("Please take a picture and send it to me.")
    print("Asking user's picture...")
    return ASK_PHOTO

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save the photo and user data in a JSON file."""
    user_name = user_data['name']
    photo_file = await update.message.photo[-1].get_file()
    photo_path = f"{SAVE_FOLDER}/{user_name}.jpg"
    await photo_file.download_to_drive(photo_path)

    # Save the user data as a JSON file
    json_path = f"{SAVE_FOLDER}/user_db.json" 


    if os.path.exists(json_path) and os.path.getsize(json_path) > 0:
        with open(json_path, "r") as f:
            try:
                existing_data = json.load(f)
                if existing_data is None:  # Handle case when the JSON file contains 'null'
                    existing_data = {}
            except json.JSONDecodeError:
                existing_data = {}  # If the JSON is invalid, initialize an empty dictionary
    else:
        existing_data = {}  # If the file doesn't exist or is empty, start with an empty dictionary

    # Add the user data under the generated unique ID
    existing_data[user_id] = user_data

    # Save the updated data back to the file
    with open(json_path, "w") as f:
        json.dump(existing_data, f, indent=4)  # `indent=4` for pretty-printing (optional)

    # Optionally, print or return the generated user_id to track it if needed
    print(f"Generated user ID: {user_id}")
    await update.message.reply_text("Thank you! Your information and photo have been saved.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle cancellation."""
    await update.message.reply_text("Process cancelled.")
    return ConversationHandler.END
    

async def view_data(update: Update, context: ContextTypes.DEFAULT_TYPE):

    for id, data in existing_data.items():
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(f"data/{data['name']}.jpg", 'rb'))
        await update.message.reply_text(f" name: {data['name']} phone: {data['phone']} address: {data['address']}")
        time.sleep(1)
    return ConversationHandler.END

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please provide a name")

    return SEARCH
async def find(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.lower()
    for id, data in existing_data.items():
        if name == data['name']:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(f"data/{data['name']}.jpg", 'rb'))
            await update.message.reply_text(f" name: {data['name']} phone: {data['phone']} address: {data['address']}")
            time.sleep(1)
            return ConversationHandler.END
    await update.message.reply_text("Sorry, I couldn't find that name. Please try again.")
    return SEARCH
# async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text("Please provide a name")
#     # name = update.message.text
#     # for id, data in existing_data.items():
#     #     if name == data['name']:
#     #         await context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(f"data/{data['name']}.jpg", 'rb'))
#     #         await update.message.reply_text(f" Name: {data['name']} Age: {data['age']} Phone: {data['phone']} Address: {data['address']}")
#     #         time.sleep(1)
#     return REMOVE
async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.lower()
    for id, data in existing_data.items():
        if name == data['name']:
            
            
            time.sleep(1)
            return ConversationHandler.END

    await update.message.reply_text("Sorry, I couldn't find that name. Please try again.")
    return SEARCH