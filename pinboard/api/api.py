from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .models import *
from .config import *


class CustomAPIView(APIView):
    def get(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        user.last_online = timezone.now()
        user.save()

class DeleteAccount(CustomAPIView):
    def post(self, request):
        user = CustomUser.objects.get(id=request.data['user_id'])
        user.delete()

        return Response({
            'status': 'OK',
            'data': {}
        }, status=status.HTTP_200_OK)

class SignUp(CustomAPIView):
    def post(self, request):
        try:
            if not CustomUser.objects.filter(email=request.data['email']):
                user = CustomUser()
                user.email = request.data['email']
                user.set_password(request.data['password'])
                user.code = user.generate_auth_code()
                user.username = user.email
                user.full_name = request.data['full_name']
                user.save()
                user.username = 'id' + '000000000' + str(user.id)
                user.API_TOKEN = create_token(user.username)
                user.save()

                msg = MIMEMultipart()
                msg['Subject'] = 'Код подтверждения Pinboard 📍'
                msg.attach(MIMEText(f'{user.username}, привет 👋\n'
                                    f'Вот твой код подтверждения: {user.code}\n\n'
                                    f'Благодарим за использование Pinboard 📍 ❤', 'plain'))

                server = smtplib.SMTP('smtp.gmail.com: 587')
                server.starttls()
                server.login(server_email, server_password)
                server.sendmail(server_email, user.email, msg.as_string())

                login(request, user)

                return Response({
                    'status': 'OK',
                    'data': {
                        'message': f'Код подтверждения отправлен на {user.email}'
                    }
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'ERR',
                    'data': {
                        'message': 'Пользователь с такой эл. почтой уже существует'
                    }
                }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                'status': 'ERR',
                'data': {
                    'message': 'Ошибка'
                }
            }, status=status.HTTP_400_BAD_REQUEST)


class CheckAuthCode(CustomAPIView):
    def post(self, request):
        if CustomUser.objects.filter(username=request.data['username']):
            user = CustomUser.objects.get(username=request.data['username'])
            code = request.data['code']

            if user.code == code:
                user.code = '0'
                user.save()

                return Response({
                    'status': 'OK',
                    'data': {
                        'status': True,
                        'message': 'Код подтверждения валидный'
                    }
                }, status=status.HTTP_200_OK)

            else:
                return Response({
                    'status': 'OK',
                    'data': {
                        'status': False,
                        'message': 'Код подтверждения не верный'
                    }
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'status': 'ERR',
                'data': {
                    'message': 'Нет такого пользователя'
                }
            }, status=status.HTTP_400_BAD_REQUEST)


class CancelSignUp(CustomAPIView):
    def post(self, request):
        user = CustomUser.objects.get(id=request.data['user_id'])
        user.delete()


class SignIn(CustomAPIView):
    def post(self, request):
        try:
            if CustomUser.objects.filter(email=request.data['email']):
                auth = authenticate(
                    request,
                    username=request.data['email'],
                    password=request.data['password']
                )

                if not auth is None:
                    login(request, auth)

                    if CustomUser.objects.get(email=request.data['email']).two_factor:
                        user = CustomUser.objects.get(email=request.data['email'])
                        user.code = CustomUser.generate_auth_code()
                        user.save()

                        msg = MIMEMultipart()
                        msg['Subject'] = 'Код подтверждения Pinboard 📍'
                        msg.attach(MIMEText(f'{user.username}, привет 👋\n'
                                            f'Вот твой код подтверждения: {user.code}\n\n'
                                            f'Благодарим за использование Pinboard 📍 ❤', 'plain'))

                        server = smtplib.SMTP('smtp.gmail.com: 587')
                        server.starttls()
                        server.login(server_email, server_password)
                        server.sendmail(server_email, user.email, msg.as_string())

                        return Response({
                            'status': 'OK',
                            'data': {
                                'two_factor': True
                            }
                        }, status=status.HTTP_200_OK)

                    else:
                        return Response({
                            'status': 'OK',
                            'data': {
                                'message': f'Вы успешно вошли в аккаунт'
                            }
                        }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'status': 'ERR',
                        'data': {
                            'message': 'Неверный пароль'
                        }
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    'status': 'ERR',
                    'data': {
                        'message': 'Пользователь не существует'
                    }
                }, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({
                'status': 'ERR',
                'data': {
                    'message': 'Ошибка'
                }
            }, status=status.HTTP_400_BAD_REQUEST)


