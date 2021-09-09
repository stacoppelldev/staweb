from django.forms import ModelForm
from .models import event, time, reading, announcement, detail, faq, banner
from django import forms
from django.forms import ModelForm
from django.core.mail import send_mail
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout




class addEventForm(forms.ModelForm):

    class Meta:
        model = event
        fields = ['title', 'start_date', 'start_time', 'description', 'cover_image', 'event_image', 'event_files']
        widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'start_date': forms.DateInput(attrs={'class': 'form-control'}),
        'start_time': forms.TimeInput(attrs={'class': 'form-control'}),
        'description': forms.TextInput(attrs={'class': 'form-control'}),
        'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
        'event_image': forms.FileInput(attrs={'class': 'form-control'}),
        'event_files': forms.FileInput(attrs={'class': 'form-control'}),
    }


class addFAQForm(forms.ModelForm):

    class Meta:
        model = faq
        fields = ['question', 'answer']
        widgets = {
        'question': forms.TextInput(attrs={'class': 'form-control'}),
        'answer': forms.TextInput(attrs={'class': 'form-control'}),
    }

class addAnnouncementForm(forms.ModelForm):

    class Meta:
        model = announcement
        fields = ['message', 'order']
        widgets = {
        'message': forms.TextInput(attrs={'class': 'form-control'}),
        'order': forms.NumberInput(attrs={'class': 'form-control'}),
    }

class addDetailForm(forms.ModelForm):

    class Meta:
        model = detail
        fields = ['message', 'announcement']
        widgets = {
        'message': forms.TextInput(attrs={'class': 'form-control'}),
        'announcement': forms.Select(attrs={'class': 'form-control'}),
    }

class addBannerForm(forms.ModelForm):

    class Meta:
        model = banner
        fields = ['message', 'hyperlink']
        widgets = {
        'message': forms.TextInput(attrs={'class': 'form-control'}),
        'hyperlink': forms.TextInput(attrs={'class': 'form-control'}),
    }

class addFAQ(forms.ModelForm):

    class Meta:
        model = faq
        fields = ['question', 'answer']
        widgets = {
        'question': forms.TextInput(attrs={'class': 'form-control'}),
        'answer': forms.TextInput(attrs={'class': 'form-control'}),
    }

class updateEventForm(forms.ModelForm):

    class Meta:
        model = event
        fields = ['title', 'start_date', 'start_time', 'description', 'event_status', 'cover_image', 'event_image', 'event_files']
        widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'start_date': forms.DateInput(attrs={'class': 'form-control'}),
        'start_time': forms.TimeInput(attrs={'class': 'form-control'}),
        'description': forms.TextInput(attrs={'class': 'form-control'}),
        'cover_image': forms.FileInput(attrs={'class': 'form-control'}),
        'event_image': forms.FileInput(attrs={'class': 'form-control'}),
        'event_files': forms.FileInput(attrs={'class': 'form-control'}),
    }


class updateBannerForm(forms.ModelForm):

    class Meta:
        model = banner
        fields = ['message', 'hyperlink']
        widgets = {
        'message': forms.TextInput(attrs={'class': 'form-control'}),
        'hyperlink': forms.TextInput(attrs={'class': 'form-control'}),
    }

class updateAnnouncementForm(forms.ModelForm):

    class Meta:
        model = announcement
        fields = ['message', 'order']
        widgets = {
        'message': forms.TextInput(attrs={'class': 'form-control'}),
        'order': forms.NumberInput(attrs={'class': 'form-control'}),
    }


class updateTimeForm(forms.ModelForm):

    class Meta:
        model = time
        fields = ['title', 'time']
        widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'time': forms.TimeInput(attrs={'class': 'form-control'}),
    }

class updateReadingForm(forms.ModelForm):

    class Meta:
        model = reading
        fields = ['date', 'reading_1', 'reading_1_passage', 'reading_2', 'reading_2_passage', 'gospel', 'gospel_passage']
        widgets = {
        'date': forms.DateInput(attrs={'class': 'form-control'}),
        'reading_1': forms.TextInput(attrs={'class': 'form-control'}),
        'reading_1_passage': forms.Textarea(attrs={'class': 'form-control'}),
        'reading_2': forms.TextInput(attrs={'class': 'form-control'}),
        'reading_2_passage': forms.Textarea(attrs={'class': 'form-control'}),
        'gospel': forms.TextInput(attrs={'class': 'form-control'}),
        'gospel_passage': forms.Textarea(attrs={'class': 'form-control'}),
    }

class updateFAQForm(forms.ModelForm):

    class Meta:
        model = faq
        fields = ['question', 'answer']
        widgets = {
        'question': forms.TextInput(attrs={'class': 'form-control'}),
        'answer': forms.TextInput(attrs={'class': 'form-control'}),
    }

class contactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    cell = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    message = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    def clean(self):
        user_email = self.cleaned_data['email']
        send_mail('test', 'test', 'devalphonsa@gmail.com', [user_email])



