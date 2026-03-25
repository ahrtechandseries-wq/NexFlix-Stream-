import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
from threading import Thread

# --- Flask Server for Render (Keep Alive) ---
app = Flask(__name__)
@app.route('/')
def home(): return "NexFlix Stream Server is Running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- Load Config From Render Environment Variables ---
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
APP_URL = os.getenv("APP_URL") 

bot = Client(
    "NexFlixStreamBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# --- Handlers ---
@bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.reply_text("🎬 **NexFlix Admin Panel Active!**\nSend me a video file to get the streaming link.")

@bot.on_message(filters.private & (filters.video | filters.document))
async def generate_stream_link(client, message):
    # Only Admin can use this
    if message.from_user.id != ADMIN_ID:
        return

    msg = await message.reply_text("⏳ *Processing File...*", quote=True)
    
    # Generate Link using Message ID
    stream_link = f"{APP_URL}/watch/{message.id}"
    
    text = (
        "✅ **Link Generated!**\n\n"
        f"🔗 **URL:** `{stream_link}`\n\n"
        "Use this link in your website's Iframe."
    )
    
    await msg.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🌐 Open Stream", url=stream_link)
        ]])
    )

if __name__ == "__main__":
    # Start Flask in a separate thread
    Thread(target=run_flask).start()
    bot.run()
