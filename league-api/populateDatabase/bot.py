#!/usr/bin/python

from telegram.ext import Updater,CommandHandler, MessageHandler, BaseFilter, Filters
import time
import commands

def MessageCheck(Message):
    MyList = ["Dan","Neil","Shed","Matt","Shane","Ads","Tom","Elliott","Crigs","Rholo","Sam"]
    for iname in MyList:
        if re.search('(^|\s)'+iname+'(\s|$)',Message,re.I):
            return True            
                
BotToken='395243580:AAGrDXsMYzCs0h1NkNt66tLtgYTW4tvdCeo'
                
updater = Updater(token=BotToken)
j = updater.job_queue
dispatcher = updater.dispatcher


#---Message Functions

def Scores(bot,update,args):
    if args:
        if not args[0] == 'all':
            bot.send_message(chat_id=update.message.chat_id,text='Please format command /scores all')
        else:
            bot.send_message(chat_id=update.message.chat_id,text=commands.getAllScores())
    else:
        id = update.message.from_user['id']
        msg = commands.getOneScore(id)
        bot.send_message(chat_id=update.message.chat_id,text=msg)

#---Handlers
#------Commands
Handlers = [] # Command Handlers

def AF2L(FunctionName): # add function 2 list
    Handlers.append(FunctionName)

#------Messages

AF2L(CommandHandler('scores', Scores,pass_args=True))


for f in Handlers:
    dispatcher.add_handler(f)
updater.start_polling()
updater.idle()
