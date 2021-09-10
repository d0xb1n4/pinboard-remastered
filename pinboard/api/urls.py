from django.urls import path
from .views import *
from .api import *

urlpatterns = [
    # api

    # sign
    path('api/general/', GeneralApi.as_view(), name='general__api'),

    path('api/signIn/', SignIn.as_view(), name='sign__in'),
    path('api/signUp/', SignUp.as_view(), name='sign__up'),
    path('api/checkAuthCode/', CheckAuthCode.as_view(), name='check__auth__code'),
    path('api/cancelSignUp/', CancelSignUp.as_view(), name='cancel__sign__up'),

    path('api/signIn/', SignIn.as_view(), name='sign__in'),

    path('api/signOut/', SignOut.as_view(), name='sign__out'),

    path('api/editAccount/', EditAccount.as_view(), name='edit__account'),

    path('api/createPin/', CreatePin.as_view(), name='create__pin'),

    path('api/editPin/', EditPin.as_view(), name='edit__pin'),

    path('api/likeCheck/', LikeCheck.as_view(), name='like__check'),

    path('api/createComment/', CreateComment.as_view(), name='create__comment'),
    path('api/deleteComment/', DeleteComment.as_view(), name='delete__comment'),

    path('api/subscribe/', Subscribe.as_view(), name='subscribe'),

    path('api/createBoard/', CreateBoard.as_view(), name='create__board'),
    path('api/deleteBoard/', DeleteBoard.as_view(), name='delete__board'),

    path('api/pinAddToBoard/', PinAddToBoard.as_view(), name='pin__add__to__board'),
    path('api/pinDeleteToBoard/', PinDeleteToBoard.as_view(), name='pin__delete__to__board'),

    path('api/deletePin/', DeletePin.as_view(), name='delete__pin'),

    path('api/newPassword/', NewPassword.as_view(), name='check__user__password'),

    # views
    path('', MainView.as_view(), name='main'),
    path('user/<str:username>/', AccountView.as_view(), name='account'),

    path('pin/<int:pin_id>/comments/', PinCommentsView.as_view(), name='pin_comments'),
    path('pin/builder/', PinBuilderView.as_view(), name='pin_builder'),
    path('pin/<int:pin_id>/', PinView.as_view(), name='pin_view'),

    path('board/<int:board_id>/', BoardView.as_view(), name='board_view'),
    path('board/builder/', BoardBuilderView.as_view(), name='board_builder'),

    path('search/', SearchView.as_view(), name='search'),

    path('api/', ApiDocsView.as_view(), name='api_docs')
]
