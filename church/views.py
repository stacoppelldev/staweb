import json
import cloudinary
from datetime import datetime, timedelta
from os import environ as env
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives, send_mail
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse
from django.views.generic import TemplateView
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import event, time, reading, announcement, faq, banner, PhotoAlbum
from .forms import ContactForm, ReserveAuditoriumForm

class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = datetime.today().strftime('%Y-%m-%d')
        latestAlbum = PhotoAlbum.objects.order_by('-start_date').first()

        context['events'] = event.objects.filter(start_date__gte=today).filter(event_status='Active').order_by('start_date')
        context['sundayMassMalayalam1'] = time.objects.get(title='Holy Qurbana Malayalam1')
        context['sundayMassMalayalam'] = time.objects.get(title='Holy Qurbana Malayalam')
        context['sundayMassEnglish'] = time.objects.get(title='Holy Qurbana English')
        #context['weekdayMassMTWS'] = time.objects.get(title='Weekday Mass MTWS')
        #context['weekdayMassTTH'] = time.objects.get(title='Weekday Mass TTH')
        context['weekdayMassTS'] = time.objects.get(title='Weekday Mass TS')
        context['weekdayMassMF'] = time.objects.get(title='Weekday Mass MF')
        context['weekdayExtMass'] = time.objects.get(title='Weekday Extension Mass')
        #context['adorationMTWS'] = time.objects.get(title='Adoration MTWS')
        #context['adorationTHF'] = time.objects.get(title='Adoration THF')
        context['adorationTS'] = time.objects.get(title='Adoration TS')
        context['confession'] = time.objects.get(title='Confession')
        try:
            context['reading'] = reading.objects.get(date=today)
        except:
            pass
        context['announcements'] = announcement.objects.all().order_by('order')
        context['faqs'] = faq.objects.all()
        context['banners'] = banner.objects.all()
        context['photoAlbums'] = getPhotoAlbums()
        context['latestAlbum'] = latestAlbum
        context['latestAlbumPhotos'] = getLatestAlbumPhotos(latestAlbum)
        context['reserve_auditorium_form']  = ReserveAuditoriumForm()
        context['contact_form'] = ContactForm()
        return context

    def get(self, request):
        return render(request, 'church/yummy/index.html', self.get_context_data())

class PhotoAlbumView(TemplateView):
    template_name = 'church/yummy/media.html'

    def get_context_data(self, **kwargs):
        context = super(PhotoAlbumView, self).get_context_data(**kwargs)

        pStartDate = self.kwargs['startDate']
        pSlug      = self.kwargs['slug']
        startDate  = datetime.strptime(pStartDate, '%Y-%m-%d').date()

        cloudinaryExp    = 'folder:"media/photos/' + str(startDate.year) + '/' + pSlug + '"'
        cloudinaryImages = []
        cloudinaryFolder = cloudinary.Search()\
            .expression(cloudinaryExp)\
            .sort_by('public_id', 'desc')\
            .max_results('30')\
            .execute()

        for asset in cloudinaryFolder['resources']:
            cloudinaryImages.append(asset['secure_url'])

        context['photoAlbums'] = getPhotoAlbums()
        context['album'] = PhotoAlbum.objects.filter(start_date=pStartDate).filter(slug=pSlug).get()
        context['photos'] = cloudinaryImages
        return context

def processReservationRequest(request):
    reserveAuditoriumForm = ReserveAuditoriumForm(request.POST)
    if reserveAuditoriumForm.is_valid():
        sendReservationRequestMail(reserveAuditoriumForm)
        return JsonResponse({ 'status': True })
    else:
        return JsonResponse({ 'status': False, 'errors': reserveAuditoriumForm.errors })

def processContactUs(request):
    contactForm = ContactForm(request.POST)
    if contactForm.is_valid():
        sendContactUsMail(contactForm)
        return JsonResponse({ 'status': True })
    else:
        return JsonResponse({ 'status': False, 'errors': contactForm.errors })


# UNUSED (FOR NOW)

class CalendarView(TemplateView):
    template_name = 'church/yummy/calendar.html'

    def get_context_data(self, **kwargs):
        context = super(CalendarView, self).get_context_data(**kwargs)

        events = event.objects.all()
        eventsObj = [{
            'title' : x.title,
            'start' : x.start_date,
            'id'    : x.id,
            # 'url'   : x.get_absolute_url()
        } for x in events]

        context['events'] = json.dumps(eventsObj, cls=DjangoJSONEncoder)
        return context


# UTIL FUNCTION

def getPhotoAlbums():
    a = dict()
    albums = PhotoAlbum.objects.all().order_by('start_date')

    for album in albums:
        c = {
            'year': album.start_date.year,
            'start_date': album.start_date,
            'slug': album.slug,
            'title': album.title
        }

        if (album.start_date.year in a.keys()):
            # GET THE VALUE FOR THAT YEAR & ADD TO IT
            b = a.get(album.start_date.year)
            b.append(c)
            a[album.start_date.year] = b
        else:
            # CREATE A NEW YEAR AND ADD TO IT
            d = []
            d.append(c)
            a[album.start_date.year] = d

    return a

def getLatestAlbumPhotos(latestAlbum):
    cloudinaryExp    = 'folder:"media/photos/' + str(latestAlbum.start_date.year) + '/' + latestAlbum.slug + '"'
    cloudinaryImages = []
    cloudinaryFolder = cloudinary.Search()\
        .expression(cloudinaryExp)\
        .sort_by('public_id', 'desc')\
        .max_results('30')\
        .execute()

    for asset in cloudinaryFolder['resources']:
        cloudinaryImages.append(asset['secure_url'])

    return cloudinaryImages

def sendReservationRequestMail(reserveAuditoriumForm):
    form_data = reserveAuditoriumForm.cleaned_data
    context = {
        'name'   : form_data['name'],
        'email'  : form_data['email'],
        'phone'  : form_data['phone'],
        'date'   : form_data['date'],
        'time'   : form_data['time'],
        'people' : form_data['people']
    }

    html_message = render_to_string('church/email/reservation-request.html', context=context)
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject='[STAWeb] Auditorium Reservation Request: ' + form_data['name'],
        body=plain_message,
        from_email='devalphonsa@gmail.com',
        to=[env['MAIL_TO_RESERVATION_REQUEST']],
        cc=[env['MAIL_CC_ALL']]
    )
    message.attach_alternative(html_message, 'text/html')
    message.send()

def sendContactUsMail(contactForm):
    form_data = contactForm.cleaned_data
    context = {
        'name'    : form_data['name'],
        'email'   : form_data['email'],
        'subject' : form_data['subject'],
        'message' : form_data['message']
    }

    html_message = render_to_string('church/email/contact-us.html', context=context)
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject='[STAWeb] Contact Us: ' + form_data['name'],
        body=plain_message,
        from_email='devalphonsa@gmail.com',
        to=[env['MAIL_TO_CONTACT_US']],
        cc=[env['MAIL_CC_ALL']]
    )
    message.attach_alternative(html_message, 'text/html')
    message.send()
