from pinboard_api import PinboardApi
import wikipedia

wikipedia.set_lang('ru')

token = 'adminQOuWws3617vBOJyHUTJA'
api = PinboardApi(token)


def send_message(text):
    api.method('sendMessage', text=text)

for event in api.listen():
    print(event)
    text = event['text'].lower()

    if 'запись' in text:
        pin = int(text.split()[1])

        print(api.method('sendMessage', pin_id=pin))

    elif 'привет' in text:
        send_message('И тебе прuвет!')


    elif 'удали свои сообщения' in text:
        for i in range(0, event['id']):
            print(api.method('deleteMessage', message_id=i))

