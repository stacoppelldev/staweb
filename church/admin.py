from django.contrib import admin
from . import models

churchModels = [
    models.event,
    models.time,
    models.reading,
    models.announcement,
    models.faq,
    models.banner,
    models.page,
    models.PhotoAlbum,
    models.Photo
]
admin.site.register(churchModels)
