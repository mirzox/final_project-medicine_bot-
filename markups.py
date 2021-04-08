from telegram import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        for i in footer_buttons:
            menu.append([i])
    return menu


def category():
    temp = [
        KeyboardButton('О препарате'),
        KeyboardButton('Применение'),
        KeyboardButton('Где можно купить?'),
        KeyboardButton('Назад')
    ]
    return ReplyKeyboardMarkup(build_menu(temp, 2), True, True)


def start_markup(stage=None):
    if stage is None:
        items = [
            InlineKeyboardButton('🔍 Найти препарат', callback_data='find_medicine'),
            InlineKeyboardButton('📖 Справочная', callback_data='reference'),
            InlineKeyboardButton('❗️O COVID-19', callback_data='covid')

        ]
        return InlineKeyboardMarkup(build_menu(items, 1))
    elif stage == 1:
        header = [
            InlineKeyboardButton('🏥 Вакцинация ❤️', callback_data='вакцинация')
        ]
        items = [
            InlineKeyboardButton('❗️Симптомы', callback_data='симптомы'),
            InlineKeyboardButton('✅ Лечение', callback_data='лечение')
        ]
        footer = [
            InlineKeyboardButton('Назад', callback_data='back')
        ]
        return InlineKeyboardMarkup(build_menu(items, 2, header_buttons=header, footer_buttons=footer))
    elif stage == 2:
        return InlineKeyboardMarkup([[InlineKeyboardButton('Назад', callback_data='back')]])


def vaccine(step=0):
    if step == 0:
        items = [
            InlineKeyboardButton('🇬🇧 Vaxzevria 🇬🇧', callback_data='Vaxzevria'),
            InlineKeyboardButton("🇷🇺 Спутник V 🇷🇺", callback_data='Sputnik')
        ]
        footer = [
            InlineKeyboardButton('Назад', callback_data='back')
        ]
        return InlineKeyboardMarkup(build_menu(items, 2, footer_buttons=footer))
    elif step == 1:
        items = [
            InlineKeyboardButton('🇬🇧 Vaxzevria 🇬🇧', callback_data='Vaxzevria'),
            InlineKeyboardButton('Назад', callback_data='back')
        ]
        return InlineKeyboardMarkup(build_menu(items, 1))
    else:
        items = [
            InlineKeyboardButton("🇷🇺 Спутник V 🇷🇺", callback_data='Sputnik'),
            InlineKeyboardButton('Назад', callback_data='back')
        ]
        return InlineKeyboardMarkup(build_menu(items, 1))


def button_back():
    return ReplyKeyboardMarkup([[KeyboardButton('Назад')]], True, True)


def remove():
    return ReplyKeyboardRemove()


