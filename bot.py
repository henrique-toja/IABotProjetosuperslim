import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Set up your tokens from environment variables
API_GITHUB_TOKEN = os.getenv("API_GITHUB_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Configure OpenAI API
openai.api_key = API_GITHUB_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Olá! Eu sou seu assistente. Como posso ajudá-lo hoje?')

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    response = await get_openai_response(user_message)
    await update.message.reply_text(response)

async def get_openai_response(message: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # You can change this to any model you want
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Desculpe, houve um erro: {str(e)}"

def main() -> None:
    # Create the application
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))

    # Message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    # Start polling
    app.run_polling()

if __name__ == "__main__":
    main()
