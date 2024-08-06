from data.loader import bot

from telebot import types

from states.custom_states import AdState


@bot.message_handler(state=AdState.start_process)
def start_process(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Сколько фотографий будет в объявлении?')
    bot.set_state(message.from_user.id, AdState.pre_process_photo, chat_id)


@bot.message_handler(state=AdState.pre_process_photo, content_types=['text'])
def get_photo(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    count = 0
    photos = []

    bot.send_message(chat_id, f'Отправьте {message.text} фотографий подряд')
    bot.set_state(chat_id, AdState.post_process_photo, chat_id)
    with bot.retrieve_data(chat_id, user_id) as data:
        data['pre_process_photo'] = message.text


photos = []

@bot.message_handler(state=AdState.post_process_photo, content_types=['photo'])
def get_photo(message: types.Message):
    global photos
    chat_id = message.chat.id
    user_id = message.from_user.id

    print(message.photo)
    photos.append(message.photo[0])
    with bot.retrieve_data(chat_id, user_id) as data:
        pre = data['pre_process_photo']

    if len(photos) == int(pre):
        print('correct')

