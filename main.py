import logging
import os
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import openai

# ========================
# إعداد اللوج
# ========================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ========================
# التوكنات
# ========================
TELEGRAM_TOKEN = "8142897497:AAHkRSwKlJei4m42Ij9N1f7_OKcbl_vfWHA"
OPENAI_API_KEY = "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"
WEBHOOK_URL = "https://ai-8-djr8.onrender.com/"  # رابط مشروعك على Render

openai.api_key = OPENAI_API_KEY

# ========================
# دالة الرد على الرسائل
# ========================
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

# ========================
# تشغيل البوت باستخدام webhook
# ========================
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), reply))

    # حذف أي ويب هوك قديم
    bot = Bot(TELEGRAM_TOKEN)
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)

    # تشغيل السيرفر
    port = int(os.environ.get("PORT", 8080))
    await app.run_webhook(
        listen="0.0.0.0",
        port=port,
        webhook_url=WEBHOOK_URL
    )

# ========================
# نقطة البداية
# ========================
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
