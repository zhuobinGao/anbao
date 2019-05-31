from django.contrib import admin
from .models import *
# Register your models here.


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('driverType', 'desc')


class DriverCompanyAdmin(admin.ModelAdmin):
    list_display = ('companyName', 'isDelete')


class DriverAdmin(admin.ModelAdmin):
    list_display = ('driverName', 'driverType', 'telPhone', 'idCardNO', 'truckCompanyCode', 'truckNO', 'firstCardDate')










class MySite(admin.AdminSite):
    site_title = '安保管理系统'
    site_header = '管理系统'
    # site_url = '/welcome'


mysite = MySite()

admin.site.register(CarModel, CarModelAdmin)
admin.site.register(DriverCompany, DriverCompanyAdmin)
admin.site.register(Driver, DriverAdmin)

admin.site.register(OutMan)
admin.site.register(OutCar)
admin.site.register(Illegal)
admin.site.register(IllegalImage)
admin.site.register(DriverTran)
admin.site.register(OutCarTran)
admin.site.register(DriverTest)
admin.site.register(DriverLearnCard)
admin.site.register(DriverTempInCard)

admin.site.register(DriverLongInCard)
admin.site.register(OutCarCard)
admin.site.register(OutManCard)
admin.site.register(ResDept)
admin.site.register(ResGroup)
admin.site.register(CheckMan)