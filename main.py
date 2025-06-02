from telegram import Update, ReplyKeyboardMarkup from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext import os

Admin ID (env orqali olinadi)

ADMIN_ID = os.getenv("ADMIN_ID")

Har bir viloyatga tegishli tumanlar

regions = { "Andijon": ["Andijon shahri", "Asaka", "Baliqchi", "Bo‘z", "Buloqboshi", "Izboskan", "Jalaquduq", "Marhamat", "Oltinko‘l", "Paxtaobod", "Shahrixon", "Ulug‘nor", "Xo‘jaobod", "Qo‘rg‘ontepa"], "Buxoro": ["Buxoro shahri", "Buxoro tumani", "G‘ijduvon", "Kogon", "Olot", "Peshku", "Romitan", "Shofirkon", "Vobkent", "Qorako‘l", "Qorovulbozor", "Jondor"], "Farg‘ona": ["Farg‘ona shahri", "Quva", "Qo‘qon", "Rishton", "Beshariq", "Dang‘ara", "Furqat", "Marg‘ilon", "Oltiariq", "Toshloq", "Uchko‘prik", "Yozyovon", "O‘zbekiston", "Bog‘dod"], "Jizzax": ["Jizzax shahri", "G‘allaorol", "Zarbdor", "Zomin", "Mirzacho‘l", "Paxtakor", "Yangiobod", "Zafarobod", "Do‘stlik", "Baxmal", "Forish", "Sharof Rashidov"], "Namangan": ["Namangan shahri", "Chortoq", "Chust", "Kosonsoy", "Mingbuloq", "Norin", "Pop", "To‘raqo‘rg‘on", "Uychi", "Uchkurgan", "Yangiqo‘rg‘on"], "Navoiy": ["Navoiy shahri", "Karmana", "Konimex", "Navbahor", "Nurota", "Qiziltepa", "Xatirchi", "Zarafshon", "Uchquduq"], "Qashqadaryo": ["Qarshi shahri", "Dehqonobod", "G‘uzor", "Kamashi", "Kasbi", "Kitob", "Koson", "Mirishkor", "Muborak", "Nishon", "Shahrisabz", "Yakkabog‘", "Chiroqchi"], "Qoraqalpog‘iston": ["Nukus shahri", "Amudaryo", "Beruniy", "Chimboy", "Ellikqal‘a", "Kegeyli", "Mo‘ynoq", "Qanliko‘l", "Qorao‘zak", "Shumanay", "Taxtako‘pir", "To‘rtko‘l", "Xo‘jayli"], "Samarqand": ["Samarqand shahri", "Bulung‘ur", "Ishtixon", "Jomboy", "Kattaqo‘rg‘on", "Narpay", "Nurobod", "Oqdaryo", "Pastdarg‘om", "Paxtachi", "Payariq", "Qo‘shrabot", "Toyloq", "Urgut"], "Sirdaryo": ["Guliston shahri", "Boyovut", "Sardoba", "Sayxunobod", "Mirzaobod", "Oqoltin", "Shirin", "Sirdaryo", "Xovos", "Yangiyer"], "Surxondaryo": ["Termiz shahri", "Angor", "Bandixon", "Boysun", "Denov", "Jarqo‘rg‘on", "Muzrabot", "Oltinsoy", "Qiziriq", "Sariosiyo", "Sho‘rchi", "Uzun", "Qumqo‘rg‘on"], "Toshkent": ["Nurafshon shahri", "Bekobod", "Bo‘ka", "Bo‘stonliq", "Chinoz", "Qibray", "Ohangaron", "Oqqo‘rg‘on", "Parkent", "Piskent", "Quyichirchiq", "Yangiyo‘l", "Yuqorichirchiq", "Zangiota"] }

Har bir foydalanuvchi uchun vaqtinchalik ma'lumotlar

user_data = {} user_step = {}

Boshlanish

def start(update: Update, context: CallbackContext): chat_id = update.message.chat_id user_step[chat_id] = "viloyat" viloyatlar = list(regions.keys()) keyboard = ReplyKeyboardMarkup([viloyatlar[i:i+2] for i in range(0, len(viloyatlar), 2)], resize_keyboard=True) update.message.reply_text("Viloyatingizni tanlang:", reply_markup=keyboard)

def handle_message(update: Update, context: CallbackContext): chat_id = update.message.chat_id text = update.message.text step = user_step.get(chat_id)

if step == "viloyat":
    if text not in regions:
        update.message.reply_text("Iltimos, mavjud viloyatlardan birini tanlang.")
        return
    user_data[chat_id] = {"viloyat": text}
    user_step[chat_id] = "tuman"
    tumanlar = regions[text]
    keyboard = ReplyKeyboardMarkup([tumanlar[i:i+2] for i in range(0, len(tumanlar), 2)], resize_keyboard=True)
    update.message.reply_text("Tumanni tanlang:", reply_markup=keyboard)

elif step == "tuman":
    vil = user_data[chat_id].get("viloyat")
    if text not in regions.get(vil, []):
        update.message.reply_text("Iltimos, ro‘yxatdagi tumanlardan birini tanlang.")
        return
    user_data[chat_id]["tuman"] = text
    user_step[chat_id] = "fish"
    update.message.reply_text("F.I.Sh ni kiriting:")

elif step == "fish":
    user_data[chat_id]["fish"] = text
    user_step[chat_id] = "tel"
    update.message.reply_text("📱 Telefon raqamingizni kiriting:")

elif step == "tel":
    user_data[chat_id]["tel"] = text
    user_step[chat_id] = "project"
    update.message.reply_text("📌 Loyiha nomini yozing:")

elif step == "project":
    user_data[chat_id]["project"] = text
    user_step[chat_id] = "done"
    summary = f"📥 Yangi ro‘yxat:\nViloyat: {user_data[chat_id]['viloyat']}\nTuman: {user_data[chat_id]['tuman']}\nF.I.SH: {user_data[chat_id]['fish']}\nTelefon: {user_data[chat_id]['tel']}\nLoyiha: {user_data[chat_id]['project']}"
    context.bot.send_message(chat_id=ADMIN_ID, text=summary)
    update.message.reply_text("✅ Ro‘yxatdan o‘tdingiz. Rahmat!")
    user_step.pop(chat_id)
    user_data.pop(chat_id)

Botni ishga tushirish

updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True) dp = updater.dispatcher dp.add_handler(CommandHandler("start", start)) dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

updater.start_polling() updater.idle()

