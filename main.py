import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import openai
import asyncio

# تفعيل اللوج
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# التوكنات
TELEGRAM_TOKEN = "8142897497:AAHkRSwKlJei4m42Ij9N1f7_OKcbl_vfWHA"
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

# الرد على الرسائل
async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text.lower() == "az":
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "رد على az بشكل لطيف"}],
            max_tokens=100
        )
        reply_text = response.choices[0].message.content
        await update.message.reply_text(reply_text)

# تشغيل البوت
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply))
    
    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
