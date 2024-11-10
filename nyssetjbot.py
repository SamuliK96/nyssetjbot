import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import datetime as dt
import random
import threading, time, sys, pytz
NYSSE = dt.date(2025, 5, 29)
AJOT  = dt.date(2024, 10, 25)
nysse_secs = dt.datetime(2025, 5, 29, 12, 00, 00)




logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Tervetuloa käyttämään NysseTJ-bottia",  reply_to_message_id=update.message.id)

async def nysse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = dt.datetime.now(pytz.timezone('Europe/Helsinki')).date()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"NSSS:n alkuun jäljellä {(NYSSE-today).days} päivää.",  reply_to_message_id=update.message.id)

async def ajot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = dt.datetime.now(pytz.timezone('Europe/Helsinki')).date()
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Kokoontumisajojen alkuun jäljellä: {(AJOT-today).days} päivää.",  reply_to_message_id=update.message.id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Seuraavat kokoontumisajot järjestetään lappeen Rannoilla. Lisää tietoa tulee myöhemmin.",  reply_to_message_id=update.message.id)

# async def check_day(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    global today
#    today = dt.datetime.now(pytz.timezone('Europe/Helsinki')).date()
#    await context.bot.send_message(chat_id=update.effective_chat_id, text="Today value updated.")

# async def minutes(update: Update, context: ContextTypes.DEFAULT_TYPE):
#    timenow = dt.datetime.now()
#    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"NSSS:n alkuun jäljellä {(nysse_secs-timenow).seconds/60} minuuttia.",  reply_to_message_id=update.message.id)

async def other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Tuntematon komento.", reply_to_message_id=update.message.id)

def texts(text: str):
    replies = ["Älä oo noin perseestä", 
               "Ite oot paska", 
               "Ikävä tunnelma", 
               "Eikö äiti opettanu käytöstapoja?",
               "Menisit töihin"]
    
    if "paska" in text.lower() and "botti" in text.lower():
        return random.choice(replies)
    
    if "nysse" in text.lower():
        today = dt.datetime.now(pytz.timezone('Europe/Helsinki')).date()
        return f"NSSS:n alkuun jäljellä {(NYSSE-today).days} päivää."
    
    if "Lappeenranta" in text.lower():
        # return f"Kokoontumisajojen alkuun jäljellä: {AJOTJ.days} päivää."
        return "Seuraavat kokoontumisajot järjestetään lappeen Rannoilla. Lisää tietoa tulee myöhemmin."

    
async def msg_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg_type: str = update.message.chat.type
    text:     str = update.message.text
    print(f'\nUser {update.message.chat.id} in {msg_type}: {text}\n')

    try:
        await update.message.reply_text(texts(text), quote=True)
    except Exception:
        pass

'''def update_day_counter():
    while True:
        #TZ = pytz.timezone('Europe/Helsinki')
        global NYSSETJ, AJOTJ
        NYSSETJ = NYSSE - dt.datetime.now(pytz.timezone('Europe/Helsinki')).date()
        AJOTJ   = AJOT  - dt.datetime.now(pytz.timezone('Europe/Helsinki')).date()
        print("\nThis line is executed.\n")
        time.sleep(60)  # 86400 seconds = 24 hours
        return NYSSETJ, AJOTJ'''
    
def main():
    tokn = 'TOKEN'
    application = ApplicationBuilder().token(tokn).build()
    #today = dt.date.today()
    
    
    start_handler = CommandHandler('start', start)
    nysse_handler = CommandHandler('nysse', nysse)
    ajo_handler   = CommandHandler('kokoontumisajot', ajot)
    # check_handler = CommandHandler('update', check_day)
    # minute_handler= CommandHandler ('minutes', minutes)
    othercommand  = MessageHandler(filters.COMMAND, other)
    text_handler  = MessageHandler(filters.TEXT, msg_handle)

    application.add_handler(start_handler)
    application.add_handler(nysse_handler)
    application.add_handler(ajo_handler)
    # application.add_handler(check_handler)
    # application.add_handler(minute_handler)
    application.add_handler(othercommand)
    application.add_handler(text_handler)


    # Start the day-checking thread
    # threading.Thread(target=update_day_counter, daemon=True).start()
    # global NYSSETJ, AJOTJ  
    # NYSSETJ = NYSSE - dt.datetime.now(pytz.timezone('Europe/Helsinki')).date()
    # AJOTJ   = AJOT  - dt.datetime.now(pytz.timezone('Europe/Helsinki')).date()

    application.run_polling()



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)