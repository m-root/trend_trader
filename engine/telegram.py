from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# from telegram.ext import Updater
TOKEN='620369180:AAF58K-FUyB1E5L-AwEdp6D7GFciRNxEYJw'
updater = Updater(token=TOKEN)




def sayhi(bot, job):
    job.context.message.reply_text("hi")

def time(bot, update,job_queue):
    job = job_queue.run_repeating(sayhi, 5, context=update)

def main():
    updater = Updater("BOT TOKEN")
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text , time,pass_job_queue=True))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()





