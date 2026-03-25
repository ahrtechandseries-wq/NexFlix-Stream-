import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

# --- Flask Server (Render এর জন্য জরুরি) ---
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

# --- Bot Initialization ---
bot = Client("NexFlixBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.command("start") & filters.private)
async def start(c, m):
    if m.from_user.id == ADMIN_ID:
        await m.reply_text("✅ **Admin Mode Active!**\nভিডিও ফাইল পাঠান, আমি লিঙ্ক দিচ্ছি।")

@bot.on_message(filters.private & (filters.video | filters.document))
async def stream(c, m):
    if m.from_user.id != ADMIN_ID: return
    
    # স্ট্রিমিং লিঙ্ক তৈরি
    stream_url = f"{APP_URL}/watch/{m.id}"
    
    await m.reply_text(
        f"🔗 **Your Streaming Link:**\n`{stream_url}`",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🎬 Play Now", url=stream_url)
        ]])
    )

if __name__ == "__main__":
    # Flask সার্ভার আলাদা থ্রেডে চালানো
    Thread(target=run_flask).start()
    
    # এরর এড়াতে নতুন ইভেন্ট লুপ সেট করা
    loop = asyncio.get_event_loop()
    bot.run()
