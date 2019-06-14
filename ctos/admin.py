from django.contrib import admin
from .models import *


class er_truckAdmin(admin.ModelAdmin):
    actions = None
    list_per_page = 10
    list_display = ('truckid', 'truckheadweight', 'REALTRUCKNO', 'PCCNO', 'TRUCKOWNER', 'TRAILNO', 'ISLOCK', 'REMARK')


class pl_guestsAdmin(admin.ModelAdmin):
    actions = None
    list_per_page = 10
    list_display = ('GUESTCODE', 'CNAME', 'CONTACTMAN', 'ADDRESS', 'CONTACTPERSON', 'CONTACTTEL', 'CONTACTMOBIL')

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset &= self.model.objects.filter(ISTRUCKCOMPANY='Y')
        return queryset, use_distinct


class er_truckbody_prjAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('TRUCKBODYCODE_PRJ', 'TRUCKBODYTYPECODE_PRJ', 'WEIGHT_PRJ', 'TRUCKCOMPANY_PRJ', 'MEMO_PRJ')

class er_violationcodeAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('VIOLATIONCODEID', 'VIOLATIONCODE', 'PENALTY', 'CONTENT', 'ISPENALTY', 'LASTUPDATEMAN',
                    'LASTUPDATETIME')


admin.site.register(er_truck, er_truckAdmin)
admin.site.register(pl_guests, pl_guestsAdmin)
admin.site.register(er_truckbody_prj, er_truckbody_prjAdmin)
admin.site.register(er_violationcode, er_violationcodeAdmin)

