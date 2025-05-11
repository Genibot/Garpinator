elena-bot/
├── bot.py  
│   # Gère le comportement du chatbot Elena, multilingue et contextuel  
│
│import os
│import json
│import random
│import datetime
│from telegram import Update, InputFile
│from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
│from langdetect import detect
│from responses import get_response, get_photo_response, get_lang_code, error_no_photos, welcome_message, goodbye_message, subscription_invite
│
│BOT_TOKEN = "8072445010:AAFhz9wqtCdi6cg0jM2MK_bW9uwsVK2Q93Y"
│ADMIN_ID = 1880671464
│PHOTO_LIMIT = 8
│FREE_DURATION_MINUTES = 30
│PHOTO_PATH = "photos"
│USERS_FILE = "users.json"
│
│# Charger les utilisateurs
│def load_users():
│    if not os.path.exists(USERS_FILE):
│        return {}
│    with open(USERS_FILE, "r") as f:
│        return json.load(f)
│
│# Sauvegarder les utilisateurs
│def save_users(users):
│    with open(USERS_FILE, "w") as f:
│        json.dump(users, f, indent=2)
│
│# Initialisation
│users = load_users()
│
│# Utilitaire pour déterminer la langue
│def get_lang(text):
│    try:
│        lang = detect(text)
│        return get_lang_code(lang)
│    except:
│        return "fr"
│
│# Vérifie si abonné
│def is_subscribed(user):
│    return user.get("subscribed", False)
│
│# Vérifie le quota ou durée gratuite
│def check_access(user_id):
│    user = users.get(str(user_id), {})
│    now = datetime.datetime.utcnow()
│    if not user:
│        users[str(user_id)] = {
│            "start_time": now.isoformat(),
│            "photos_sent": [],
│            "subscribed": False
│        }
│        save_users(users)
│        return True
│    elif is_subscribed(user):
│        return True
│    else:
│        start = datetime.datetime.fromisoformat(user.get("start_time"))
│        elapsed = (now - start).total_seconds() / 60
│        return elapsed < FREE_DURATION_MINUTES
│
│# Commande /start
│async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
│    user_id = update.effective_user.id
│    lang = get_lang(update.message.text or "")
│    users[str(user_id)] = {
│        "start_time": datetime.datetime.utcnow().isoformat(),
│        "photos_sent": [],
│        "subscribed": False,
│        "lang": lang
│    }
│    save_users(users)
│    await update.message.reply_text(welcome_message(lang))
│
│# Réponse principale
│async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
│    user_id = update.effective_user.id
│    text = update.message.text
│    user = users.get(str(user_id), {})
│    lang = user.get("lang") or get_lang(text)
│    user["lang"] = lang
│
│    if not check_access(user_id):
│        await update.message.reply_text(subscription_invite(lang))
│        return
│
│    if "video" in text.lower():
│        await update.message.reply_text("Désolé mon cœur, je n'en ai pas encore fait... je préfère envoyer des photos.")
│        return
│
│    photo_category = None
│    if any(word in text.lower() for word in ["selfie", "photo"]):
│        photo_category = "selfie"
│    elif any(word in text.lower() for word in ["lingerie", "culotte", "string", "nuisette"]):
│        photo_category = "sexy"
│    elif any(word in text.lower() for word in ["fesse", "seins"]):
│        photo_category = "coquin"
│
│    if photo_category:
│        photos_sent = user.get("photos_sent", [])
│        if not is_subscribed(user) and len(photos_sent) >= 1:
│            await update.message.reply_text("Tu as déjà reçu ta photo gratuite mon chéri... Abonne-toi pour en avoir d'autres")
│            return
│        elif is_subscribed(user) and len(photos_sent) >= PHOTO_LIMIT:
│            await update.message.reply_text(error_no_photos(lang))
│            return
│
│        # Envoi d'une photo unique non répétée
│        folder = os.path.join(PHOTO_PATH, photo_category)
│        choices = [f for f in os.listdir(folder) if f not in photos_sent]
│        if not choices:
│            await update.message.reply_text("J'ai déjà tout montré pour cette catégorie, mon ange...")
│            return
│        chosen = random.choice(choices)
│        photos_sent.append(chosen)
│        user["photos_sent"] = photos_sent
│        save_users(users)
│        await update.message.reply_text(get_photo_response(lang, photo_category))
│        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=InputFile(os.path.join(folder, chosen)))
│        await update.message.reply_text("Et toi, tu aimerais qu'on se voit en vrai ? 😘")
│        return
│
│    await update.message.reply_text(get_response(lang, text))
│    save_users(users)
│
│# Lancement du bot
│if __name__ == '__main__':
│    app = ApplicationBuilder().token(BOT_TOKEN).build()
│    app.add_handler(CommandHandler("start", start))
│    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
│    app.run_polling()
│
├── responses.py
│   # (à compléter ensuite)
├── users.json  
│   # sera généré dynamiquement  
├── Dockerfile  
│   # (à compléter ensuite)
├── fly.toml  
│   # (à compléter ensuite)
├── requirements.txt  
│   # (à compléter ensuite)
└── photos/  
    ├── selfie/  
    │   ├── selfie1.jpg  
    │   └── selfie2.jpg  
    ├── sexy/  
    │   ├── sexy1.jpg  
    │   └── sexy2.jpg  
    └── coquin/  
        ├── coquin1.jpg  
        └── coquin2.jpg
