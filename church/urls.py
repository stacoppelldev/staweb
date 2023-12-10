from django.urls import path
from .views import HomeView, processReservationRequest, processContactUs, PhotoAlbumView, CalendarView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('media/<str:startDate>/<str:slug>/', PhotoAlbumView.as_view(), name='media'),
    path('reserve-auditorium/', processReservationRequest, name='e-reserve-auditorium'),
    path('contact-us/', processContactUs, name='e-contact-us'),
    path('calendar/', CalendarView.as_view(), name='calendar')
]
