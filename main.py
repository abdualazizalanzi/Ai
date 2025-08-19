from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai

TELEGRAM_TOKEN = "8142897497:AAHkRSwKlJei4m42Ij9N1f7_OKcbl_vfWHA"
OPENAI_API_KEY = "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"

openai.api_key = OPENAI_API_KEY

# نخزن المحادثات لكل قروب
chat_history = {}  # key = chat_id, value = list of messages

async def reply_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_message = update.message.text

    # إذا ما فيه تاريخ محادثة للقروب، نعمل قائمة جديدة
    if chat_id not in chat_history:
        chat_history[chat_id] = []

    # نضيف رسالة المستخدم
    chat_history[chat_id].append({"role": "user", "content": user_message})

    # نرسل كل المحادثة لـ OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history[chat_id]
    )

    ai_reply = response["choices"][0]["message"]["content"]

    # نضيف رد البوت للمحادثة
    chat_history[chat_id].append({"role": "assistant", "content": ai_reply})

    # نرسل الرد للقروب
    await update.message.reply_text(ai_reply)

# أمر /last يرسل آخر رسالة فقط
async def send_last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id in chat_history and chat_history[chat_id]:
        last_msg = chat_history[chat_id][-1]["content"]
        await update.message.reply_text(f"Last message:\n{last_msg}")
    else:
        await update.message.reply_text("No messages yet.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # الرد على أي رسالة
    app.add_handler(MessageHandler(filters.TEXT, reply_message))
    # أمر /last
    app.add_handler(CommandHandler("last", send_last))

    app.run_polling()

if __name__ == "__main__":
    main()
