from django.contrib import admin
from .models import *
from polls.models import *

from other.admin import *
from polls.admin import *

def to_local_date(date):
    return date.strftime('%Y{y}%m{m}%d{d}').format(y='/', m='/', d='')


class DriverCompanyAdmin(admin.ModelAdmin):
    list_display = ('code', 'companyName', 'contactMan', 'lxr1', 'phone1', 'tel1', 'fax', 'lxr2', 'phone2', 'tel2',
                    'mail', 'createMan', 'createTime', 'updateMan', 'updateTime')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset &= self.model.objects.filter(isDelete=False)
        return queryset, use_distinct

    def my_syn(self, request, queryset):
        print('mysyn')

    my_syn.short_description = "同步CTOS数据"

    def my_syn(self, request, queryset):
        print('mysyn')

    my_syn.short_description = "同步CTOS数据"
    actions = ['my_syn']


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


class OutManInfo(admin.TabularInline):
    model = OutManCard
    extra = 1


class OutManAdmin(admin.ModelAdmin):

    def get_valid_date(self, man):
        q = OutManCard.objects.get(manID=man, isDelete=False)
        q = q.order_by('-endTime')[0:1]
        return '%s 至 %s' % (to_local_date(q[0].startTime), to_local_date(q[0].endTime)) \
            if len(q) > 0 else '暂无'

    get_valid_date.short_description = '进港有效期'

    list_display = ('cname', 'sex', 'cardID', 'telPhone', 'inPortNO', 'unitName', 'position', 'lxr', 'unitPhone',
                    'certificateDate', 'get_valid_date', 'illegalCount', 'bakMsg')
    inlines = (OutManInfo,)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset &= self.model.objects.filter(isDelete=False)
        return queryset, use_distinct


class OutCarAdmin(admin.ModelAdmin):

    def get_valid_date(self, car):
        q = OutCarCard.objects.filter(manID=car, isDelete=False)
        q = q.order_by('-endTime')[0:1]
        return '%s 至 %s' % (to_local_date(q[0].startTime), to_local_date(q[0].endTime)) \
            if len(q) > 0 else '暂无'

    def get_tran(self, car):
        q = OutCarTran.objects.filter(manID=car, isDelete=False)
        q = q.order_by('-tranDate')[0:1]
        return '%s 至 %s' % (to_local_date(q[0].startTime), to_local_date(q[0].endTime)) \
            if len(q) > 0 else '暂无'

    get_valid_date.short_description = '进港有效期'
    get_tran.short_description = '培训情况'
    list_display = ('truckNO', 'driverName', 'sex', 'cardID', 'telPhone', 'inPortNO', 'unitName', 'position',
                    'lxr', 'unitPhone', 'inResion', 'firstCardDate', 'get_valid_date', 'get_tran', 'bakMsg',
                    'illegalCount')
    inlines = (OutCarTranInfo, OutCarTranInfo)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset &= self.model.objects.filter(isDelete=False)
        return queryset, use_distinct


class IllegalAdmin(admin.ModelAdmin):

    # def show_image(self, illegal):
    #     q = IllegalImage.objects.all()
    #     return format_html(
    #         '<img src="{}" width="100px"/>',
    #         q.image,
    #     )


    # show_image.short_description = '违章图片'

    list_display = ('illegalDate', 'illegalAttribute', 'illegalCode', 'illegalDesc', 'illegalMan', 'resDept',
                    'resGroup', 'handle', 'resMoney', 'allRes', 'checkMan', 'bakMsg')
    inlines = (IllegalImageInfo, )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset &= self.model.objects.filter(isDelete=False)
        return queryset, use_distinct


class TruckBodyPrjAdmin(admin.ModelAdmin):
    list_display = ('code', 'bodyType', 'weight', 'truckCompany', 'basMes')

    def my_syn(self, request, queryset):
        print('mysyn')

    my_syn.short_description = "同步CTOS数据"

    actions = ['my_syn']


class ViolationCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'penalty', 'content', 'is_penalty')

    def my_syn(self, request, queryset):
        print('mysyn')

    my_syn.short_description = "同步CTOS数据"
    actions = ['my_syn']


class TruckAdmin(admin.ModelAdmin):

    def show_name(self, param):
        return param.driver.driverName

    def show_phone(self, param):
        return param.driver.telPhone

    show_name.short_description = '司机姓名'
    show_phone.short_description = '司机电话'

    list_display = ('realTruck', 'truckNO', 'owner', 'isLock', 'weight', 'pcc', 'company',
                    'basMes', 'truckType', 'fileNO', 'isZX', 'regDate', 'checkDate', 'tranNO',
                    'insuranceNO', 'show_name', 'show_phone', 'createMan', 'createTime', 'updateMan', 'updateTime')

    def my_syn(self, request, queryset):
        print('mysyn')

    my_syn.short_description = "同步CTOS数据"
    actions = ['my_syn']


class TruckIllegalAdmin(admin.ModelAdmin):

    list_display = ('illegalTime', 'code', 'truck', 'driverName', 'status', 'desc',
                    'lockStartTime', 'lockEndTime', 'checkMan')


admin.site.site_header = '安保信息系统'
admin.site.site_title = 'Security'

admin.site.register(DriverCompany, DriverCompanyAdmin)
admin.site.register(Truck, TruckAdmin)
admin.site.register(TruckIIllegal, TruckIllegalAdmin)
admin.site.register(ViolationCode, ViolationCodeAdmin)
admin.site.register(TruckBodyPrj, TruckBodyPrjAdmin)

admin.site.register(Driver, DriverAdmin)
admin.site.register(OutMan, OutManAdmin)
admin.site.register(OutCar, OutCarAdmin)
admin.site.register(Illegal, IllegalAdmin)





#------------------------------------




