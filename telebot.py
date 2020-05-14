from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import requests


updater = Updater(token='1136342890:AAH-hmQaQYNSIcIYhw72PnsbGZAmm1kwujM', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    print("STARTING!")
    contents = requests.get("http://77robinson.xyz/get_utilization_stats").json()
    image = contents['img']
    print(image)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=image)    
    context.bot.send_message(chat_id=update.effective_chat.id,text="Empty Seats: "+ str(contents['empty'])  +
                                                                    " Hogged Seats: " + str(contents['hogging']) + " Occupied Seats: " + 
                                                                    str(contents['occupied']))


def s1(update, context):
    print("STARTING!")
    contents = requests.get("http://77robinson.xyz/secret_sauce").json()
    s1 = contents['sean']
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=s1)    
    context.bot.send_message(chat_id=update.effective_chat.id,text="Hi I'm regular Sean")

def s2(update, context):
    print("STARTING!")
    contents = requests.get("http://77robinson.xyz/secret_sauce").json()
    s2 = contents['sean1']
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=s2)    
    context.bot.send_message(chat_id=update.effective_chat.id,text="Hi I'm the Better Sean")




def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command. Input /start to see seat utilization!")




start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

s1_handler = CommandHandler('s1', s1)
dispatcher.add_handler(s1_handler)

s2_handler = CommandHandler('s2', s2)
dispatcher.add_handler(s2_handler)

# ADD ALL OTHER HANDLERS ON TOP OF UNKNOWN HANDLER OR THEY WONT WORK # 
unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)



print("Bot has Started!")

updater.start_polling()

updater.idle()

updater.stop()