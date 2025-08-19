from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# توكن البوت
TELEGRAM_TOKEN = "8142897497:AAHkRSwKlJei4m42Ij9N1f7_OKcbl_vfWHA"

# مفتاح OpenAI
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

last_question = ""

async def reply_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_question
    user_message = update.message.text
    last_question = user_message

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}]
    )

    ai_reply = response["choices"][0]["message"]["content"]
    await update.message.reply_text(ai_reply)

async def send_last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_question
    if last_question:
        await update.message.reply_text(f"Last question was:\n{last_question}")
    else:
        await update.message.reply_text("No question has been sent yet.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # الرد على أي رسالة
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_message))
    # أمر /last
    app.add_handler(CommandHandler("last", send_last))

    app.run_polling()

if __name__ == "__main__":
    main()
