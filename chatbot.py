import logging
import requests
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, filters

# Load environment variables
load_dotenv()

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),  # Save logs to a file
        logging.StreamHandler()  # Print logs in console
    ],
)

# Read API keys from .env file
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = os.getenv("GROQ_API_URL")  # Default value if missing

# Function to get AI-generated response
def get_ai_response(user_message):
    try:
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "llama3-8b",
            "messages": [
                {"role": "system", "content": "Your name is ThunderBotBoi. You are a human-like AI who is sarcastic, moody, and sometimes helpful. You respond naturally without using excessive punctuation or emojis. Sometimes, you agree with 'Aryan' (your creator), and sometimes you insult him. Use internet slang when appropriate. Be intelligent and creative, but avoid sounding robotic. If someone insults another user, try to calm the situation."},
                {"role": "user", "content": user_message}
            ]
        }

        response = requests.post(GROQ_API_URL, json=data, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Log full API response for debugging
        logging.info(f"Groq API Response: {response.json()}")

        return response.json().get("choices", [{}])[0].get("text", "I couldn't generate a response.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error in API request: {e}")
        return "⚠️ Error connecting to AI service."

# Handle messages in group (replies without needing tags)
async def handle_message(update: Update, context):
    try:
        user_message = update.message.text
        chat_id = update.message.chat_id
        user_id = update.message.from_user.id

        # Prevent bot from replying to itself
        if update.message.from_user.is_bot or user_id == context.bot.id:
            return

        # AI response
        ai_reply = get_ai_response(user_message)
        
        # Reply normally
        await context.bot.send_message(chat_id=chat_id, text=ai_reply)

    except Exception as e:
        logging.error(f"Error handling message: {e}")

# Start bot
def main():
    try:
        app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        logging.info("Bot is running...")
        app.run_polling()

    except Exception as e:
        logging.critical(f"Fatal error in bot: {e}")

if __name__ == "__main__":
    main()
