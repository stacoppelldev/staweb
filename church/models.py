from django.db import models
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse
from ckeditor.fields import RichTextField
import cloudinary
from cloudinary.models import CloudinaryField
from staweb.util import unique_slug_generator

EVENT_STATUS = (
    ('Active', 'Active'),
    ('Archived', 'Archived')
)

class event(models.Model):
    title        = models.CharField(max_length=100)
    start_date   = models.DateField(auto_now_add=False, auto_now=False, null=True)
    start_time   = models.TimeField(blank=True, null=True)
    end_date     = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    end_time     = models.TimeField(blank=True, null=True)
    description  = models.CharField(max_length=100, null=True)
    cover_image  = CloudinaryField(folder='events', blank=True, null=True)
    event_image  = CloudinaryField(folder='events', blank=True, null=True)
    event_status = models.CharField(choices=EVENT_STATUS, default='Active', max_length=30)
    event_files  = CloudinaryField(folder='events', blank=True, null=True)

    def __str__(self):
        return '%s %s: %s' % (self.start_date, self.start_time, self.title)

class time(models.Model):
    title = models.CharField(max_length=100)
    time  = models.TimeField(blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.title, self.time)

class reading(models.Model):
    date              = models.DateField(null=True)
    reading_1         = models.CharField(max_length=100, null=True)
    reading_1_passage = models.CharField(max_length=1000, null=True)
    reading_2         = models.CharField(max_length=100, null=True)
    reading_2_passage = models.CharField(max_length=1000, null=True)
    gospel            = models.CharField(max_length=100, null=True)
    gospel_passage    = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return '%s %s' % (self.date, self.reading_1)

class announcement(models.Model):
    message            = models.CharField(null=True, max_length=100)
    detail             = RichTextField(null=True, blank=True, max_length=1000)
    announcement_files = CloudinaryField(null=True, blank=True, folder='announcements')
    order              = models.IntegerField()

    def __str__(self):
        return '%s: %s' % (self.order, self.message)

@receiver(pre_delete, sender=announcement)
def announcement_delete(sender, instance, **kwargs):
    if not instance.announcement_files == None:
        cloudinary.uploader.destroy(instance.announcement_files.public_id)

# @receiver(pre_save, sender=announcement)
# def announcement_update(sender, instance, **kwargs):
#     if not kwargs.get('created') and not instance.announcement_files == None:
#         cloudinary.uploader.destroy(instance.announcement_files.public_id)

class faq(models.Model):
    question = models.CharField(max_length=200)
    answer   = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.question, self.answer)

class banner(models.Model):
    message   = models.CharField(max_length=200)
    hyperlink = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.message, self.hyperlink)

class page(models.Model):
    title              = models.CharField(max_length=200)
    subtitle           = models.CharField(max_length=250, blank=True, null=True)
    call_to_action     = models.CharField(max_length=250, blank=True, null=True)
    call_to_action_url = models.CharField(max_length=250, blank=True, null=True)
    cover_image        = models.ImageField(upload_to='images', blank=True, null=True)
    section_1_title    = models.CharField(max_length=200, null=True, blank=True)
    section_1_body     = RichTextField(null=True, blank=True, max_length=5000)
    image2             = models.ImageField(upload_to='images', blank=True, null=True)
    section_2_title    = models.CharField(max_length=200, null=True, blank=True)
    section_2_body     = RichTextField(null=True, blank=True, max_length=5000)

    def __str__(self):
        return '%s' % (self.title)

##### MEDIA > ALBUMS & ALBUM PHOTOS

def get_album_photo_upload_to(instance):
    return 'media/photos/%s/%s' % (str(instance.album.start_date.year), instance.album.slug)

class PhotoAlbum(models.Model):
    start_date = models.DateField()
    end_date   = models.DateField(blank=True, null=True)
    title      = models.CharField()
    slug       = models.SlugField(max_length=50, blank=True, editable=False)

    class Meta:
        verbose_name = 'Photo Album'
        verbose_name_plural = 'Photo Albums'
        ordering = ['-start_date']

    def __str__(self):
        return '%s: %s' % (self.start_date, self.title)

@receiver(pre_save, sender=PhotoAlbum)
def PhotoAlbumPreSaveReceiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

    cloudinary.api.create_folder('media/photos/' + str(instance.start_date.year) + '/' + instance.slug)

@receiver(pre_delete, sender=PhotoAlbum)
def PhotoAlbumPreDeleteReceiver(sender, instance, *args, **kwargs):
    cloudinary.api.delete_folder('media/photos/' + str(instance.start_date.year) + '/' + instance.slug)

class Photo(models.Model):
    image = CloudinaryField('image', folder=get_album_photo_upload_to)
    album = models.ForeignKey(PhotoAlbum, on_delete=models.CASCADE, related_name='photos')

    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return 'Photo <%s>' % (public_id)

@receiver(pre_save, sender=Photo)
def PhotoPreSaveReceiver(sender, instance, *args, **kwargs):
    cloudinary.uploader.upload('media/photos/' + str(instance.start_date.year) + '/' + instance.slug)
