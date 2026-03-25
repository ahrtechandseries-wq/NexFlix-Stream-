import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

# --- Flask Server for Render ---
app = Flask(__name__)
@app.route('/')
def home(): return "NexFlix Server is Live!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- Configuration (From Environment Variables) ---
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
        await m.reply_text("✅ **Admin Mode Active!**\nSend me a video file for the streaming link.")

@bot.on_message(filters.private & (filters.video | filters.document))
async def stream(c, m):
    if m.from_user.id != ADMIN_ID: return
    
    # Generate Streaming Link
    stream_url = f"{APP_URL}/watch/{m.id}"
    
    await m.reply_text(
        f"🔗 **Streaming Link Ready:**\n`{stream_url}`",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🎬 Play Now", url=stream_url)
        ]])
    )

# --- The Fix for Runtime Error ---
async def main():
    async with bot:
        print("Bot is started!")
        # Flask keeps the web service alive
        await asyncio.Event().wait()

if __name__ == "__main__":
    Thread(target=run_flask).start()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
