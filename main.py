import os from telegram import Update, ReplyKeyboardMarkup from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext from dotenv import load_dotenv

load_dotenv() BOT_TOKEN = os.getenv("BOT_TOKEN") ADMIN_ID = os.getenv("ADMIN_ID")

12 ta viloyat va tumanlari

regions = { "Andijon": ["Asaka", "Baliqchi", "Bo‘z", "Buloqboshi", "Izboskan", "Jalaquduq", "Marhamat", "Oltinko‘l", "Paxtaobod", "Shahrixon", "Ulug‘nor", "Xo‘jaobod", "Qo‘rg‘ontepa"], "Buxoro": ["Buxoro shahri", "Buxoro tumani", "G‘ijduvon", "Kogon", "Olot", "Peshku", "Romitan", "Shofirkon", "Vobkent", "Qorako‘l", "Qorovulbozor", "Jondor"], "Farg‘ona": ["Quva", "Qo‘qon", "Rishton", "Beshariq", "Dang‘ara", "Furqat", "Marg‘ilon", "Oltiariq", "Toshloq", "Uchko‘prik", "Yozyovon", "Bog‘dod"], "Jizzax": ["G‘allaorol", "Zarbdor", "Zomin", "Mirzacho‘l", "Paxtakor", "Yangiobod", "Zafarobod", "Do‘stlik", "Baxmal", "Forish", "Sharof Rashidov"], "Namangan": ["Chortoq", "Chust", "Kosonsoy", "Mingbuloq", "Norin", "Pop", "To‘raqo‘rg‘on", "Uychi", "Uchkurgan", "Yangiqo‘rg‘on"], "Navoiy": ["Karmana", "Konimex", "Navbahor", "Nurota", "Qiziltepa", "Xatirchi", "Zarafshon", "Uchquduq"], "Qashqadaryo": ["Qarshi", "Dehqonobod", "G‘uzor", "Kamashi", "Kasbi", "Kitob", "Koson", "Mirishkor", "Muborak", "Nishon", "Shahrisabz", "Yakkabog‘", "Chiroqchi"], "Qoraqalpog‘iston": ["Nukus", "Amudaryo", "Beruniy", "Chimboy", "Ellikqal‘a", "Kegeyli", "Mo‘ynoq", "Qanliko‘l", "Qorao‘zak", "Shumanay", "Taxtako‘pir", "To‘rtko‘l", "Xo‘jayli"], "Samarqand": ["Bulung‘ur", "Ishtixon", "Jomboy", "Kattaqo‘rg‘on", "Narpay", "Nurobod", "Oqdaryo", "Pastdarg‘om", "Paxtachi", "Payariq", "Qo‘shrabot", "Toyloq", "Urgut"], "Sirdaryo": ["Boyovut", "Sardoba", "Sayxunobod", "Mirzaobod", "Oqoltin", "Shirin", "Sirdaryo", "Xovos", "Yangiyer"], "Surxondaryo": ["Angor", "Bandixon", "Boysun", "Denov", "Jarqo‘rg‘on", "Muzrabot", "Oltinsoy", "Qiziriq", "Sariosiyo", "Sho‘rchi", "Uzun", "Qumqo‘rg‘on"], "Toshkent": ["Bekobod", "Bo‘ka", "Bo‘stonliq", "Chinoz", "Qibray", "Ohangaron", "Oqqo‘rg‘on", "Parkent", "Piskent", "Quyichirchiq", "Yangiyo‘l", "Yuqorichirchiq", "Zangiota"] }

user_data = {} user_step = {}

def start(update: Update, context: CallbackContext): chat_id = update.message.chat_id user_step[chat_id] = "region" region_names = list(regions.keys()) keyboard = ReplyKeyboardMarkup([region_names[i:i+2] for i in range(0, len(region_names), 2)], resize_keyboard=True) update.message.reply_text("📍 Viloyatingizni tanlang:", reply_markup=keyboard)

def handle(update: Update, context: CallbackContext): chat_id = update.message.chat_id text = update.message.text step = user_step.get(chat_id)

if step == "region":
    if text in regions:
        user_data[chat_id] = {"region": text}
        user_step[chat_id] = "district"
        districts = regions[text]
        keyboard = ReplyKeyboardMarkup([districts[i:i+2] for i in range(0, len(districts), 2)], resize_keyboard=True)
        update.message.reply_text("🏘 Tumanni tanlang:", reply_markup=keyboard)
    else:
        update.message.reply_text("❗ Viloyatni ro‘yxatdan tanlang.")

elif step == "district":
    region = user_data[chat_id]["region"]
    if text in regions[region]:
        user_data[chat_id]["district"] = text
        user_step[chat_id] = "fish"
        update.message.reply_text("👤 F.I.Sh. ni kiriting:")
    else:
        update.message.reply_text("❗ Tumanni ro‘yxatdan tanlang.")

elif step == "fish":
    user_data[chat_id]["fish"] = text
    user_step[chat_id] = "phone"
    update.message.reply_text("📞 Telefon raqamingizni yuboring:")

elif step == "phone":
    user_data[chat_id]["phone"] = text
    user_step[chat_id] = "project"
    update.message.reply_text("📝 Loyihangiz nomini yozing:")

elif step == "project":
    user_data[chat_id]["project"] = text
    user_step[chat_id] = "photo"
    update.message.reply_text("📸 3x4 fotosuratni yuboring:")

elif step == "photo":
    update.message.reply_text("✅ Ma’lumotlaringiz yuborildi. Rahmat!")
    send_to_admin(context, chat_id)
    user_step.pop(chat_id)
    user_data.pop(chat_id)

def handle_photo(update: Update, context: CallbackContext): chat_id = update.message.chat_id step = user_step.get(chat_id) if step == "photo": user_data[chat_id]["photo"] = update.message.photo[-1].file_id update.message.reply_text("✅ Ma’lumotlaringiz yuborildi. Rahmat!") send_to_admin(context, chat_id) user_step.pop(chat_id) user_data.pop(chat_id)

def send_to_admin(context: CallbackContext, chat_id): data = user_data[chat_id] text = ( f"🎂 Yangi ro‘yxatdan o‘tuvchi:\n" f"📍 Viloyat: {data['region']}\n" f"🏘 Tuman: {data['district']}\n" f"👤 F.I.Sh.: {data['fish']}\n" f"📞 Tel: {data['phone']}\n" f"📝 Loyiha: {data['project']}" ) context.bot.send_message(chat_id=ADMIN_ID, text=text) context.bot.send_photo(chat_id=ADMIN_ID, photo=data.get("photo"))

updater = Updater(BOT_TOKEN, use_context=True) dp = updater.dispatcher dp.add_handler(CommandHandler("start", start)) dp.add_handler(MessageHandler(Filters.photo, handle_photo)) dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle))

updater.start_polling() updater.idle()

