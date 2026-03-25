import os
import asyncio
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# --- Flask Server (Render এর পোর্ট চেক পাস করার জন্য) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "NexFlix Server is Live!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- Configuration ---
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
APP_URL = os.getenv("APP_URL", "https://nexflix-stream-1.onrender.com")

# --- Bot Client ---
bot = Client("NexFlixBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start") & filters.private)
async def start(c, m):
    if m.from_user.id == ADMIN_ID:
        await m.reply_text("✅ **NexFlix Admin Active!**\nভিডিও পাঠান, আমি লিঙ্ক দিচ্ছি।")

@bot.on_message(filters.private & (filters.video | filters.document))
async def stream(c, m):
    if m.from_user.id != ADMIN_ID: return
    stream_url = f"{APP_URL}/watch/{m.id}"
    await m.reply_text(f"🔗 **Streaming Link:**\n`{stream_url}`")

# --- Python 3.14 এর জন্য আল্টিমেট ফিক্স ---
async def start_services():
    # ফ্ল্যাস্ক আলাদা থ্রেডে চালানো
    t = Thread(target=run_flask, daemon=True)
    t.start()
    
    # বট স্টার্ট করা (Async Context Manager দিয়ে)
    async with bot:
        print("Bot is started successfully!")
        # এটি বটকে চালু রাখবে
        await asyncio.Future() 

if __name__ == "__main__":
    try:
        # সরাসরি asyncio.run ব্যবহার করা (Python 3.14 এর জন্য বেস্ট)
        asyncio.run(start_services())
    except (KeyboardInterrupt, SystemExit):
        pass
                
