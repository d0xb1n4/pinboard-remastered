import requests


class PinboardApi:
    def __init__(self, token):
        self.token = token
        self.last_event_id = 0

    def method(self, method_name: str, **kwargs):
        """ Обращение к методам API """
        params = []
        for i in kwargs:
            params.append(f'{i}={kwargs[i]}')

        url = 'http://127.0.0.1:8000/api/general/?method='
        url = url + method_name + '&token=' + self.token + '&'
        url = url + '&'.join(params)

        response = requests.get(url).json()

        return [response['data']]

    def check(self):
        """ Получает последнее сообщение из чата 1 раз """
        response = self.method('chatListen')

        if self.last_event_id != response[0]['id']:
            self.last_event_id = response[0]['id']
        else:
            return ''
        return response

    def listen(self):
        """ слушает сервер """

        while True:
            for event in self.check():
                yield event
