from .models import event, time, reading, announcement, faq, banner
from django import forms
from django.forms import ModelForm
from django.core.mail import send_mail
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Column, Field, Submit
from captcha.fields import CaptchaField

# FORMS FOR ADDING DIFFERENT TYPES

class addEventForm(forms.ModelForm):
    class Meta:
        model = event
        fields = ['title', 'start_date', 'start_time', 'end_date', 'end_time',
            'description', 'cover_image', 'event_image', 'event_files']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control'}),
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
        fields = ['message', 'detail', 'announcement_files', 'order']

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

# FORMS FOR EDITING DIFFERENT TYPES

class updateEventForm(forms.ModelForm):
    class Meta:
        model = event
        fields = ['title', 'start_date', 'start_time', 'end_date', 'end_time',
            'description', 'event_status', 'cover_image', 'event_image', 'event_files']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control'}),
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
        fields = ['message', 'detail', 'announcement_files', 'order']

class updateTimeForm(forms.ModelForm):
    class Meta:
        model = time
        fields = ['title', 'time']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }

class updateReadingForm(forms.ModelForm):
    class Meta:
        model = reading
        fields = ['date', 'reading_1', 'reading_1_passage', 'reading_2',
            'reading_2_passage', 'gospel', 'gospel_passage']
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

# ADDITIONAL FORMS (HAS NO MODEL, USED ONLY TO SEND EMAIL)

class contactForm(forms.Form):
    name    = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email   = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    cell    = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Column(
                    Field('name', css_class='form-control'),
                    css_class='col-md-6 form-group',
                ),
                Column(
                    Field('email', css_class='form-control'),
                    css_class='col-md-6 form-group mt-3 mt-md-0',
                ),
                css_class='row'
            ),
            Div('subject', css_class='form-group mt-3'),
            Div('message', css_class='form-group mt-3')
        )

    def clean(self):
        user_email = self.cleaned_data['email']
        send_mail('test', 'test', 'devalphonsa@gmail.com', [user_email])

class reserveAuditoriumForm(forms.Form):
    name    = forms.CharField(widget=forms.TextInput())
    email   = forms.CharField(widget=forms.TextInput(attrs={'type': 'email'}))
    phone   = forms.CharField(widget=forms.TextInput())
    date    = forms.CharField(widget=forms.DateInput(attrs={'type': 'date'}))
    time    = forms.CharField(widget=forms.TimeInput(attrs={'type': 'time'}))
    people  = forms.IntegerField()
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Column(
                    Field('name', id='name',
                        css_class='form-control',
                        data_rule='minlen:4',
                        data_msg='Please enter at least 4 chars',
                        placeholder='Your Name'
                    ),
                    Div(css_class='validate'),
                    css_class='col-md-6',
                ),
                Column(
                    Field('email', id='email',
                        css_class='form-control',
                        data_rule='email',
                        data_msg='Please enter a valid email',
                        placeholder='Your Email'
                    ),
                    Div(css_class='validate'),
                    css_class='col-md-6',
                ),
                Column(
                    Field('phone', id='phone',
                        css_class='form-control',
                        data_rule='minlen:10',
                        data_msg='Please enter 10 digits',
                        placeholder='Your Phone'
                    ),
                    Div(css_class='validate'),
                    css_class='col-md-6',
                ),
                Column(
                    Field('people', id='people',
                        css_class='form-control',
                        data_rule='minlen:1',
                        data_msg='Please enter at least 1 chars',
                        placeholder='# of people'
                    ),
                    Div(css_class='validate'),
                    css_class='col-md-6',
                ),
                Column(
                    Field('date', id='date',
                        css_class='form-control',
                        data_rule='minlen:4',
                        data_msg='Please enter at least 4 chars',
                        placeholder='Date'
                    ),
                    Div(css_class='validate'),
                    css_class='col-md-6',
                ),
                Column(
                    Field('time', id='time',
                        css_class='form-control',
                        data_rule='minlen:4',
                        data_msg='Please enter at least 4 chars',
                        placeholder='Time'
                    ),
                    Div(css_class='validate'),
                    css_class='col-md-6',
                ),
                css_class='row gy-4'
            ),
            Div(css_class='mb-5'),
            Div(
                Submit('request-reservation', 'Request Reservation'),
                css_class='text-center'
            ),
        )

    def clean(self):
        user_email = self.cleaned_data['email']
        send_mail('test', 'test', 'devalphonsa@gmail.com', [user_email])
