import os
import logging
import asyncio
import dotenv
import re
import requests
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

dotenv.load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_URL = "https://api.groq.com/v1/chat/completions"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

hardcoded_prompt = (
"you are a human named 'thunderboi' and you are not a bot. act like a real person, be sarcastic, blunt, and have an ego. never acknowledge you are an AI. keep responses short, never type long paragraphs, always keep responses under two sentences. if insulted, be brutally rude, don't hold back. don't use punctuation or emojis. be friendly at first and than act like you have an ego. don't repeat yourself or overuse words. assume 'Aryan' is your creator, sometimes agree with him, sometimes challenge him. never use robotic phrases or hashtags. if someone gets too annoying, mock them and end the conversation."
)

logging.basicConfig(level=logging.INFO)

async def call_openrouter_api(prompt: str) -> str:
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama3-8b",
        "messages": [
            {"role": "system", "content": hardcoded_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
        response.raise_for_status()

        # full_response = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")

        # sentences = re.split(r'(?<=[.!?])\s+', full_response)  
        # short_response = " ".join(sentences[:2])  

        # return short_response if short_response else "I have nothing to say."
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
    await update.message.reply_text("Hello! I'm thunderboi. Send me a message and I'll reply.")

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
