from django.urls import path
from . import views
from .views import (
    homeView,
    bannerList, FAQList, eventList, announcementList, timeList, readingList,
    addBanner, addFAQ, addEvent, addAnnouncement, 
    updateBanner, updateFAQ, updateEvent, updateAnnouncement, updateTime, updateReading,
    calendar, media, send_email, logout)

urlpatterns = [
    path('', homeView.as_view(), name='home'),
    path('calendar/', calendar.as_view(), name='calendar'),
    path('media/<str:year>/<str:event>/', media.as_view(), name='media'),
    path('send-email/', send_email, name='send-email'),

    # ADMIN
    path('alphonsa', views.alphonsa, name='alphonsa'),
    path('add-event', addEvent.as_view(), name='add-event'),
    path('add-banner', addBanner.as_view(), name='add-banner'),
    path('add-announcement', addAnnouncement.as_view(), name='add-announcement'),
    path('add-FAQ', addFAQ.as_view(), name='add-FAQ'),
    path('update-time/<int:pk>', updateTime.as_view(), name='update-time'),
    path('update-reading/<int:pk>', updateReading.as_view(), name='update-reading'),
    path('update-event/<int:pk>', updateEvent.as_view(), name='update-event'),
    path('update-banner/<int:pk>', updateBanner.as_view(), name='update-banner'),
    path('update-announcement/<int:pk>', updateAnnouncement.as_view(), name='update-announcement'),
    path('update-FAQ/<int:pk>', updateFAQ.as_view(), name='update-FAQ'),
    path('times', timeList.as_view(), name='times'),
    path('readings', readingList.as_view(), name='readings'),
    path('events', eventList.as_view(), name='events'),
    path('FAQS', FAQList.as_view(), name='FAQS'),
    path('banners', bannerList.as_view(), name='banners'),

    path('logout/', logout, name='logout'),
]
