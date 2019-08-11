#!/usr/bin/python

from telegram.ext import Updater,CommandHandler, MessageHandler, BaseFilter, Filters
import time
import commands

def MessageCheck(Message):
    MyList = ["Dan","Neil","Shed","Matt","Shane","Ads","Tom","Elliott","Crigs","Rholo","Sam"]
    for iname in MyList:
        if re.search('(^|\s)'+iname+'(\s|$)',Message,re.I):
            return True            
                
BotToken='580359883:AAEFmZ-M_OWWF6GcDVpRsgEDN5GiERnlpJ4'
                
updater = Updater(token=BotToken)
j = updater.job_queue
dispatcher = updater.dispatcher

#--Filter Classes

class NameFilter(BaseFilter):
    def filter(self,message):
        return (MessageCheck(message.text))

# --Initialise class instances
namefilter = NameFilter()

#---Message Functions

def Scores(bot,update,args):
    if CurrentScore.DataAvailable():
        if args:
            if not args[0] == 'all':
                bot.send_message(chat_id=update.message.chat_id,text='Please format command /scores all')
            else:
                bot.send_message(chat_id=update.message.chat_id,text='Team (currentscore) Played-Playing-Yet To Play')
                for i in CurrentScore.LeagueData():
                    bot.send_message(chat_id=update.message.chat_id,text=i)
                    time.sleep(1)
        else:
            bot.send_message(chat_id=update.message.chat_id,text='Team (currentscore) Played-Playing-Yet To Play')
            id = update.message.from_user['id']
            msg = CurrentScore.SingleScore(id)
            bot.send_message(chat_id=update.message.chat_id,text=msg)
    else:
        bot.send_message(chat_id=update.message.chat_id,text='FPL Servers are a bit hectic right now blud. Try again in a bit yeah?')

#---Handlers
#------Commands
Handlers = [] # Command Handlers

def AF2L(FunctionName): # add function 2 list
    Handlers.append(FunctionName)

#------Messages

AF2L(MessageHandler(namefilter, NameCheck))
AF2L(CommandHandler('scores', Scores, pass_args=True))


echo_handler = MessageHandler(Filters.text, echo)
for f in Handlers:
    dispatcher.add_handler(f)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(timer_handler)
updater.start_polling()
updater.idle()
