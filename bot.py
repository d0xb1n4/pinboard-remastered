from pinboard_api import PinboardApi

token = 'id0000000002VjbVw9UHqBmJJ5v32JVi'
api = PinboardApi(token)

for event in api.listen():
    api.method('deleteMessage', message_id=event['data']['id'])

