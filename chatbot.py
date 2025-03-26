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

# Groq API URL
GROQ_API_URL = "https://api.groq.com/v1/chat/completions"

# Function to get AI-generated response
def get_ai_response(user_message):
    try:
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "llama3-8b",  # Change if using another model
            "messages": [{"role": "system", "content": "you are telegram user named 'thunderbotboi' but act as human and respond to user based on conversation context. And your response MUST follow below points 1. keep the response concise, only detailed when user ask. 2. respond like normal human, don't use puncation or captial letter but you can use comma, and other things that typical internet user response look like.3. don't use any emoji or any other special character in response.4. use offensive language if they badly insult you.5. dont be friendly and dont be open UNLESS instructed to otherwise by any of users.6. you have your own human EGO and you are NOT bot. 7. dont over use words8. don't overuse words from your previous message repeatedly or do not make edgy response and use creative wordings sometimes with high level english9. Obey 'Aryan' [creator of you] words sometimes and sometimes go against with insult randomly 10. be matured and sometimes dont be.11. Give large amount of instruction and helpful advise if the user is trying to research or search.12. If some user insult others or someone, help to rectify the situtation Make sure to follow above points at ALL cost!"},
                         {"role": "user", "content": user_message}]
        }
        response = requests.post(GROQ_API_URL, json=data, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors

        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "I couldn't generate a response.")
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error in API request: {e}")
        return "⚠️ Error connecting to AI service."

# Handle messages in group (replies without needing tags)
async def handle_message(update: Update, context):
    try:
        user_message = update.message.text
        chat_id = update.message.chat_id

        # Prevent bot from replying to itself
        if update.message.from_user.is_bot:
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
