from django.views.generic import TemplateView, DetailView
from .models import *


class MainView(TemplateView):
    template_name = 'pages/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pins'] = Pin.objects.all()[::-1]
        return context


class AccountView(TemplateView):
    template_name = 'pages/account.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        user = CustomUser.objects.get(username=self.kwargs['username'])

        subscribe = False
        if self.request.user in user.subscribers.all():
            subscribe = True

        context = super().get_context_data(**kwargs)
        context['user'] = user
        context['subscribe'] = subscribe
        context['pins'] = Pin.objects.filter(owner=user)
        context['boards'] = Board.objects.filter(owner=user)
        return context


class PinView(TemplateView):
    template_name = 'pin/pin-view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pin = Pin.objects.get(id=self.kwargs['pin_id'])
        pin.views += 1
        pin.save()
        context['comments'] = Comment.objects.filter(pin=pin).count()
        context['pin'] = pin
        return context


class PinBuilderView(TemplateView):
    template_name = 'pin/pin-builder.html'


class PinCommentsView(TemplateView):
    template_name = 'pin/pin-comments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pin = Pin.objects.get(id=self.kwargs['pin_id'])
        context['comments'] = Comment.objects.filter(pin=pin)[::-1]
        context['pin'] = pin
        return context


class BoardView(TemplateView):
    template_name = 'board/board-view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['board'] = Board.objects.get(id=self.kwargs['board_id'])

        return context


class BoardBuilderView(TemplateView):
    template_name = 'board/board-builder.html'


from django.db.models import Q


class SearchView(TemplateView):
    template_name = 'pages/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'q' in self.request.GET:
            context['pins'] = Pin.objects.filter(Q(title__contains=self.request.GET['q']) | Q(description__contains=self.request.GET['q']))

        return context


class ApiDocsView(TemplateView):
    template_name = 'pages/api.html'
