import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN") ADMIN_ID = os.getenv("ADMIN_ID")

regions = { "Toshkent": ["Bekobod", "Bo'ka", "Bo'stonliq", "Chinoz", "Qibray", "Ohangaron", "Oqqo'rg'on", "Parkent", "Piskent", "Toshkent tumani", "Yangiyo'l", "Zangiota"], "Andijon": ["Andijon shahri", "Asaka", "Baliqchi", "Bo'z", "Buloqboshi", "Izboskan", "Jalaquduq", "Kurgontepa", "Marhamat", "Oltinko'l", "Paxtaobod", "Shahrixon", "Ulug'nor", "Xo'jaobod"], "Farg'ona": ["Farg'ona shahri", "Beshariq", "Bog'dod", "Buvayda", "Dang'ara", "Furqat", "Qo'shtepa", "Oltiariq", "Quva", "Rishton", "So'x", "Toshloq", "Uchko'prik", "Yozyovon"], "Namangan": ["Namangan shahri", "Chortoq", "Chust", "Kosonsoy", "Mingbuloq", "Norin", "Pop", "To'raqo'rg'on", "Uchqo'rg'on", "Yangiqo'rg'on"], "Samarqand": ["Samarqand shahri", "Bulung'ur", "Ishtixon", "Jomboy", "Kattaqo'rg'on", "Narpay", "Nurobod", "Oqdaryo", "Paxtachi", "Payariq", "Pastdarg'om", "Tayloq", "Urgut"], "Buxoro": ["Buxoro shahri", "G'ijduvon", "Jondor", "Kogon", "Olot", "Peshku", "Qorako'l", "Qorovulbozor", "Romitan", "Shofirkon", "Vobkent"], "Qashqadaryo": ["Qarshi shahri", "Chiroqchi", "Dehqonobod", "G'uzor", "Kasbi", "Kitob", "Koson", "Mirishkor", "Muborak", "Nishon", "Shahrisabz", "Yakkabog'"], "Surxondaryo": ["Termiz shahri", "Angor", "Bandixon", "Boysun", "Denov", "Jarqo'rg'on", "Qiziriq", "Qo'mqo'rg'on", "Muzrabot", "Oltinsoy", "Sariosiyo", "Sherobod", "Sho'rchi", "Uzun"], "Jizzax": ["Jizzax shahri", "Arnasoy", "Baxmal", "Do'stlik", "Forish", "G'allaorol", "Mirzacho'l", "Paxtakor", "Yangiobod", "Zafarobod", "Zarbdor"], "Navoiy": ["Navoiy shahri", "Karmana", "Konimex", "Navbahor", "Nurota", "Qiziltepa", "Xatirchi", "Zarafshon"], "Sirdaryo": ["Guliston shahri", "Akaltyn", "Boyovut", "Guliston tumani", "Mirzaobod", "Oqoltin", "Sardoba", "Sayxunobod", "Sharof Rashidov", "Xovos"], "Xorazm": ["Urganch shahri", "Bog'ot", "Gurlan", "Hazorasp", "Khiva", "Qo'shko'pir", "Shovot", "Urganch tumani", "Xonqa", "Yangiariq", "Yangibozor"] }

user_data = {} user_step = {}

from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext): keyboard = [[region] for region in regions.keys()] reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True) update.message.reply_text("Viloyatingizni tanlang:", reply_markup=reply_markup) user_step[update.message.chat_id] = "region"

def handle_message(update: Update, context: CallbackContext): chat_id = update.message.chat_id text = update.message.text step = user_step.get(chat_id)

if step == "region":
    if text in regions:
        user_data[chat_id] = {"region": text}
        user_step[chat_id] = "district"
        keyboard = [[d] for d in regions[text]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        update.message.reply_text("Tumanni tanlang:", reply_markup=reply_markup)
    else:
        update.message.reply_text("Iltimos, ro'yxatdan viloyatni tanlang.")
elif step == "district":
    user_data[chat_id]["district"] = text
    update.message.reply_text("Ismingizni to‘liq kiriting:")
    user_step[chat_id] = "name"
elif step == "name":
    user_data[chat_id]["name"] = text
    update.message.reply_text("Telefon raqamingizni kiriting:")
    user_step[chat_id] = "phone"
elif step == "phone":
    user_data[chat_id]["phone"] = text
    update.message.reply_text("Loyihangiz nomini yozing:")
    user_step[chat_id] = "project"
elif step == "project":
    user_data[chat_id]["project"] = text
    update.message.reply_text("Loyiha planshetini yuboring (fayl):")
    user_step[chat_id] = "planshet"
elif step == "planshet":
    user_step[chat_id] = "photo"
    update.message.reply_text("3x4 fotosuratni yuboring:")
elif step == "photo":
    send_to_admin(context, chat_id)
    update.message.reply_text("✅ Ma'lumotlaringiz yuborildi.")
    user_step.pop(chat_id)
    user_data.pop(chat_id)

def send_to_admin(context: CallbackContext, chat_id): data = user_data[chat_id] text = ( f"📍 Viloyat: {data['region']}\n" f"📌 Tuman: {data['district']}\n" f"👤 F.I.SH.: {data['name']}\n" f"📞 Tel: {data['phone']}\n" f"📄 Loyiha: {data['project']}" ) context.bot.send_message(chat_id=ADMIN_ID, text=text)

def main(): updater = Updater(BOT_TOKEN, use_context=True) dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

updater.start_polling()
updater.idle()

if name == 'main': main()

