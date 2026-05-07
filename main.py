from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import subprocess
import os

TOKEN = os.getenv("TOKEN")

async def compress(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = await update.message.reply_text("Compressing video...")

    video = update.message.video

    file = await video.get_file()

    await file.download_to_drive("input.mp4")

    subprocess.run([
        "ffmpeg",
        "-i", "input.mp4",
        "-vf", "scale=-2:720",
        "-crf", "32",
        "output.mp4"
    ])

    await msg.edit_text("Uploading...")

    await update.message.reply_video(video=open("output.mp4", "rb"))

    os.remove("input.mp4")
    os.remove("output.mp4")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    MessageHandler(filters.VIDEO, compress)
)

print("Bot running...")

app.run_polling()
