from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
# Register your models here.


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


class DriverJobCardAdmin(admin.ModelAdmin):
    list_display = ('driver', 'startTime', 'endTime')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset &= self.model.objects.filter(isDelete=False)
        return queryset, use_distinct


class DriverTranAdmin(admin.ModelAdmin):

    list_display = ('driver', 'status', 'tranDate')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset &= self.model.objects.filter(isDelete=False)
        return queryset, use_distinct


class DriverTestAdmin(admin.ModelAdmin):
    list_display = ('driver', 'testScore', 'testDate')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset &= self.model.objects.filter(isDelete=False)
        return queryset, use_distinct


class DriverLearnCardAdmin(admin.ModelAdmin):
    list_display = ('driver', 'startTime', 'endTime')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset &= self.model.objects.filter(isDelete=False)
        return queryset, use_distinct


class DriverTempInCardAdmin(admin.ModelAdmin):
    list_display = ('driver', 'startTime', 'endTime')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset &= self.model.objects.filter(isDelete=False)
        return queryset, use_distinct


class DriverLongInCardAdmin(admin.ModelAdmin):
    list_display = ('driver', 'startTime', 'endTime')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset &= self.model.objects.filter(isDelete=False)
        return queryset, use_distinct


class OutManCardAdmin(admin.ModelAdmin):
    list_display = ('manID', 'startTime', 'endTime')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset &= self.model.objects.filter(isDelete=False)
        return queryset, use_distinct


class OutCarTranInfo(admin.TabularInline):
    model = OutCarTran
    extra = 1


class OutCarCardInfo(admin.TabularInline):
    model = OutCarCard
    extra = 1


class OutCarTranAdmin(admin.ModelAdmin):

    list_display = ('driver', 'status', 'tranDate')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset &= self.model.objects.filter(isDelete=False)
        return queryset, use_distinct


class OutCarCardAdmin(admin.ModelAdmin):
    list_display = ('carID', 'startTime', 'endTime')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset &= self.model.objects.filter(isDelete=False)
        return queryset, use_distinct


class IllegalImageInfo(admin.TabularInline):
    model = IllegalImage
    extra = 2


class IllegalImageAdmin(admin.ModelAdmin):

    def image_data(self, param):
        print('url', param.image.url)
        return mark_safe(u'<img src="{}" width="100px" />'.format(param.image.url))

    image_data.short_description = u'图片'
    list_display = ('illegal', 'image', 'image_data')
    readonly_fields = ('image_data',)


admin.site.register(DriverJobCard, DriverJobCardAdmin)
admin.site.register(DriverTest, DriverTestAdmin)
admin.site.register(DriverLearnCard, DriverLearnCardAdmin)
admin.site.register(DriverTempInCard, DriverTempInCardAdmin)
admin.site.register(DriverLongInCard, DriverLongInCardAdmin)
admin.site.register(DriverTran, DriverTranAdmin)
admin.site.register(OutManCard, OutManCardAdmin)
admin.site.register(OutCarTran, OutCarTranAdmin)
admin.site.register(OutCarCard, OutCarCardAdmin)
admin.site.register(IllegalImage, IllegalImageAdmin)