#!/usr/bin/python

from telegram.ext import Updater,CommandHandler, MessageHandler, BaseFilter, Filters
import time
import Kneel
import re
import DraftList
import LeagueTable
import CurrentScore
import References
import JanCup
import trades

def MessageCheck(Message):
    MyList = ["Dan","Neil","Shed","Matt","Shane","Ads","Tom","Elliott","Crigs","Rholo","Sam"]
    for iname in MyList:
        if re.search('(^|\s)'+iname+'(\s|$)',Message,re.I):
            return True            
                
updater = Updater(token=References.BotToken)
j = updater.job_queue
dispatcher = updater.dispatcher

#--Filter Classes

class NameFilter(BaseFilter):
    def filter(self,message):
        return (MessageCheck(message.text))

# --Initialise class instances
namefilter = NameFilter()

#---Message Functions

def callback_minute(bot, job):
    bot.send_message(chat_id=282457851, 
                    text='One message every minute')

def echo(bot, update):
    print(update.message)
    print(update.message['chat'])
    #update.message.reply_text(update.message.text)

def AsItStands(bot,update):
    bot.send_message(chat_id=update.message.chat_id,text='Generating Temporary Live Table')
    LeagueTable.AsItStands()
    time.sleep(1)
    bot.send_photo(chat_id=update.message.chat_id, photo=open('asitstands.png', 'rb'))

def ScoresDetailed(bot,update):
    id = update.message.from_user['id']
    bot.send_message(chat_id=update.message.chat_id,text=CurrentScore.DetailedTeamList(id))

def PlayersLeft(bot,update):
    id = update.message.from_user['id']
    bot.send_message(chat_id=update.message.chat_id,text=CurrentScore.PlayersLeft(id))

def jc(bot,update):
    bot.send_message(chat_id=update.message.chat_id,text=JanCup.LeagueData())

def ListTrades(bot,update):
    bot.send_message(chat_id=update.message.chat_id,text=trades.ListTrades())

def AddTrade(bot,update,args):
    if args:
        id = update.message.from_user['id']
        bot.send_message(chat_id=update.message.chat_id,text=trades.AddTrade(args[0],id))
    else:
        bot.send_message(chat_id=update.message.chat_id,text='Add a player to trade!')

def RemoveTrade(bot,update,args):
    if args:
        id = update.message.from_user['id']
        bot.send_message(chat_id=update.message.chat_id,text=trades.RemoveTrade(args[0],id))
    else:
        bot.send_message(chat_id=update.message.chat_id,text='Choose a player to remove!')

def NameCheck(bot,update):
    response = Kneel.NamePicker(update.message.text)
    if response:
        bot.send_message(chat_id=update.message.chat_id,text=response)

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


def Table(bot,update):
    bot.send_message(chat_id=update.message.chat_id,text='Generating Table')
    LeagueTable.CreateTable()
    time.sleep(1)
    bot.send_photo(chat_id=update.message.chat_id, photo=open('table.png', 'rb'))

def whosgot(bot, update, args):
    response = DraftList.WhosGot(args[0])
    bot.send_message(chat_id=update.message.chat_id, text=response)

def callback_alarm(bot, job):
    bot.send_message(chat_id=job.context, text='Deadline Has Passed!')

def callback_timer(bot, update, job_queue):
    bot.send_message(chat_id=update.message.chat_id,
                    text='Setting deadline timer')
    timer = References.SecondsUntilDeadline()
    job_queue.run_once(callback_alarm, timer, context=update.message.chat_id)

#---Handlers
#------Commands
Handlers = [] # Command Handlers

def AF2L(FunctionName): # add function 2 list
    Handlers.append(FunctionName)

#------Messages

AF2L(MessageHandler(namefilter, NameCheck))
AF2L(CommandHandler('scores', Scores, pass_args=True))
AF2L(CommandHandler('trades', ListTrades))
AF2L(CommandHandler('addtrade', AddTrade, pass_args=True))
AF2L(CommandHandler('removetrade', RemoveTrade, pass_args=True))
AF2L(CommandHandler('scoresdetailed', ScoresDetailed))
AF2L(CommandHandler('playersleft', PlayersLeft))
AF2L(CommandHandler('jancup', jc))
AF2L(CommandHandler('table', Table))
AF2L(CommandHandler('asitstands', AsItStands))
AF2L(CommandHandler('whosgot', whosgot, pass_args=True))
timer_handler = CommandHandler('timer', callback_timer, pass_job_queue=True)

echo_handler = MessageHandler(Filters.text, echo)
for f in Handlers:
    dispatcher.add_handler(f)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(timer_handler)
updater.start_polling()
updater.idle()