class SignOut(CustomAPIView):
    def post(self, request):
        logout(request)
        return Response({
            'status': 'OK',
            'data': {
                'message': 'Выход из аккаунта успешен'
            }
        }, status=status.HTTP_200_OK)


class EditAccount(CustomAPIView):
    def post(self, request):
        user = CustomUser.objects.get(id=int(request.data['user_id'][0]))
        data = request.data
        print(data)

        if data['avatar'] == 'null':
            user.avatar.delete()

        if data['cap'] == 'null':
            user.cap.delete()

        if data['cap'] != 'null':

            if data['cap'] != 'undefined':
                user.cap = data['cap']

            if data['avatar'] != 'undefined':
                user.avatar = data['avatar']

            if data['full_name'][0]:
                user.full_name = data['full_name']

            try:
                user.description = data['description'][0]
            except:
                user.description = 'Нет описания пользователя.'

            if data['two_factor'] != 'undefined':
                if data['two_factor'] is False:
                    user.code = '0'

                user.two_factor = data['two_factor'][0]

        user.save()

        return Response({
            'status': 'OK',
            'data': {
                'message': 'Профиль изменён'
            }
        }, status=status.HTTP_200_OK)


class CreatePin(CustomAPIView):
    def post(self, request):
        try:
            pin = Pin()
            pin.title = request.data['title']
            pin.image = request.FILES['image']
            pin.owner = CustomUser.objects.get(username=request.data['username'])
            pin.description = request.data['description']
            pin.sourse = request.data['sourse']
            pin.save()

            return Response({
                'status': 'OK',
                'data': {
                    'id': pin.id,
                    'title': pin.title,
                    'description': pin.description,
                }
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'status': 'ERR',
                'data': {
                    'message': 'Ошибка. Возможно не переданы нужные параметры.'
                }
            }, status=status.HTTP_400_BAD_REQUEST)


class EditPin(CustomAPIView):
    def post(self, request):
        try:
            pin = Pin.objects.get(id=request.data['pin_id'])
            pin.title = request.data['title']

            if 'image' in request.FILES:
                pin.image = request.FILES['image']

            pin.description = request.data['description']
            pin.sourse = request.data['sourse']
            pin.save()

            return Response({
                'status': 'OK',
                'data': {
                    'id': pin.id,
                    'title': pin.title,
                    'description': pin.description,
                }
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'status': 'ERR',
                'data': {
                    'message': 'Ошибка. Возможно не переданы нужные параметры.'
                }
            }, status=status.HTTP_400_BAD_REQUEST)


class LikeCheck(CustomAPIView):
    def post(self, request):
        pin = Pin.objects.get(id=request.data['pin_id'])
        owner = CustomUser.objects.get(username=request.data['username'])

        if request.data['set']:
            if Like.objects.filter(pin=pin, owner=owner):
                like = Like.objects.get(pin=pin, owner=owner)
                like.delete()

            else:
                like = Like()
                like.owner = owner
                like.pin = pin
                like.save()

        like = Like.objects.filter(pin=pin, owner=owner)

        return Response({
            'status': 'OK',
            'data': {
                'like': True if like else False,
                'likes_count': Like.objects.filter(pin=pin).count()
            }
        }, status=status.HTTP_200_OK)


class CreateComment(CustomAPIView):
    def post(self, request):
        pin = Pin.objects.get(id=request.data['pin_id'])
        owner = CustomUser.objects.get(username=request.data['username'])
        comment = Comment()
        comment.pin = pin
        comment.owner = owner
        comment.text = request.data['text']
        comment.save()

        return Response({
            'status': 'OK',
            'data': {
                'id': comment.id,
                'owner_id': owner.id,
                'text': comment.text,
                'pin_id': comment.pin.id
            }
        }, status=status.HTTP_200_OK)


