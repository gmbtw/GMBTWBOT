from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
import subprocess

# Ваш токен API
TOKEN = "7611314815:AAFPDl9aA6gIxpZEhKAzJVwkGBfv8DyRKsM"

# Функция для обработки команды /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привет! Отправь мне ссылку на TikTok, и я конвертирую её в MP3.")

# Функция для обработки TikTok-ссылок
def download_tiktok(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    if "tiktok.com" not in url:
        update.message.reply_text("Пожалуйста, отправьте корректную ссылку на TikTok.")
        return

    update.message.reply_text("Скачиваю и конвертирую...")

    try:
        # Скачивание и конвертация в MP3
        output_path = "./downloads"
        os.makedirs(output_path, exist_ok=True)
        result = subprocess.run(
            ["yt-dlp", "-x", "--audio-format", "mp3", "-o", f"{output_path}/%(title)s.%(ext)s", url],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            mp3_file = next(file for file in os.listdir(output_path) if file.endswith(".mp3"))
            with open(os.path.join(output_path, mp3_file), "rb") as audio:
                update.message.reply_audio(audio)
            os.remove(os.path.join(output_path, mp3_file))
        else:
            update.message.reply_text("Произошла ошибка при загрузке. Попробуйте снова.")
    except Exception as e:
        update.message.reply_text(f"Ошибка: {str(e)}")

# Основной блок
def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_tiktok))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
