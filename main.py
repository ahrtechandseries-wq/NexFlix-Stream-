import os
import sys
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# --- Flask Server for Render ---
app = Flask(__name__)
@app.route('/')
def home(): return "NexFlix Server is Running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- Configuration Check ---
try:
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    ADMIN_ID = int(os.getenv("ADMIN_ID"))
    APP_URL = os.getenv("APP_URL", "https://rnexflix.top")
except Exception as e:
    print(f"ERROR: Missing Env Variables: {e}")
    sys.exit(1)

# --- Bot Initialization ---
bot = Client(
    "NexFlixStreamBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    in_memory=True  # এটি রেন্ডারের স্টোরেজ সমস্যা কমাবে
)

@bot.on_message(filters.command("start") & filters.private)
def start_cmd(client, message):
    if message.from_user.id == ADMIN_ID:
        message.reply_text("✅ **NexFlix Admin Active!**\nSend a video for the link.")

@bot.on_message(filters.private & (filters.video | filters.document))
def handle_video(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    
    stream_url = f"{APP_URL}/watch/{message.id}"
    message.reply_text(f"🔗 **Streaming Link:**\n`{stream_url}`")

if __name__ == "__main__":
    # Start Flask
    Thread(target=run_flask, daemon=True).start()
    # Start Bot
    print("Starting NexFlix Bot...")
    bot.run()
    
