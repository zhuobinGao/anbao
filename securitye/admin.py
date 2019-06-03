from django.contrib import admin
from .models import *


import locale
# Register your models here.


def to_local_date(date):
    return date.strftime('%Y{y}%m{m}%d{d}').format(y='/', m='/', d='')


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('driverType', 'desc')


class DriverCompanyAdmin(admin.ModelAdmin):
    list_display = ('companyName', 'isDelete')


class DriverJobCardInfo(admin.TabularInline):
    model = DriverJobCard
    extra = 1


class DriverTranInfo(admin.TabularInline):
    model = DriverTran
    extra = 1


class DriverTestInfo(admin.TabularInline):
    model = DriverTest
    extra = 1


class DriverLearnCardInfo(admin.TabularInline):
    model = DriverLearnCard
    extra = 1


class DriverTempInCardInfo(admin.TabularInline):
    model = DriverTempInCard
    extra = 1


class DriverLongInCardInfo(admin.TabularInline):
    model = DriverLongInCard
    extra = 1


class DriverJobCardAdmin(admin.ModelAdmin):
    list_display = ('driver', 'startTime', 'endTime', 'isOn')


class DriverAdmin(admin.ModelAdmin):

    def get_driver_job_card(self, driver):
        q = DriverJobCard.objects.filter(driver=driver, isDelete=False)
        q = q.order_by('-endTime')[0:1]
        return '%s 至 %s' % (to_local_date(q[0].startTime), to_local_date(q[0].endTime)) \
            if len(q) > 0 else '暂无'

    def get_driver_tran(self, driver):
        q = DriverTran.objects.filter(driver=driver, isDelete=False)
        q = q.order_by('-tranDate')[0:1]
        return q[0].status if len(q) > 0 else '暂无'

    def get_driver_test(self, driver):
        q = DriverTest.objects.filter(driver=driver, isDelete=False)
        q = q.order_by('-testDate')[0:1]
        return q[0].testScore if len(q) > 0 else '暂无'

    def get_driver_learn_card(self, driver):
        q = DriverLearnCard.objects.filter(driver=driver, isDelete=False)
        q = q.order_by('-endTime')[0:1]
        return '%s 至 %s' % (to_local_date(q[0].startTime), to_local_date(q[0].endTime)) \
            if len(q) > 0 else '暂无'

    def get_driver_temp_card(self, driver):
        q = DriverTempInCard.objects.filter(driver=driver, isDelete=False)
        q = q.order_by('-endTime')[0:1]
        return '%s 至 %s' % (to_local_date(q[0].startTime), to_local_date(q[0].endTime)) \
            if len(q) > 0 else '暂无'

    def get_driver_long_card(self, driver):
        q = DriverLongInCard.objects.filter(driver=driver, isDelete=False)
        q = q.order_by('-endTime')[0:1]
        return '%s 至 %s' % (to_local_date(q[0].startTime), to_local_date(q[0].endTime)) \
            if len(q) > 0 else '暂无'

    get_driver_job_card.short_description = '从业资格证'
    get_driver_tran.short_description = '培训情况'
    get_driver_test.short_description = '考试成绩'
    get_driver_learn_card.short_description = '学习证'
    get_driver_temp_card.short_description = '临时进港证'
    get_driver_long_card.short_description = '长期进港证'

    list_display = ('driverName', 'driverType', 'telPhone', 'idCardNO', 'truckCompanyCode', 'truckNO',
                    'get_driver_job_card', 'get_driver_tran', 'get_driver_test', 'get_driver_learn_card',
                    'get_driver_temp_card', 'get_driver_long_card', 'firstCardDate', 'illegalCount')
    inlines = [DriverJobCardInfo, DriverTestInfo, DriverLearnCardInfo,
               DriverTempInCardInfo, DriverLongInCardInfo, DriverTranInfo]
    list_filter = ['driverName', 'truckCompanyCode', 'illegalCount']
    search_fields = ['driverName', 'truckCompanyCode__companyName', 'illegalCount']
    list_per_page = 50
    date_hierarchy = 'firstCardDate'  # 详细时间分层筛选

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset &= self.model.objects.filter(isDelete=False)
        return queryset, use_distinct

    def save_model(self, request, obj, form, change):
        obj.recordMan = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        obj.cancelMan = request.user
        obj.cancelTime = datetime.datetime.now()
        super().delete_model(request, obj)


# class MySite(admin.AdminSite):
#     site_title = 'Security'
#     site_header = '安保管理系统'

admin.site.site_header = '安保信息系统'
admin.site.site_title = 'Security'

# admin.site = MySite(name='management')
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(DriverCompany, DriverCompanyAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(DriverJobCard)

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