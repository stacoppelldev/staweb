from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import FormMixin
from django.views.generic import CreateView, TemplateView, UpdateView, ListView, FormView
from .models import event, time, reading, announcement, faq, banner, page
from .forms import (contactForm, addFAQForm, addBannerForm, addEventForm,
 addAnnouncementForm, updateBannerForm, updateFAQForm, updateAnnouncementForm,
  updateEventForm, updateTimeForm, updateReadingForm)
from django.contrib.auth.decorators import user_passes_test
from django.core import serializers
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from django.urls import reverse
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import logout as auth_logout

@user_passes_test(lambda u: u.is_superuser)
def alphonsa(request):
    return render(request, 'church/admin/alphonsa.html', {'title': 'Home'})

class homeView(TemplateView):
    template_name = "church/index2.html"
    
    def get_context_data(self, **kwargs):
        context = super(homeView, self).get_context_data(**kwargs)

        today = datetime.today().strftime('%Y-%m-%d')
        context['events'] = event.objects.filter(start_date__gte=today,start_date__lte=("2025-01-26")).filter(event_status='Active').order_by("start_date")
        context['sundayMassMalayalam1'] = time.objects.get(title="Holy Qurbana Malayalam1")
        context['sundayMassMalayalam'] = time.objects.get(title="Holy Qurbana Malayalam")
        context['sundayMassEnglish'] = time.objects.get(title="Holy Qurbana English")
        context['weekdayMassMTWS'] = time.objects.get(title="Weekday Mass MTWS")
        context['weekdayMassTTH'] = time.objects.get(title="Weekday Mass TTH")
        context['adorationMTWS'] = time.objects.get(title="Adoration MTWS")
        context['adorationTHF'] = time.objects.get(title="Adoration THF")
        context['confession'] = time.objects.get(title="Confession")
        try:
            context['reading'] = reading.objects.get(date=today)
        except:
            pass
        context['announcement'] = announcement.objects.all().order_by('order')
        context['faqs'] = faq.objects.all()
        context['banners'] = banner.objects.all()
        return context

def about(request):
    return render(request, 'church/about.html', {'title': 'About'})

def faithFormation(request):
    return render(request, 'church/faithFormation.html', {'title': 'About'})

def sacraments(request):
    return render(request, 'church/sacraments.html', {'title': 'About'})

def give(request):
    return render(request, 'church/give.html', {'title': 'About'})

def getInvolved(request):
    return render(request, 'church/getInvolved.html', {'title': 'About'})

class pageView(TemplateView):
    template_name = "church/template.html"

    def get_context_data(self, **kwargs):
        context = super(pageView, self).get_context_data(**kwargs)
        pageName = self.kwargs.get("name")
        context['pageContent'] = page.objects.get(title=pageName)
        print(page.objects.filter(title=pageName))
        return context

class templateOptions(TemplateView):
    template_name = "church/templateOptions.html"

class calendar(TemplateView):
    template_name = "church/calendar.html"

    def get_context_data(self, **kwargs):
        context = super(calendar, self).get_context_data(**kwargs)
        e = event.objects.all()
        e_vents = [{'title': x.title, 'start': x.start_date, 'id': x.id, 'url': x.get_absolute_url()} for x in e]
        context['events'] = json.dumps(e_vents, cls=DjangoJSONEncoder)
        print(context)
        return context

    # def get_context_data(self, **kwargs):
    #     context = super(calendar, self).get_context_data(**kwargs)
    #     context['eventss'] = serializers.serialize('json', event.objects.filter(pk=1))
    #     print(context)
    #     return context

def meetTheVicars(request):
    return render(request, 'church/meetTheVicars.html', {'title': 'About'})

# def contact(request):
#     return render(request, 'church/contactUs.html', {'title': 'About'})

# def contactUs(request):
#     return render(request, 'church/contactUs.html', {'title': 'About'})

class contact(SuccessMessageMixin, FormView):
    template_name = 'church/contactUs.html'
    form_class = contactForm
    success_url = '/'
    success_message = "Message successfully sent"

def services(request):
    return render(request, 'church/services.html')

class massTimes(TemplateView):
    template_name = "church/massTimes.html"
    model = time

    def get_context_data(self, **kwargs):
        context = super(massTimes, self).get_context_data(**kwargs)
        context['sundayMassMalayalam1'] = time.objects.get(title="Holy Qurbana Malayalam1")
        context['sundayMassMalayalam'] = time.objects.get(title="Holy Qurbana Malayalam")
        context['sundayMassEnglish'] = time.objects.get(title="Holy Qurbana English")
        context['weekdayMassMTWS'] = time.objects.get(title="Weekday Mass MTWS")
        context['weekdayMassTTH'] = time.objects.get(title="Weekday Mass TTH")
        return context

class FAQ(TemplateView):
    template_name = 'church/FAQ.html'
    model = faq

    def get_context_data(self, **kwargs):
        context = super(FAQ, self).get_context_data(**kwargs)
        context['faqs'] = faq.objects.all()
        return context

