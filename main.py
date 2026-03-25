import os
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# --- Flask App for Render Health Check ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "NexFlix Streaming Server is Active!"

def run_web_server():
    # Render-এর দেওয়া পোর্টে রান করবে
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- Bot Config ---
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
APP_URL = os.getenv("APP_URL", "")

bot = Client(
    "NexFlixBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command("start") & filters.private)
def start(c, m):
    if m.from_user.id == ADMIN_ID:
        m.reply_text("✅ **NexFlix Admin Active!**\nSend a video for the link.")

@bot.on_message(filters.private & (filters.video | filters.document))
def stream(c, m):
    if m.from_user.id != ADMIN_ID: return
    
    # Generate Link
    stream_url = f"{APP_URL}/watch/{m.id}"
    m.reply_text(f"🔗 **Streaming Link:**\n`{stream_url}`")

if __name__ == "__main__":
    # ১. ব্যাকগ্রাউন্ডে ফ্ল্যাস্ক সার্ভার চালু করা
    t = Thread(target=run_web_server)
    t.daemon = True
    t.start()
    
    # ২. টেলিগ্রাম বট রান করা
    print("Starting Bot...")
    bot.run()
    
