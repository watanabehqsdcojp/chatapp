from django.db import models
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from django.contrib.auth import get_user_model

from .models import Room


class TopView(TemplateView):
    template_name = 'chatapp/top.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rooms'] = Room.objects.filter(users__in=[self.request.user])

        rooms = Room.objects.filter(users__in=[self.request.user])

        context['friends'] = get_user_model().objects.exclude(pk=self.request.user.pk)
        return context


class RoomDetailView(DetailView):
    model = Room
    template_name = 'chatapp/room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_name'] = self.get_object().id
        return context
