import os
from flask import Flask, request
from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0, use_context=True)

user_data = {}
user_step = {}

districts = [
    "Angor", "Bandixon", "Boysun", "Denov", "Jarqoʻrgʻon", "Muzrabot", "Oltinsoy",
    "Qiziriq", "Sariosiyo", "Sherobod", "Shoʻrchi", "Termiz", "Uzun", "Qumqoʻrgʻon"
]
district_keyboard = ReplyKeyboardMarkup([[d] for d in districts], resize_keyboard=True)

def start(update: Update, context):
    print("✅ /start ishladi!")  # log uchun
    chat_id = update.message.chat_id
    user_step[chat_id] = "tuman"
    user_data[chat_id] = {}
    update.message.reply_text("Assalomu alaykum! Tumanni tanlang:", reply_markup=district_keyboard)

def handle_message(update: Update, context):
    chat_id = update.message.chat_id
    text = update.message.text
    step = user_step.get(chat_id)

    if step == "tuman":
        user_data[chat_id]["tuman"] = text
        user_step[chat_id] = "fish"
        update.message.reply_text("F.I.SH. ni kiriting:")
    elif step == "fish":
        user_data[chat_id]["fish"] = text
        user_step[chat_id] = "phone"
        update.message.reply_text("Telefon raqamingizni kiriting:")
    elif step == "phone":
        user_data[chat_id]["phone"] = text
        user_step[chat_id] = "project"
        update.message.reply_text("Loyiha nomini kiriting:")
    elif step == "project":
        user_data[chat_id]["project"] = text
        user_step[chat_id] = "presentation"
        update.message.reply_text("📎 Taqdimot faylini yuboring (.pdf yoki .pptx):")

def handle_document(update: Update, context):
    chat_id = update.message.chat_id
    step = user_step.get(chat_id)

    if step == "presentation":
        user_data[chat_id]["presentation"] = update.message.document.file_id
        user_step[chat_id] = "planshet"
        update.message.reply_text("📄 Loyiha planshetini yuboring (pdf yoki rasm):")
    elif step == "planshet":
        user_data[chat_id]["planshet"] = update.message.document.file_id
        user_step[chat_id] = "photo"
        update.message.reply_text("🖼 3x4 fotosuratni yuboring:")
    elif step == "photo":
        user_data[chat_id]["photo"] = update.message.document.file_id
        send_to_admin(context, chat_id)
        update.message.reply_text("✅ Maʼlumotlaringiz adminga yuborildi. Rahmat!")
        user_step.pop(chat_id)
        user_data.pop(chat_id)

def handle_photo(update: Update, context):
    chat_id = update.message.chat_id
    step = user_step.get(chat_id)

    if step == "photo":
        user_data[chat_id]["photo"] = update.message.photo[-1].file_id
        send_to_admin(context, chat_id)
        update.message.reply_text("✅ Maʼlumotlaringiz adminga yuborildi. Rahmat!")
        user_step.pop(chat_id)
        user_data.pop(chat_id)

def send_to_admin(context, chat_id):
    data = user_data[chat_id]
    text = (
        f"🎂 Yangi ro‘yxatdan o‘tuvchi:
"
        f"📍 Tuman: {data['tuman']}
"
        f"👤 F.I.SH.: {data['fish']}
"
        f"📞 Tel: {data['phone']}
"
        f"🧪 Loyiha: {data['project']}"
    )
    context.bot.send_message(chat_id=ADMIN_ID, text=text)
    context.bot.send_document(chat_id=ADMIN_ID, document=data["presentation"], caption="📎 Taqdimot")
    context.bot.send_document(chat_id=ADMIN_ID, document=data["planshet"], caption="📄 Planshet")
    context.bot.send_photo(chat_id=ADMIN_ID, photo=data["photo"], caption="🖼 3x4 fotosurat")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
dispatcher.add_handler(MessageHandler(Filters.document, handle_document))
dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK"

@app.route("/")
def index():
    return "✅ Bot ishlayapti!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
