import telebot
from pathlib import Path
from runner import run_py

TOKEN = "8314436525:AAH00j-URCgLdvNljnElshFQ6EaB9DtFweo"
bot = telebot.TeleBot(TOKEN)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@bot.message_handler(content_types=["document"])
def handle_py_upload(message):
    doc = message.document

    if not doc.file_name.endswith(".py"):
        bot.reply_to(message, "❌ Sadece .py dosyası atabilirsin")
        return

    file_info = bot.get_file(doc.file_id)
    downloaded = bot.download_file(file_info.file_path)

    file_path = UPLOAD_DIR / doc.file_name
    file_path.write_bytes(downloaded)

    bot.reply_to(message, "📦 Dosya alındı, analiz ediliyor...")

    try:
        run_py(file_path)
        bot.send_message(message.chat.id, "✅ Script başarıyla çalıştı")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Hata:\n{e}")

@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(msg, "🤖 .py dosyasını gönder")

bot.infinity_polling()
