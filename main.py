import os
import time
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# --- Flask Server (Render Port Check Pass করার জন্য) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "NexFlix Server is Live and Running!"

def run_flask():
    # Render এর পোর্ট এনভায়রনমেন্ট থেকে নেওয়া
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- Configuration (From Render Env Variables) ---
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
APP_URL = os.getenv("APP_URL", "")

# --- Bot Initialization ---
# Simple Client (No complex async settings)
bot = Client(
    "NexFlixBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command("start") & filters.private)
def start(c, m):
    if m.from_user.id == ADMIN_ID:
        m.reply_text("✅ **NexFlix Admin Active!**\nভিডিও পাঠান, আমি লিঙ্ক দিচ্ছি।")

@bot.on_message(filters.private & (filters.video | filters.document))
def stream(c, m):
    if m.from_user.id != ADMIN_ID: return
    
    # স্ট্রিমিং লিঙ্ক জেনারেট
    stream_url = f"{APP_URL}/watch/{m.id}"
    m.reply_text(f"🔗 **Your Streaming Link:**\n`{stream_url}`")

if __name__ == "__main__":
    # ১. ব্যাকগ্রাউন্ডে ফ্ল্যাস্ক সার্ভার স্টার্ট করা
    print("Starting Flask Web Server...")
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    # ২. বটের জন্য ছোট বিরতি (যাতে পোর্ট বাইন্ডিং শেষ হয়)
    time.sleep(2)
    
    # ৩. টেলিগ্রাম বট রান করা (সরাসরি পদ্ধতি)
    print("Starting NexFlix Bot...")
    bot.run()
