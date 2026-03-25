import os
import asyncio
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# --- Flask Server (For Render Web Service) ---
app = Flask(__name__)
@app.route('/')
def home(): return "NexFlix Server is Live!"

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
async def start(c, m):
    if m.from_user.id == ADMIN_ID:
        await m.reply_text("✅ **NexFlix Admin Active!**\nভিডিও পাঠান, আমি লিঙ্ক দিচ্ছি।")

@bot.on_message(filters.private & (filters.video | filters.document))
async def stream(c, m):
    if m.from_user.id != ADMIN_ID: return
    stream_url = f"{APP_URL}/watch/{m.id}"
    await m.reply_text(f"🔗 **Your Streaming Link:**\n`{stream_url}`")

# --- Python 3.14 Event Loop Fix ---
async def start_bot():
    # ব্যাকগ্রাউন্ডে ফ্ল্যাস্ক চালানো
    Thread(target=run_flask, daemon=True).start()
    
    # বট স্টার্ট করা
    async with bot:
        print("Bot is Live on Python 3.14!")
        await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        # নতুন ভার্সনে লুপ হ্যান্ডেল করার সঠিক উপায়
        asyncio.run(start_bot())
    except (KeyboardInterrupt, SystemExit):
        pass
        
