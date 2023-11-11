from django.urls import path
from . import views
from .views import home, media, send_email, calendar

urlpatterns = [
    path('', home.as_view(), name='home'),
    path('media/<str:year>/<str:event>/', media.as_view(), name='media'),
    path('send-email/', send_email, name='send-email'),
    path('calendar/', calendar.as_view(), name='calendar')
]