class DeleteComment(CustomAPIView):
    def post(self, requests):
        comment = Comment.objects.get(id=requests.data['comment_id'])
        comment.delete()

        return Response({
            'status': 'OK',
            'data': {
                'id': comment.id,
                'owner_id': comment.owner.id,
                'text': comment.text,
                'pin_id': comment.pin.id
            }
        })


class Subscribe(CustomAPIView):
    def post(self, request):
        from_ = CustomUser.objects.get(username=request.data['from_username'])
        to_ = CustomUser.objects.get(username=request.data['to_username'])

        if not from_ in to_.subscribers.all():

            from_.subscriptions.add(to_)
            to_.subscribers.add(from_)

            from_.save()
            to_.save()
        else:
            from_.subscriptions.remove(to_)
            to_.subscribers.remove(from_)

            from_.save()
            to_.save()

        return Response({
            'status': 'OK',
            'data': {
                'message': 'OK',
                'subscribe': from_ in to_.subscribers.all()
            }
        }, status=status.HTTP_200_OK)


class CreateBoard(CustomAPIView):
    def post(self, request):
        board = Board()
        board.owner = CustomUser.objects.get(username=request.data['owner_id'])
        board.name = request.data['name']

        if 'cover' in request.data:
            board.cover = request.FILES['cover']

        board.save()

        return Response({
            'status': 'OK',
            'data': {
                'id': board.id,
                'name': board.name
            }
        }, status=status.HTTP_200_OK)


class DeleteBoard(CustomAPIView):
    def post(self, request):
        board = Board.objects.get(id=request.data['board_id'])
        board.delete()

        return Response({
            'status': 'OK',
            'data': {

            }
        }, status=status.HTTP_200_OK)


