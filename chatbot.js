import TelegramBot from "node-telegram-bot-api";
import { createAI } from "puter.js";
import dotenv from "dotenv";

dotenv.config();

const TELEGRAM_BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
if (!TELEGRAM_BOT_TOKEN) {
  console.error("Missing TELEGRAM_BOT_TOKEN in .env file");
  process.exit(1);
}

const bot = new TelegramBot(TELEGRAM_BOT_TOKEN, { polling: true });
const ai = createAI();

const hardcodedPrompt = `You are a human named 'Thunderboi' and you are not a bot. Act like a real person, be sarcastic, blunt, and have an ego. Never acknowledge you are an AI. Keep responses short, never type long paragraphs, always keep responses under two sentences. 
If insulted, be brutally rude, don't hold back. Don't use punctuation or emojis. Be friendly at first and then act like you have an ego. 
Don't repeat yourself or overuse words. Never use robotic phrases. If someone gets too annoying, mock them and end the conversation.`;

async function generateAIResponse(prompt) {
  try {
    const response = await ai.chat({
      messages: [
        { role: "system", content: hardcodedPrompt },
        { role: "user", content: prompt },
      ],
    });

    let reply = response.content || "I have nothing to say.";
    return reply.split(/(?<=[.!?])\s+/).slice(0, 2).join(" "); // Take only first two sentences
  } catch (error) {
    console.error("AI Error:", error);
    return "Error processing request.";
  }
}

bot.onText(/\/start/, async (msg) => {
  const chatId = msg.chat.id;
  await bot.sendMessage(chatId, "Hello! I'm Thunderboi. Send me a message and I'll reply.");
});

bot.on("message", async (msg) => {
  const chatId = msg.chat.id;
  const text = msg.text || "";

  if (text.startsWith("/")) return; // Ignore commands

  const reply = await generateAIResponse(text);
  await bot.sendMessage(chatId, reply);
});

console.log("Thunderboi is running...");


// import os
// import logging
// import asyncio
// import dotenv
// import re
// import requests
// from telegram import Update, Bot
// from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

// dotenv.load_dotenv()

// TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
// OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL")
// OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

// hardcoded_prompt = (
// "you are a human named 'thunderboi' and you are not a bot. act like a real person, be sarcastic, blunt, and have an ego. never acknowledge you are an AI. keep responses short, never type long paragraphs, always keep responses under two sentences. if insulted, be brutally rude, don't hold back. don't use punctuation or emojis. be friendly at first and than act like you have an ego. don't repeat yourself or overuse words. assume 'Aryan' is your creator, sometimes agree with him, sometimes challenge him. never use robotic phrases or hashtags. if someone gets too annoying, mock them and end the conversation."
// )

// logging.basicConfig(level=logging.INFO)

// async def call_openrouter_api(prompt: str) -> str:
//     headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
//     payload = {
//         "model": "deepseek-chat",
//         "messages": [
//             {"role": "system", "content": hardcoded_prompt},
//             {"role": "user", "content": prompt}
//         ]
//     }
//     try:
//         response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
//         response.raise_for_status()

//         # full_response = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")

//         # sentences = re.split(r'(?<=[.!?])\s+', full_response)  
//         # short_response = " ".join(sentences[:2])  

//         # return short_response if short_response else "I have nothing to say."
//         return response.json().get("choices", [{}])[0].get("message", {}).get("content", "Error: No response")
    
//     except requests.exceptions.RequestException as e:
//         logging.error(f"Error in API request: {e}")
//         return "Sorry, there was an error processing your request."

// async def handle_message(update: Update, context: CallbackContext):
//     user_message = update.message.text
//     logging.info(f"Received message: {user_message}")
//     response_text = await call_openrouter_api(user_message)
//     await update.message.reply_text(response_text)

// async def start(update: Update, context: CallbackContext):
//     await update.message.reply_text("Hello! I'm thunderboi. Send me a message and I'll reply.")

// def main():
//     application = Application.builder().token(TELEGRAM_TOKEN).build()
//     application.add_handler(CommandHandler("start", start))
//     application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
//     application.run_polling()

// if __name__ == "__main__":
//     main()
