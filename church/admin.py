from django.contrib import admin
from . import models


myModels = [models.event, models.time, models.reading, models.announcement, models.faq, models.banner, models.page]
admin.site.register(myModels)