class DeletePin(CustomAPIView):
    def post(self, request):
        if Pin.objects.get(id=request.data['pin_id']):
            pin = Pin.objects.get(id=request.data['pin_id'])
            pin.delete()

            return Response({
                'status': 'OK',
                'data': {
                    'id': pin.id,
                    'owner_id': pin.owner.id,
                    'title': pin.title,
                    'description': pin.description,
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'ERR',
                'data': {
                    'message': 'Записи не существует'
                }
            }, status=status.HTTP_400_BAD_REQUEST)


class PinAddToBoard(CustomAPIView):
    def post(self, request):
        board = Board.objects.get(id=int(request.data['board_id']))
        pin = Pin.objects.get(id=int(request.data['pin_id']))

        board.pins.add(pin)
        board.save()

        return Response({
            'status': 'OK',
            'data': {}
        }, status=status.HTTP_200_OK)


class PinDeleteToBoard(CustomAPIView):
    def post(self, request):
        board = Board.objects.get(id=int(request.data['board_id']))
        pin = Pin.objects.get(id=int(request.data['pin_id']))

        board.pins.remove(pin)
        board.save()

        return Response({
            'status': 'OK',
            'data': {}
        }, status=status.HTTP_200_OK)


class NewPassword(CustomAPIView):
    def post(self, request):
        user = CustomUser.objects.get(id=request.data['user_id'])

        if user.check_password(request.data['password']):
            user.set_password(request.data['password1'])
            user.save()

            return Response({
                'status': 'OK',
                'data': {
                    'message': 'Пароль успешно сменён'
                }
            }, status=status.HTTP_200_OK)

        else:
            return Response({
                'status': 'ERR',
                'data': {
                    'message': 'Текущий пароль не верный.'
                }
            }, status=status.HTTP_400_BAD_REQUEST)


class UpdateMessages(CustomAPIView):
    def post(self, request):
        try:
            messages = []
            for i in Message.objects.all():
                if not PinMessage.objects.filter(id=i.id):
                    messages.append({
                        'oti': i.owner.id,
                        'owner_id': i.owner.username,
                        'owner_full_name': i.owner.full_name,
                        'date_of_creation': str(i.date_of_creation).split('.')[0][:-3],
                        'text': i.text,
                        'id': i.id
                    })
                else:
                    message = PinMessage.objects.get(id=i.id)

                    messages.append({
                        'oti': i.owner.id,
                        'owner_id': i.owner.username,
                        'owner_full_name': i.owner.full_name,
                        'date_of_creation': str(i.date_of_creation).split('.')[0][:-3],
                        'text': i.text,
                        'id': i.id,
                        'pin': {
                            'id': message.pin.id,
                            'image': message.pin.image.url
                        }
                    })

            return Response({
                'status': 'OK',
                'data': {
                    'messages': messages[::-1]
                }
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'status': 'ERR',
                'data': {
                    'message': 'Неизвестная ошибка'
                }
            }, status=status.HTTP_400_BAD_REQUEST)


class DeleteMessage(CustomAPIView):
    def post(self, request):
        message = Message.objects.get(id=request.data['message_id'])
        message.delete()

        return Response({
            'status': 'OK',
            'data': {

            }
        }, status=status.HTTP_200_OK)


class SendMessage(CustomAPIView):
    def post(self, request):
        if 'pin_id' in request.data:
            message = PinMessage()
            message.text = request.data['text']
            message.owner = CustomUser.objects.get(username=request.data['owner_id'])
            message.pin = Pin.objects.get(id=request.data['pin_id'])
            message.save()

            return Response({
                'status': 'OK',
                'data': {
                    'id': message.id,
                    'owner_id': message.owner.id,
                    'text': message.text,
                    'pin_id': message.pin.id
                }
            }, status=status.HTTP_200_OK)

        else:
            message = Message()
            message.text = request.data['text']
            if CustomUser.objects.filter(username=request.data['owner_id']):
                message.owner = CustomUser.objects.get(username=request.data['owner_id'])
            else:
                message.owner = CustomUser.objects.get(id=int(request.data['owner_id']))

            message.save()

            return Response({
                'status': 'OK',
                'data': {
                    'id': message.id,
                    'owner_id': message.owner.id,
                    'text': message.text,
                }
            }, status=status.HTTP_200_OK)


class EditMessage(CustomAPIView):
    def post(self, request):
        message = Message.objects.get(id=request.data['message_id'])
        message.text = request.data['text']
        message.save()

        return Response({
            'status': 'OK',
            'data': {

            }
        }, status=status.HTTP_200_OK)


letters = 'abcdefghijklmnopqrstuvwxyz123456789QWERTYUIOPASDFGHJKLZXCVBNMM'


def create_token(user_id):
    token = str(user_id) + ''.join([random.choice(letters) for i in range(20)])
    return token


class SetToken(CustomAPIView):
    def post(self, request):
        if 'owner_id' in request.data:
            owner = CustomUser.objects.get(username=request.data['owner_id'])

            try:
                owner.API_TOKEN = create_token(request.data['owner_id'])
                owner.save()

            except:
                return Response({
                    'status': 'ERR',
                    'data': {
                        'message': 'Ошибка. Пользователь с таким ID не найден.'
                    }
                })

            msg = MIMEMultipart()
            msg['Subject'] = 'API-TOKEN Pinboard 📍'
            msg.attach(MIMEText(f'{owner.username}, привет 👋\n'
                                f'Вот твой token: {owner.API_TOKEN}\n\n'
                                f'Благодарим за использование Pinboard 📍 ❤', 'plain'))

            server = smtplib.SMTP('smtp.gmail.com: 587')
            server.starttls()
            server.login(server_email, server_password)
            server.sendmail(server_email, owner.email, msg.as_string())

            return Response({
                'status': 'success',
                'data': {
                    'token': owner.API_TOKEN
                }
            })
        else:
            return Response({
                'status': 'error',
                'data': {
                    'message': 'Переданы не все параметры.'
                }
            })


class GetUserBoards(CustomAPIView):
    def get(self, request):
        if CustomUser.objects.filter(username=request.GET['user_id']):
            user = CustomUser.objects.get(username=request.GET['user_id'])

            boards = Board.objects.filter(owner=user)
            boards_list = []

            for i in boards:
                boards_list.append(
                    {
                        'id': i.id,
                        'name': i.name
                    }
                )

            return Response({
                'status': 'OK',
                'data': {
                    'count': len(boards_list),
                    'boards': boards_list
                }
            })
        else:
            return Response({
                'status': 'ERR',
                'data': {
                    'message': 'Объекта не существует.'
                }
            })


class GeneralApi(CustomAPIView):
    def get(self, request):
        if 'token' in request.GET:
            if CustomUser.objects.filter(API_TOKEN=request.GET['token']):
                user = CustomUser.objects.get(API_TOKEN=request.GET['token'])

                if 'method' in request.GET:
                    method = request.GET['method']
                    if method == 'getUserInfo':
                        if CustomUser.objects.filter(username=request.GET['user_id']):
                            user = CustomUser.objects.get(username=request.GET['user_id'])
                            return Response({
                                'status': 'OK',
                                'data': {
                                    'id': user.username,
                                    'full_name': user.full_name,
                                    'description': user.description,
                                    'avatar': user.avatar.url if user.avatar.url else 'Фото профиля не установлено',
                                    'cap': user.cap.url if user.cap else 'Шапка не установлена'
                                }
                            })
                        else:
                            return Response({
                                'status': 'ERR',
                                'data': {
                                    'message': 'Объекта не существует.'
                                }
                            })

                    elif method == 'setOnline':
                        user.last_online = timezone.now()
                        user.save()

                        return Response({
                            'status': 'OK',
                            'data': {
                                'message': 'Статус "онлайн" устанолвен на 5 минут.'
                            }
                        })

                    elif method == 'getUserSubscribers':
                        if CustomUser.objects.filter(username=request.GET['user_id']):
                            user = CustomUser.objects.get(username=request.GET['user_id'])

                            subscribers = []

                            for i in user.subscribers.all():
                                subscribers.append(
                                    {
                                        'id': i.username,
                                        'full_name': i.full_name
                                    }
                                )

                            return Response({
                                'status': 'OK',
                                'data': {
                                    'count': len(subscribers),
                                    'subscribers': subscribers
                                }
                            })
                        else:
                            return Response({
                                'status': 'ERR',
                                'data': {
                                    'message': 'Объекта не существует.'
                                }
                            })

                    elif method == 'getPinInfo':
                        if Pin.objects.filter(id=request.GET['pin_id']):
                            pin = Pin.objects.get(id=request.GET['pin_id'])

                            return Response({
                                'status': 'OK',
                                'data': {
                                    'pin_id': pin.id,
                                    'owner_id': pin.owner.username,
                                    'title': pin.title,
                                    'description': pin.description,
                                    'image': pin.image.url,
                                }
                            })
                        else:
                            return Response({
                                'status': 'ERR',
                                'data': {
                                    'message': 'Объекта не существует.'
                                }
                            })

                    elif method == 'getPinComments':
                        if Pin.objects.filter(id=request.GET['pin_id']):
                            pin = Pin.objects.get(id=request.GET['pin_id'])
                            comments = Comment.objects.filter(pin=pin)

                            comments_list = []

                            for i in comments:
                                comments_list.append(
                                    {
                                        'id': i.id,
                                        'owner_id': i.owner.username,
                                        'text': i.text,
                                        'date_of_creation': i.date_of_creation
                                    }
                                )

                            return Response({
                                'status': 'OK',
                                'data': {
                                    'count': len(comments_list),
                                    'subscribers': comments_list
                                }
                            })
                        else:
                            return Response({
                                'status': 'ERR',
                                'data': {
                                    'message': 'Объекта не существует.'
                                }
                            })

                    elif method == 'getCommentInfo':
                        if Comment.objects.filter(id=request.GET['comment_id']):
                            comment = Comment.objects.get(id=request.GET['comment_id'])

                            return Response({
                                'status': 'OK',
                                'data': {
                                    'id': comment.id,
                                    'owner_id': comment.owner.username,
                                    'pin_id': comment.pin.id,
                                    'text': comment.text,
                                    'date_of_creation': comment.date_of_creation
                                }
                            })
                        else:
                            return Response({
                                'status': 'ERR',
                                'data': {
                                    'message': 'Объекта не существует.'
                                }
                            })

                    elif method == 'getUserPins':
                        if CustomUser.objects.filter(username=request.GET['user_id']):
                            user = CustomUser.objects.get(username=request.GET['user_id'])

                            pins = Pin.objects.filter(owner=user)
                            pins_list = []

                            for i in pins:
                                pins_list.append(
                                    {
                                        'id': i.id,
                                        'title': i.title
                                    }
                                )

                            return Response({
                                'status': 'OK',
                                'data': {
                                    'count': len(pins_list),
                                    'boards': pins_list
                                }
                            })
                        else:
                            return Response({
                                'status': 'ERR',
                                'data': {
                                    'message': 'Объекта не существует.'
                                }
                            })

                    #   CHAT API

                    elif method == 'deleteMessage':
                        if Message.objects.filter(id=request.GET['message_id']):
                            message = Message.objects.get(id=request.GET['message_id'])

                            print(message.owner, user)

                            if message.owner == user:
                                message.delete()

                                return Response({
                                    'status': 'OK',
                                    'data': {

                                    }
                                })

                            else:
                                return Response({
                                    'status': 'ERR',
                                    'data': {
                                        'message': 'Сообщение не пренадлежит вам.'
                                    }
                                })
                        else:
                            return Response({
                                'status': 'ERR',
                                'data': {
                                    'message': 'Объекта не существует.'
                                }
                            })

                    elif method == 'sendMessage':
                        if 'pin_id' in request.GET:
                            message = PinMessage()
                            if Pin.objects.filter(id=request.GET['pin_id']):
                                message.pin = Pin.objects.get(id=request.GET['pin_id'])
                            else:
                                return Response({
                                    'status': 'ERR',
                                    'data': {
                                        'message': 'Объект не существует.'
                                    }
                                })
                        else:
                            if 'text' in request.GET:
                                message = Message()
                                message.text = request.GET['text']
                            else:
                                return Response({
                                    'status': 'ERR',
                                    'data': {
                                        'message': 'Не переданы некоторые параметры.'
                                    }
                                })

                        message.owner = user
                        message.save()

                        return Response({
                            'status': 'OK',
                            'data': {
                                'id': message.id,
                                'owner_id': message.owner.id,
                                'text': message.text,
                            }
                        })


                    elif method == 'chatListen':
                        message = Message.objects.all()[::-1][0]

                        if PinMessage.objects.filter(id=message.id):
                            message = PinMessage.objects.get(id=message.id)
                            return Response({
                                'status': 'OK',
                                'data': {
                                    'id': message.id,
                                    'owner_id': message.owner.id,
                                    'text': message.text,
                                    'date_of_creation': str(message.date_of_creation).split('.')[0][:-3],
                                    'pin': {
                                        'id': message.pin.id
                                    }
                                }
                            })
                        return Response({
                            'status': 'OK',
                            'data': {
                                'id': message.id,
                                'owner_id': message.owner.id,
                                'text': message.text,
                                'date_of_creation': str(message.date_of_creation).split('.')[0][:-3]
                            }
                        })

                    else:
                        return Response({
                            'status': 'ERR',
                            'data': {
                                'message': 'Метода не существует.'
                            }
                        })

                else:
                    return Response({
                        'status': 'ERR',
                        'data': {
                            'message': ' Не передан параметр: method'
                        }
                    })
            else:
                return Response({
                    'status': 'ERR',
                    'data': {
                        'message': 'Неверный параметр: token.'
                    }
                })
        else:
            return Response({
                'status': 'ERR',
                'data': {
                    'message': ' Не передан параметр: token'
                }
            })
