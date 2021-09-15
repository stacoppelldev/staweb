from django.db import models
from django.urls import reverse

EVENT_STATUS = (
    ('Active', 'Active'),
    ('Archived', 'Archived')
)

# Create your models here.
class event(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    # location = models.CharField(max_length=100, null=True, default='Main Hall')
    description = models.CharField(max_length=100, null=True, blank=True)
    cover_image = models.ImageField(upload_to='images', blank=True, null=True)
    event_image = models.ImageField(upload_to='images', blank=True, null=True)
    event_status = models.CharField(choices=EVENT_STATUS, default='Active', max_length=30)
    event_files = models.FileField(upload_to='files', blank=True, null=True)

    def __str__(self):
        return '%s %s %s %s' % (self.title, self.start_date, self.start_time, self.description)

    def get_absolute_url(self):
        return reverse('event-details', args=[self.id])


class time(models.Model):
    title = models.CharField(max_length=100)
    time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.title, self.time)

class reading(models.Model):
    date = models.DateField(null=True)
    reading_1 = models.CharField(max_length=100, null=True)
    reading_1_passage = models.CharField(max_length=1000, null=True)
    reading_2 = models.CharField(max_length=100, null=True)
    reading_2_passage = models.CharField(max_length=1000, null=True)
    gospel = models.CharField(max_length=100, null=True)
    gospel_passage = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return '%s %s' % (self.date, self.reading_1)

class announcement(models.Model):
    message = models.CharField(max_length=100)
    order = models.IntegerField()

    def __str__(self):
        return '%s %s' % (self.message, self.order)

class detail(models.Model):
    message = models.CharField(max_length=100)
    announcement = models.ForeignKey(announcement, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.message, self.announcement)

class faq(models.Model):
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.question, self.answer)

class banner(models.Model):
    message = models.CharField(max_length=200)
    hyperlink = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.message, self.hyperlink)