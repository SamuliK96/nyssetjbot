import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import datetime as dt
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
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Seuraavaan NSSS on jäljellä {NYSSETJ.days} päivää.")

async def ajot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Seuraaviin kokoontumisajoihin on jäljellä {AJOTJ.days} päivää.")

if __name__ == '__main__':
    application = ApplicationBuilder().token("7105195103:AAH7yDbExpUneGI7CUnrKdvT7QE41rKgtho").build()
    
    start_handler = CommandHandler('start', start)
    nysse_handler = CommandHandler('nyssetj', nysse)
    ajo_handler   = CommandHandler('ajotj', ajot)

    application.add_handler(start_handler)
    application.add_handler(nysse_handler)
    application.add_handler(ajo_handler)
    
    application.run_polling()