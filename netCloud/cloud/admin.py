from django.contrib import admin
from .models import User, File, FileOperateRecord, SubRecord
# Register your models here.
admin.site.register([User, File, FileOperateRecord, SubRecord])
