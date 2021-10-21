from django.urls import path

from .views import TopView, RoomDetailView

app_name = 'chatapp'
urlpatterns = [
    path('', TopView.as_view(), name='top'),
    path('rooms/<uuid:pk>/', RoomDetailView.as_view(), name='room'),
]
