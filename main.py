from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from const import TOKEN
import models as mdl
updater = Updater(TOKEN, workers=4)
dp = updater.dispatcher

dp.add_handler(CommandHandler('start', mdl.start, run_async=True))



dp.add_handler(CallbackQueryHandler(pattern='find_medicine', callback=mdl.find_med, run_async=True))

dp.add_handler(CallbackQueryHandler(pattern='covid', callback=mdl.covid, run_async=True))

dp.add_handler(CallbackQueryHandler(pattern='reference', callback=mdl.reference, run_async=True))

for i in ['симптомы', 'вакцинация', 'лечение']:
    dp.add_handler(CallbackQueryHandler(pattern=i, callback=mdl.symptoms, run_async=True))

for i in ["Sputnik", "Vaxzevria"]:
    dp.add_handler(CallbackQueryHandler(pattern=i, callback=mdl.vaccine, run_async=True))

dp.add_handler(CallbackQueryHandler(pattern='back', callback=mdl.step_back, run_async=True))

dp.add_handler(MessageHandler(Filters.text, mdl.answer, run_async=True))

updater.start_polling()
updater.idle()
