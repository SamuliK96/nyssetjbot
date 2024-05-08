import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import datetime as dt
import random
today = dt.date.today()
NYSSE = dt.date(2025, 5, 29)
AJOT = dt.date(2024, 10, 25)
NYSSETJ  = NYSSE - today
AJOTJ    = AJOT - today

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Tervetuloa käyttämään NysseTJ-bottia")

async def nysse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"NSSS:n alkuun jäljellä {NYSSETJ.days} päivää.")

async def ajot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Kokoontumisajojen alkuun jäljellä: {AJOTJ.days} päivää.")

async def other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Tuntematon komento.")

def texts(text: str):
    replies = ["Älä oo noin perseestä", 
               "Ite oot paska", 
               "Ikävä tunnelma", 
               "Eikö äiti opettanu käytöstapoja?",
               "Menisit töihin",
               "Opettele laulamaan paremmin"]
    
    if "paska" in text.lower() and "botti" in text.lower():
        return random.choice(replies)
    
    if "nysse" in text.lower():
        return f"NSSS:n alkuun jäljellä {NYSSETJ.days} päivää."

    
async def msg_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User {update.message.chat.id} in {msg_type}: {text}')
    await update.message.reply_text(texts(text))


if __name__ == '__main__':
    application = ApplicationBuilder().token("TOKEN").build()
    
    start_handler = CommandHandler('start', start)
    nysse_handler = CommandHandler('nysse', nysse)
    ajo_handler   = CommandHandler('kokoontumisajot', ajot)
    othercommand  = MessageHandler(filters.COMMAND, other)
    text_handler  = MessageHandler(filters.TEXT, msg_handle)

    application.add_handler(start_handler)
    application.add_handler(nysse_handler)
    application.add_handler(ajo_handler)
    application.add_handler(othercommand)
    application.add_handler(text_handler)
    
    application.run_polling()
