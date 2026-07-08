from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os, requests

# Ambil token dari environment variable
TOKEN = os.getenv("8875782650:AAEYj1dB7R9TOfiPfYWkGvZ-OUsKuhFLwq4")
AI_URL = os.getenv("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")

def start(update, context):
    update.message.reply_text("Halo bro! Kirim foto ke gue, nanti gue proses.")

def handle_photo(update, context):
    chat_id = update.message.chat_id
    update.message.reply_text("Foto diterima, lagi diproses...")

    # Ambil file foto dari Telegram
    photo = update.message.photo[-1].get_file()
    file_url = photo.file_path

    # Kirim ke AI API (contoh Hugging Face Spaces)
    try:
        response = requests.post(AI_URL, json={"image_url": file_url})
        if response.ok:
            result = response.json()
            context.bot.send_photo(chat_id, result["image_url"])
        else:
            update.message.reply_text("Gagal proses gambar 😭")
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

# Setup bot
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(MessageHandler(Filters.photo, handle_photo))

updater.start_polling()
updater.idle()
