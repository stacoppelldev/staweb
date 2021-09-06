from django.contrib import admin
from . import models


myModels = [models.event, models.time, models.reading, models.announcement, models.detail, models.faq, models.banner]
admin.site.register(myModels)
