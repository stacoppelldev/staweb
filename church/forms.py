from django.forms import ModelForm
from .models import event, time, reading, announcement, faq, banner
from django import forms
from django.forms import ModelForm
from django.core.mail import send_mail



class addEventForm(forms.ModelForm):

    class Meta:
        model = event
        fields = ['title', 'start_date', 'start_time', 'description', 'cover_image', 'event_image', 'event_files']

class addFAQForm(forms.ModelForm):

    class Meta:
        model = faq
        fields = ['question', 'answer']

class addAnnouncementForm(forms.ModelForm):

    class Meta:
        model = announcement
        fields = ['message', 'details', 'details2', 'order']

class addBannerForm(forms.ModelForm):

    class Meta:
        model = banner
        fields = ['message', 'hyperlink']

class addFAQ(forms.ModelForm):

    class Meta:
        model = faq
        fields = ['question', 'answer']

class updateEventForm(forms.ModelForm):

    class Meta:
        model = event
        fields = ['title', 'start_date', 'start_time', 'description', 'event_status', 'cover_image', 'event_image', 'event_files']

class updateBannerForm(forms.ModelForm):

    class Meta:
        model = banner
        fields = ['message', 'hyperlink']

class updateAnnouncementForm(forms.ModelForm):

    class Meta:
        model = announcement
        fields = ['message', 'order']

class updateTimeForm(forms.ModelForm):

    class Meta:
        model = time
        fields = ['title', 'time']

class updateReadingForm(forms.ModelForm):

    class Meta:
        model = reading
        fields = ['date', 'reading_1', 'reading_2', 'gospel']

class updateFAQForm(forms.ModelForm):

    class Meta:
        model = faq
        fields = ['question', 'answer']

class contactForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    subject = forms.CharField(label='Subject', max_length=100)
    email = forms.CharField(label='Email', max_length=100)
    cell = forms.CharField(label='Cell', max_length=100)
    message = forms.CharField(label='Message', max_length=500)

    def clean(self):
        user_email = self.cleaned_data['user_email']
        send_mail('test', 'test', 'devalphonsa@gmail.com', [user_email])