class eventDetails(TemplateView):
    template_name = 'church/eventDetails.html'
    model = event

    def get_context_data(self, **kwargs):
        context = super(eventDetails, self).get_context_data(**kwargs)
        e = self.kwargs.get('pk')
        context['events'] = event.objects.filter(id=e)
        return context

class announcementDetails(TemplateView):
    template_name = 'church/announcementDetails.html'
    model = announcement

    def get_context_data(self, **kwargs):
        context = super(announcementDetails, self).get_context_data(**kwargs)
        e = self.kwargs.get('pk')
        context['announcements'] = announcement.objects.filter(id=e)
        return context

class readingDetails(TemplateView):
    template_name = 'church/readingDetails.html'
    model = reading

    def get_context_data(self, **kwargs):
        context = super(readingDetails, self).get_context_data(**kwargs)
        e = self.kwargs.get('pk')
        context['readings'] = reading.objects.filter(id=e)
        return context

class media(TemplateView):
    template_name = 'church/media.html'


# ADMIN VIEWS
# CREATE

class addEvent(CreateView):
    template_name = 'church/admin/addEvent.html'
    model = event
    form_class = addEventForm
    success_url = 'events'


    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, 'Event added successfully')
        return super().form_valid(form)

class addBanner(CreateView):
    template_name = 'church/admin/addBanner.html'
    model = banner
    form_class = addBannerForm
    success_url = 'banners'

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, 'Banner added successfully')
        return super().form_valid(form)

class addAnnouncement(CreateView):
    template_name = 'church/admin/addAnnouncement.html'
    model = announcement
    form_class = addAnnouncementForm
    success_url = 'announcements'

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, 'Announcement added successfully')
        return super().form_valid(form)

class addFAQ(CreateView):
    template_name = 'church/admin/addFAQ.html'
    model = faq
    form_class = addFAQForm
    success_url = 'FAQS'

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, 'FAQ added successfully')
        return super().form_valid(form)

# UPDATE

class updateTime(UpdateView):
    template_name = 'church/admin/updateTime.html'
    model = time
    form_class = updateTimeForm
    success_url = '/times'

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, 'Updated successfully')
        return super().form_valid(form)

class updateBanner(UpdateView):
    template_name = 'church/admin/updateBanner.html'
    model = banner
    form_class = updateBannerForm
    success_url = '/banners'

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, 'Updated successfully')
        return super().form_valid(form)

class updateReading(UpdateView):
    template_name = 'church/admin/updateReading.html'
    model = reading
    form_class = updateReadingForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, 'Updated successfully')
        return super().form_valid(form)

class updateEvent(UpdateView):
    template_name = 'church/admin/updateEvent.html'
    model = event
    form_class = updateEventForm
    success_url = '/events'

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, 'Updated successfully')
        return super().form_valid(form)

class updateAnnouncement(UpdateView):
    template_name = 'church/admin/updateAnnouncement.html'
    model = announcement
    form_class = updateAnnouncementForm
    success_url = '/announcements'

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, 'Updated successfully')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(updateAnnouncement, self).get_context_data(**kwargs)
        return context

class updateFAQ(UpdateView):
    template_name = 'church/admin/updateFAQ.html'
    model = faq
    form_class = updateFAQForm
    success_url = '/FAQS'

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        messages.success(self.request, 'Updated successfully')
        return super().form_valid(form)

# READ (LISTING)

class timeList(ListView):
    model = time
    template_name = 'church/admin/times.html'
    context_object_name = 'times'
    paginate_by = 40

    def get_queryset(self):
        return time.objects.all()

class bannerList(ListView):
    model = banner
    template_name = 'church/admin/banners.html'
    context_object_name = 'banners'
    paginate_by = 40

    def get_queryset(self):
        return banner.objects.all()

class readingList(ListView):
    model = reading
    template_name = 'church/admin/readings.html'
    context_object_name = 'readings'
    paginate_by = 40

    def get_queryset(self):
        return reading.objects.all()

class eventList(ListView):
    model = event
    template_name = 'church/admin/events.html'
    context_object_name = 'events'
    paginate_by = 40

    def get_queryset(self):
        return event.objects.all()

class announcementList(ListView):
    model = announcement
    template_name = 'church/admin/announcements.html'
    context_object_name = 'announcement'
    paginate_by = 40

    def get_queryset(self):
        return announcement.objects.all()

class FAQList(ListView):
    model = faq
    template_name = 'church/admin/FAQS.html'
    context_object_name = 'FAQS'
    paginate_by = 40

    def get_queryset(self):
        return faq.objects.all()


def send_email(request):
    e = request.POST['email']
    # send_mail('Thank you for subscribing', 'Subscribed Successfully', 'devalphonsa@gmail.com', [e])
    messages.success(request, 'Successfully subscribed!')
    return HttpResponseRedirect('/')

# Admin Logout
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')