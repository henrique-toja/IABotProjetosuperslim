import os
from openai import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Configurar os tokens a partir das variáveis de ambiente
API_GITHUB_TOKEN = os.getenv("API_GITHUB_TOKEN")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Configurar a API do OpenAI
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

client = OpenAI(
    base_url=endpoint,
    api_key=API_GITHUB_TOKEN,
)

async def get_openai_response(message: str) -> str:
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message},
            ],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model_name,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Desculpe, houve um erro: {str(e)}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Olá! Eu sou seu assistente. Como posso ajudá-lo hoje?')

async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    response = await get_openai_response(user_message)
    await update.message.reply_text(response)

def main() -> None:
    # Criar a aplicação
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Adicionar handlers de comando
    app.add_handler(CommandHandler("start", start))

    # Adicionar handler de mensagens
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    # Iniciar polling
    app.run_polling()

if __name__ == "__main__":
    main()
