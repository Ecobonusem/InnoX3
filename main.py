
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

regions = {
    "Toshkent": ["Yunusobod", "Chilonzor", "Olmazor", "Mirzo Ulug‘bek", "Yakkasaroy", "Bektemir", "Yashnobod", "Mirobod", "Uchtepa", "Shayxontohur", "Sirg‘ali"],
    "Andijon": ["Andijon", "Asaka", "Baliqchi", "Bo'z", "Buloqboshi", "Izboskan", "Jalaquduq", "Qo‘rg‘ontepa", "Marhamat", "Paxtakor", "Shahrixon", "Ulug‘nor", "Xo‘jaobod"],
    "Namangan": ["Namangan", "Chortoq", "Chust", "Kosonsoy", "Mingbuloq", "Norin", "Pop", "To‘raqo‘rg‘on", "Uchqo‘rg‘on", "Yangiqo‘rg‘on"],
    "Farg‘ona": ["Farg‘ona", "Qo‘qon", "Marg‘ilon", "Oltiariq", "Bag‘dod", "Beshariq", "Dang‘ara", "Furqat", "Quva", "Qo‘shtepa", "Rishton", "So‘x", "Toshloq", "Uchko‘prik", "Yozyovon"],
    "Samarqand": ["Samarqand", "Bulung‘ur", "Ishtixon", "Jomboy", "Kattaqo‘rg‘on", "Narpay", "Nurobod", "Oqdaryo", "Paxtachi", "Pastdarg‘om", "Payariq", "Qo‘shrabot", "Tayloq", "Urgut"],
    "Buxoro": ["Buxoro", "G‘ijduvon", "Jondor", "Kogon", "Olot", "Peshku", "Qorako‘l", "Qorovulbozor", "Romitan", "Shofirkon", "Vobkent"],
    "Qashqadaryo": ["Qarshi", "Chiroqchi", "Dehqonobod", "G‘uzor", "Kasbi", "Kitob", "Koson", "Mirishkor", "Muborak", "Nishon", "Qamashi", "Shahrisabz", "Yakkabog‘"],
    "Surxondaryo": ["Termiz", "Angor", "Bandixon", "Boysun", "Denov", "Jarqo‘rg‘on", "Qiziriq", "Qumqo‘rg‘on", "Muzrabot", "Oltinsoy", "Sariosiyo", "Sherobod", "Sho‘rchi", "Uzun"],
    "Jizzax": ["Jizzax", "Arnasoy", "Baxmal", "Do‘stlik", "Forish", "G‘allaorol", "Mirzacho‘l", "Paxtakor", "Yangiobod", "Zarbdor", "Zafarobod", "Zomin"],
    "Sirdaryo": ["Guliston", "Boyovut", "Mirzaobod", "Oqoltin", "Sardoba", "Sayxunobod", "Sharof Rashidov", "Sirdaryo", "Xovos"],
    "Navoiy": ["Navoiy", "Karmana", "Konimex", "Qiziltepa", "Navbahor", "Nurota", "Xatirchi", "Zarafshon"],
    "Xorazm": ["Urganch", "Bog‘ot", "Gurlan", "Xazorasp", "Xonqa", "Qo‘shko‘pir", "Shovot", "Yangiariq", "Yangibozor"]
}

user_data = {}
user_step = {}

def start(update: Update, context: CallbackContext):
    keyboard = [[region] for region in regions.keys()]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    chat_id = update.message.chat_id
    update.message.reply_text("Viloyatingizni tanlang:", reply_markup=reply_markup)
    user_step[chat_id] = "region"

def handle_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text
    step = user_step.get(chat_id)

    if step == "region":
        if text in regions:
            user_data[chat_id] = {"region": text}
            keyboard = [[district] for district in regions[text]]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            update.message.reply_text(f"{text} viloyati tanlandi. Endi tumaningizni tanlang:", reply_markup=reply_markup)
            user_step[chat_id] = "district"
        else:
            update.message.reply_text("Iltimos, viloyat nomini to‘g‘ri tanlang.")
    elif step == "district":
        user_data[chat_id]["district"] = text
        region = user_data[chat_id]["region"]
        district = user_data[chat_id]["district"]
        context.bot.send_message(chat_id=ADMIN_ID, text=f"📍 Yangi ro‘yxat:
Viloyat: {region}
Tuman: {district}")
        update.message.reply_text("✅ Ma’lumot yuborildi.")
        user_data.pop(chat_id)
        user_step.pop(chat_id)
    else:
        update.message.reply_text("Iltimos, /start buyrug‘i bilan boshlang.")

updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

updater.start_polling()
