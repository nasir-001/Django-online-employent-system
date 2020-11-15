from django.contrib import admin
from .models import *

# Register your models here.
admin.site.site_header = 'Online Employment System'
admin.site.register(Category)
admin.site.register(Applicant)
admin.site.register(Job)
admin.site.register(BookmarkJob)


