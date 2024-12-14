from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

history = []

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    response = handle_ai_response(text)
    await update.message.reply_text(response)

def handle_ai_response(user_input: str) -> str:
    global history
    chat_session = model.start_chat(history=history)
    response = chat_session.send_message(user_input)
    model_response = response.text

    history.append({"role": "user", "parts": [user_input]})
    history.append({"role": "model", "parts": [model_response]})

    return model_response

async def webhook(request):
    update = Update.de_json(request.json, bot)
    await handle_message(update)

if __name__ == '__main__':
    app.run()
