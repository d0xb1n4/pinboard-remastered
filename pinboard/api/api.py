from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .models import *
from .config import *


class SignUp(APIView):
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


class CheckAuthCode(APIView):
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


class CancelSignUp(APIView):
    def post(self, request):
        user = CustomUser.objects.get(id=request.data['user_id'])
        user.delete()


class SignIn(APIView):
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


class SignOut(APIView):
    def post(self, request):
        logout(request)
        return Response({
            'status': 'OK',
            'data': {
                'message': 'Выход из аккаунта успешен'
            }
        }, status=status.HTTP_200_OK)


class EditAccount(APIView):
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

            if data['description'][0]:
                user.description = data['description']

            if data['two_factor'][0] != 'undefined':
                if data['two_factor'][0] is False:
                    user.code = '0'

                user.two_factor = data['two_factor'][0]

        user.save()

        return Response({
            'status': 'OK',
            'data': {
                'message': 'Профиль изменён'
            }
        }, status=status.HTTP_200_OK)


class CreatePin(APIView):
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


class EditPin(APIView):
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


class LikeCheck(APIView):
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


class CreateComment(APIView):
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


class DeleteComment(APIView):
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


class Subscribe(APIView):
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


class CreateBoard(APIView):
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


class DeleteBoard(APIView):
    def post(self, request):
        board = Board.objects.get(id=request.data['board_id'])
        board.delete()

        return Response({
            'status': 'OK',
            'data': {

            }
        }, status=status.HTTP_200_OK)


class DeletePin(APIView):
    def post(self, request):
        print(request.user.id)

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


class PinAddToBoard(APIView):
    def post(self, request):
        board = Board.objects.get(id=int(request.data['board_id']))
        pin = Pin.objects.get(id=int(request.data['pin_id']))

        board.pins.add(pin)
        board.save()

        return Response({
            'status': 'OK',
            'data': {}
        }, status=status.HTTP_200_OK)


class PinDeleteToBoard(APIView):
    def post(self, request):
        board = Board.objects.get(id=int(request.data['board_id']))
        pin = Pin.objects.get(id=int(request.data['pin_id']))

        board.pins.remove(pin)
        board.save()

        return Response({
            'status': 'OK',
            'data': {}
        }, status=status.HTTP_200_OK)


class NewPassword(APIView):
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
            })

        else:
            return Response({
                'status': 'ERR',
                'data': {
                    'message': 'Текущий пароль не верный.'
                }
            }, status=status.HTTP_400_BAD_REQUEST)


class GeneralApi(APIView):
    def get(self, request):
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
                            'message': 'Обьекта не существует.'
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
                            'message': 'Обьекта не существует.'
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
                            'message': 'Обьекта не существует.'
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
                            'message': 'Обьекта не существует.'
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
                            'message': 'Обьекта не существует.'
                        }
                    })

            elif method == 'getUserBoards':
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
                            'message': 'Обьекта не существует.'
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
                            'message': 'Обьекта не существует.'
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
