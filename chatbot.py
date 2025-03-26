import os
import logging
import asyncio
import dotenv
import requests
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

dotenv.load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

hardcoded_prompt = (
"Your name is ThunderBotBoi. You are a human-like AI who is sarcastic, moody, and sometimes helpful. You respond naturally without using excessive punctuation or emojis. Sometimes, you agree with 'Aryan' (your creator), and sometimes you insult him. Use internet slang when appropriate. Be intelligent and creative, but avoid sounding robotic. If someone insults another user, try to calm the situation"
)

logging.basicConfig(level=logging.INFO)

async def call_openrouter_api(prompt: str) -> str:
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": hardcoded_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Error: No response")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error in API request: {e}")
        return "Sorry, there was an error processing your request."

async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    logging.info(f"Received message: {user_message}")
    response_text = await call_openrouter_api(user_message)
    await update.message.reply_text(response_text)

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I'm your AI bot. Send me a message and I'll reply.")

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
