from telegram.constants import CHATACTION_TYPING, CHATACTION_UPLOAD_PHOTO
import messages as msg
from database import DB
from google_spell import get_google_spelling
import markups as mrk
from datetime import datetime as dt


def start(update, context):
    user_id = update.message.chat_id
    first_name = update.message.chat.first_name
    if not DB.check_user(user_id):
        user_name = update.message.chat.username
        DB.create_user(user_id, first_name, user_name)
        context.bot.send_chat_action(user_id, CHATACTION_TYPING)
        context.bot.send_message(user_id, msg.start.format(first_name.capitalize()))
        context.bot.send_message(user_id, msg.start1, reply_markup=mrk.start_markup())
    # elif DB.get_user(user_id)[3] == 1:
    #     context.bot.send_chat_action(user_id, CHATACTION_TYPING)
    #     text = DB.get_user(user_id)[4]
    #     context.bot.send_message(user_id, "Выберите подкатегорию: ", reply_markup=mrk.category())


def status0_and_false(update, context):
    user_id = update.message.chat_id
    text = update.message.text.strip()
    text = get_google_spelling(text).capitalize()
    DB.update_user(user_id, 'stage', 1)
    DB.update_user(user_id, 'medicine', text.capitalize())
    try:
        context.bot.send_chat_action(user_id, CHATACTION_UPLOAD_PHOTO)
        photo = open('medicine/{}.png'.format(text), 'rb')
        context.bot.send_photo(user_id, photo, "Выберите подкатегорию: ", reply_markup=mrk.category())
    except Exception:
        context.bot.send_message(user_id, "Выберите подкатегорию: ", reply_markup=mrk.category())


def answer(update, context):
    user_id = update.message.chat_id
    text = update.message.text.strip()
    text = get_google_spelling(text)
    user_info = DB.get_user(user_id)
    start = dt.now()
    if user_info[5] == 'active':

        if user_info[3] == 0 and DB.check_medicine(text.capitalize()):
            status0_and_false(update, context)
            context.bot.send_message(user_id, f'Запрос в базу данных заняло: {dt.now() - start}')

        elif text == 'Назад':
            first_name = update.message.chat.first_name
            context.bot.send_chat_action(user_id, CHATACTION_TYPING)
            context.bot.send_message(user_id, ".", reply_markup=mrk.remove())
            context.bot.delete_message(user_id, update.message.message_id+1)
            context.bot.send_message(user_id, msg.start1,
                                     reply_markup=mrk.start_markup())
        elif user_info[3] == 0:
            context.bot.send_chat_action(user_id, CHATACTION_TYPING)
            context.bot.send_message(user_id, "К сожалению данный препарат не найден", reply_markup=mrk.button_back())
            context.bot.send_sticker(user_id, msg.not_find)

        elif user_info[3] == 1 and text in ["О препарате", "Применение", "Где можно купить?"]:
            msg_id = update.message.message_id
            data = DB.get_medicine(user_info[4].capitalize())
            context.bot.send_chat_action(user_id, CHATACTION_TYPING)
            if text == 'О препарате':
                send_text = data[2]
                context.bot.send_message(user_id, send_text, reply_to_message_id=msg_id)
            elif text == 'Применение':
                send_text = data[3]
                context.bot.send_message(user_id, send_text, reply_to_message_id=msg_id)
                send_t = 'Обратитесь к врачу или фармацевту за советом прежде, чем принимать лекарственный препарат'
                context.bot.send_message(user_id, send_t, reply_to_message_id=msg_id)
            else:
                send_text = data[4]
                context.bot.send_message(user_id, send_text, reply_to_message_id=msg_id)

    elif user_info[5] == 'admin':
        pass


# def find_medicine(update, context):
#     user_id = update.message.chat_id
#     first_name = update.message.chat.first_name
#     context.bot.send_chat_action(user_id, CHATACTION_TYPING)
#     DB.update_user(user_id, 'stage', 0)
#     context.bot.send_message(user_id, msg.choice_med.format(first_name), reply_markup=mrk.remove())


def covid(update, context):
    user_id = update.callback_query.message.chat_id
    msg_id = update.callback_query.message.message_id
    DB.update_user(user_id, 'stage', 5)
    context.bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=msg.covid,
                                  reply_markup=mrk.start_markup(1))


def reference(update, context):
    user_id = update.callback_query.message.chat_id
    msg_id = update.callback_query.message.message_id
    DB.update_user(user_id, 'stage', 5)
    context.bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=msg.reference,
                                  reply_markup=mrk.start_markup(2))


def symptoms(update, context):
    user_id = update.callback_query.message.chat_id
    msg_id = update.callback_query.message.message_id
    data = update.callback_query.data
    DB.update_user(user_id, 'stage', 6)
    if data == 'симптомы':
        context.bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=msg.symptoms,
                                      reply_markup=mrk.start_markup(2))
    elif data == 'вакцинация':
        context.bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=msg.prophylaxis,
                                      reply_markup=mrk.vaccine())
    elif data == 'лечение':
        context.bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=msg.treatment,
                                      reply_markup=mrk.start_markup(2))


def step_back(update, context):
    user_id = update.callback_query.message.chat_id
    msg_id = update.callback_query.message.message_id
    user_info = DB.get_user(user_id)
    stage = user_info[3]
    if stage == 5:
        DB.update_user(user_id, 'stage', 4)
        context.bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=msg.start1,
                                      reply_markup=mrk.start_markup())
    elif stage == 6:
        DB.update_user(user_id, 'stage', 5)
        context.bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=msg.covid,
                                      reply_markup=mrk.start_markup(1))
    elif stage == 7:
        DB.update_user(user_id, 'stage', 6)
        context.bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=msg.prophylaxis,
                                      reply_markup=mrk.vaccine())


def find_med(update, context):
    user_id = update.callback_query.message.chat_id
    msg_id = update.callback_query.message.message_id
    context.bot.delete_message(user_id, msg_id)
    DB.update_user(user_id, 'stage', 0)
    context.bot.send_chat_action(user_id, CHATACTION_TYPING)
    context.bot.send_sticker(user_id, msg.search, reply_markup=mrk.remove())
    context.bot.send_message(user_id, msg.choice_med)


def vaccine(update, context):
    user_id = update.callback_query.message.chat_id
    msg_id = update.callback_query.message.message_id
    data = update.callback_query.data
    DB.update_user(user_id, 'stage', 7)
    if data == 'Sputnik':
        context.bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=msg.Sputnik,
                                      reply_markup=mrk.vaccine(1))
    else:
        context.bot.edit_message_text(chat_id=user_id, message_id=msg_id, text=msg.Vaxzevria,
                                      reply_markup=mrk.vaccine(2))


def get_sticker(update, context):
    print(update.message)
