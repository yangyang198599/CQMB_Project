from django.contrib import admin

from cqen.models import Account
# Register your models here.
admin.site.register(Account)
class cqenAdmin(admin.ModelAdmin):
    list_display = ('a_username','a_passwd','a_company')

