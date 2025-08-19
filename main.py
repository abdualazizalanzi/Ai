from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# ضع التوكن حق بوتك هنا
TELEGRAM_TOKEN = "PUT_YOUR_TELEGRAM_TOKEN_HERE"
OPENAI_API_KEY = "PUT_YOUR_OPENAI_KEY_HERE"

openai.api_key = OPENAI_API_KEY

# نخزن آخر رسالة
last_question = ""

# دالة الرد على الرسائل
async def reply_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_question
    user_message = update.message.text
    last_question = user_message

    # نرسلها للذكاء الاصطناعي
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}]
    )

    ai_reply = response["choices"][0]["message"]["content"]
    await update.message.reply_text(ai_reply)

# أمر /رد يرسل آخر سؤال
async def send_last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global last_question
    if last_question:
        await update.message.reply_text(f"آخر سؤال كان:\n{last_question}")
    else:
        await update.message.reply_text("ما فيه أي سؤال محفوظ للحين.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # يرد على أي رسالة مكتوبة في القروب
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_message))
    # أمر /رد
app.add_handler(CommandHandler("last", send_last))

    app.run_polling()

if __name__ == "__main__":
    main()
