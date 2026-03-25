import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

# --- Flask Server ---
app = Flask(__name__)
@app.route('/')
def home(): return "NexFlix Server is Running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- Configuration ---
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
APP_URL = os.getenv("APP_URL", "")

bot = Client("NexFlixBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start") & filters.private)
def start(c, m):
    if m.from_user.id == ADMIN_ID:
        m.reply_text("✅ **NexFlix Admin Active!**\nভিডিও পাঠান লিঙ্ক দিচ্ছি।")

@bot.on_message(filters.private & (filters.video | filters.document))
def stream(c, m):
    if m.from_user.id != ADMIN_ID: return
    
    # Generate Link
    stream_url = f"{APP_URL}/watch/{m.id}"
    
    m.reply_text(
        f"🔗 **Streaming Link:**\n`{stream_url}`",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🎬 Play Now", url=stream_url)
        ]])
    )

if __name__ == "__main__":
    # Flask starts in background
    Thread(target=run_flask).start()
    # Simple bot run (No complex loops)
    bot.run()
