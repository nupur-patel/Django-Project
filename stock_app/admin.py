from django.contrib import admin
from stock_app.models import Security,Exchange,DividendHistory,DividendAnnouncement
# Register your models here.

admin.site.register(Security)
admin.site.register(Exchange)
admin.site.register(DividendAnnouncement)
admin.site.register(DividendHistory)