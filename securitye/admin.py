from polls.admin import *
from django.contrib import messages
from ctos.models import *
from django.utils.html import format_html
from django.http import HttpResponse
import datetime
import csv


def export_to_csv(model_admin, request, queryset):
    opts = model_admin.model._meta
    response = HttpResponse(content_type='text/csv')
    print('opts.verbose_name', opts)
    response['Content-Disposition'] = u'attachment;filename=csv_file.csv'

    writer = csv.writer(response)
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = '导出CSV'


def to_local_date(date):
    return date.strftime('%Y{y}%m{m}%d{d}').format(y='/', m='/', d='')


class DriverCompanyAdmin(admin.ModelAdmin):
    list_display = ('code', 'companyName', 'contactMan', 'lxr1', 'phone1', 'tel1', 'fax', 'lxr2', 'phone2', 'tel2',
                    'mail', 'createManCname', 'createTime', 'updateManCname', 'updateTime')

    ordering = ('-companyName',)
    search_fields = ('code', 'companyName', 'contactMan', )
    list_filter = ('companyName', 'contactMan')
    list_per_page = 15

    def my_syn(self, request, queryset):
        if len(queryset) != 1:
            self.message_user(request, '请选择"CTOS同步"记录进行数据同步', level=messages.ERROR)
            return
        if queryset[0].code != 'SYN':
            self.message_user(request, '请选择"CTOS同步"记录进行数据同步', level=messages.ERROR)
            return
        list1 = pl_guests.objects.filter(ISTRUCKCOMPANY='Y')
        list2 = DriverCompany.objects.all()
        count = 0
        for tmp in list1:
            update = False
            code = tmp.GUESTCODE
            for tmp2 in list2:
                if code == tmp2.code:
                    update = True
                    tmp2.companyName = tmp.CNAME
                    tmp2.contactMan = tmp.CONTACTMAN
                    tmp2.lxr1 = tmp.CONTACTPERSON
                    tmp2.phone1 = tmp.CONTACTTEL
                    tmp2.tel1 = tmp.CONTACTMOBIL

                    tmp2.fax = tmp.FAX
                    tmp2.lxr2 = tmp.CONTACTMAN2
                    tmp2.phone2 = tmp.TELEPHONE2
                    tmp2.tel2 = tmp.CELLPHONE
                    tmp2.mail = tmp.EMAIL

                    tmp2.createMan = tmp.CREATEMAN
                    tmp2.createTime = tmp.CREATETIME
                    tmp2.updateMan = tmp.LASTUPDATEMAN
                    tmp2.updateTime = tmp.LASTUPDATETIME
                    tmp2.address = tmp.ADDRESS
                    tmp2.createManCname = tmp.CREATEMAN
                    tmp2.updateManCname = tmp.LASTUPDATEMAN
                    tmp2.save()
                    count += 1
                    break
            if update is False:
                q = DriverCompany(code=tmp.GUESTCODE, companyName=tmp.CNAME,
                                 contactMan=tmp.CONTACTMAN, lxr1=tmp.CONTACTPERSON, phone1=tmp.CONTACTTEL,
                                 tel1=tmp.CONTACTMOBIL, fax=tmp.FAX, lxr2=tmp.CONTACTMAN2,
                                 phone2=tmp.TELEPHONE2, tel2=tmp.CELLPHONE, mail=tmp.EMAIL,
                                 address=tmp.ADDRESS, createMan=tmp.CREATEMAN ,
                                 createTime=tmp.CREATETIME, updateMan=tmp.LASTUPDATEMAN,
                                 updateTime=tmp.LASTUPDATETIME)
                q.createManCname = tmp.CREATEMAN
                q.updateManCname = tmp.LASTUPDATEMAN
                q.save()
                count += 1
        list2 = DriverCompany.objects.all()
        d = {'': ''}
        for tmp2 in list2:
            if d.get(tmp2.createManCname) is not None:
                tmp2.createManCname = d[tmp2.createMan]
            else:
                u1 = pl_user.objects.filter(US_LOGID=tmp2.createMan)
                if len(u1) > 0:
                    tmp2.createManCname = u1[0].US_NAME
                    d[tmp2.createMan] = u1[0].US_NAME

            if d.get(tmp2.updateMan) is not None:
                tmp2.updateManCname = d[tmp2.updateMan]
            else:
                u1 = pl_user.objects.filter(US_LOGID=tmp2.updateMan)
                if len(u1) > 0:
                    tmp2.updateManCname = u1[0].US_NAME
                    d[tmp2.updateMan] = u1[0].US_NAME
            tmp2.save()
        self.message_user(request, '已同步%d条数据' % count)

    def delete_queryset(self, request, queryset):
        for tmp in queryset:
            if tmp.code == 'SYN':
                self.message_user(request, '不能删除用于"CTOS同步"的记录', level=messages.ERROR)
                return
        super().delete_queryset(request, queryset)

    my_syn.short_description = "同步CTOS数据"
    actions = [export_to_csv, my_syn]


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
    actions = [export_to_csv]


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
    actions = [export_to_csv]


class OutCarAdmin(admin.ModelAdmin):

    def get_valid_date(self, car):
        q = OutCarCard.objects.filter(carID=car)
        q = q.order_by('-endTime')[0:1]
        return '%s 至 %s' % (to_local_date(q[0].startTime), to_local_date(q[0].endTime)) \
            if len(q) > 0 else '暂无'

    def get_tran(self, car):
        q = OutCarTran.objects.filter(driver=car)
        q = q.order_by('-tranDate')[0:1]
        return '%s 至 %s' % (to_local_date(q[0].startTime), to_local_date(q[0].endTime)) \
            if len(q) > 0 else '暂无'


    get_valid_date.short_description = '进港有效期'
    get_tran.short_description = '培训情况'
    list_display = ('truckNO', 'driverName', 'sex', 'cardID', 'telPhone', 'inPortNO', 'unitName', 'position',
                    'lxr', 'unitPhone', 'inResion', 'firstCardDate', 'get_valid_date', 'get_tran', 'bakMsg',
                    'illegalCount')
    inlines = (OutCarTranInfo, OutCarTranInfo)

    actions = [export_to_csv]


class IllegalAdmin(admin.ModelAdmin):

    def image_data(self, param):
        list1 = IllegalImage.objects.filter(illegal=param)
        html = u'<ol>'
        for tmp in list1:
            html += u'<li><a href="{}" target="_blank"><img src="{}" width="100px" /></a></li>'.format(tmp.image.url, tmp.image.url)
        html += u'</ol>'
        print(html)

        return mark_safe(html)

    image_data.short_description = '图片'

    list_display = ('illegalDate', 'illegalAttribute', 'illegalCode', 'illegalDesc', 'illegalMan', 'resDept',
                    'resGroup', 'handle', 'resMoney', 'allRes', 'checkMan', 'bakMsg', 'image_data')
    readonly_fields = ('image_data',)
    inlines = (IllegalImageInfo, )
    actions = [export_to_csv]


class TruckBodyPrjAdmin(admin.ModelAdmin):

    # def showCompany(self, param):
    #     list = pl_guests.objects.filter(GUESTCODE=param.truckCompany)
    #     return list[0].CNAME if len(list) > 0 else ''
    #
    # showCompany.short_description = '所属外拖公司'

    list_display = ('code', 'bodyType', 'weight', 'cnameCompany', 'basMes')
    search_fields = ('code', 'bodyType', 'cnameCompany', 'weight', 'basMes', )
    list_filter = ('bodyType', 'cnameCompany')

    def my_syn(self, request, queryset):
        if len(queryset) != 1:
            self.message_user(request, '请选择"CTOS同步"记录进行数据同步', level=messages.ERROR)
            return
        if queryset[0].code != 'SYN':
            self.message_user(request, '请选择"CTOS同步"记录进行数据同步', level=messages.ERROR)
            return
        list1 = er_truckbody_prj.objects.all()
        list2 = TruckBodyPrj.objects.all()
        count = 0
        for tmp in list1:
            update = False
            code = tmp.TRUCKBODYCODE_PRJ
            for tmp2 in list2:
                if code == tmp2.code:
                    update = True
                    tmp2.bodyType = tmp.TRUCKBODYTYPECODE_PRJ
                    tmp2.weight = tmp.WEIGHT_PRJ
                    tmp2.truckCompany = tmp.TRUCKCOMPANY_PRJ
                    tmp2.basMes = tmp.MEMO_PRJ
                    tmp2.save()
                    count += 1
                    break
            if update is False:
                q = TruckBodyPrj(code=tmp.TRUCKBODYCODE_PRJ, bodyType=tmp.TRUCKBODYTYPECODE_PRJ, weight=tmp.WEIGHT_PRJ,
                                 truckCompany=tmp.TRUCKCOMPANY_PRJ, basMes=tmp.MEMO_PRJ)
                q.save()
                count += 1
        list2 = TruckBodyPrj.objects.all()
        for tmp2 in list2:
            guest = pl_guests.objects.filter(GUESTCODE=tmp2.truckCompany)
            if len(guest) > 0:
                tmp2.cnameCompany = guest[0].CNAME
                tmp2.save()
        self.message_user(request, '已同步%d条数据' % count)

    my_syn.short_description = "同步CTOS数据"

    actions = [export_to_csv, my_syn]
    ordering = ('-cnameCompany',)
    list_per_page = 15

    def delete_queryset(self, request, queryset):
        for tmp in queryset:
            if tmp.code == 'SYN':
                self.message_user(request, '不能删除用于"CTOS同步"的记录', level=messages.ERROR)
                return
        super().delete_queryset(request, queryset)


class ViolationCodeAdmin(admin.ModelAdmin):

    def myContent(self, param):
        if param.code == 'SYN':
            return format_html('<b style="color: green;">{}</b>', param.content)
        else:
            return param.content

    myContent.short_description = '违章内容'

    list_display = ('code', 'penalty', 'myContent', 'is_penalty')
    ordering = ('vid',)

    def my_syn(self, request, queryset):
        if len(queryset) != 1:
            self.message_user(request, '请选择"CTOS同步"记录进行数据同步', level=messages.ERROR)
            return
        if queryset[0].code != 'SYN':
            self.message_user(request, '请选择"CTOS同步"记录进行数据同步', level=messages.ERROR)
            return
        list1 = er_violationcode.objects.all()
        list2 = ViolationCode.objects.all()
        count = 0
        for tmp in list1:
            update = False
            vid = tmp.VIOLATIONCODEID
            for tmp2 in list2:
                if vid == tmp2.vid:
                    update = True
                    tmp2.code = tmp.VIOLATIONCODE
                    tmp2.penalty = tmp.PENALTY
                    tmp2.content = tmp.CONTENT
                    tmp2.is_penalty = True if tmp.ISPENALTY == 'Y' else False
                    tmp2.save()
                    count += 1
                    break
            if update is False:
                q = ViolationCode(vid=tmp.VIOLATIONCODEID, code=tmp.VIOLATIONCODE, penalty=tmp.PENALTY,
                                  content=tmp.CONTENT)
                q.is_penalty = True if tmp.ISPENALTY == 'Y' else False
                q.save()
                count += 1
        self.message_user(request, '已同步%d条数据' % count)

    my_syn.short_description = "同步CTOS数据"
    actions = [export_to_csv, my_syn]

    def delete_queryset(self, request, queryset):
        for tmp in queryset:
            if tmp.code == 'SYN':
                self.message_user(request, '不能删除用于"CTOS同步"的记录', level=messages.ERROR)
                return
        super().delete_queryset(request, queryset)


class TruckAdmin(admin.ModelAdmin):

    def show_name(self, param):
        return param.driver.driverName if param is not None and param.driver is not None else ''

    def show_phone(self, param):
        return param.driver.telPhone if param is not None and param.driver is not None else ''

    show_name.short_description = '司机姓名'
    show_phone.short_description = '司机电话'

    list_display = ('realTruck', 'truckNO', 'owner', 'isPCC', 'isLock', 'weight', 'pcc', 'company',
                    'truckType', 'fileNO', 'isZX', 'regDate', 'checkDate', 'tranNO',
                    'insuranceNO', 'show_name', 'show_phone', 'createManCName', 'createTime', 'updateManCName',
                    'updateTime', 'basMes', )

    list_per_page = 15

    ordering = ('realTruck',)
    search_fields = ('realTruck', 'truckNO', 'company', 'regDate', 'owner', 'pcc', 'insuranceNO', 'fileNO', 'tranNO')
    list_filter = ('company', 'isLock', 'isZX', 'isPCC')

    def my_syn(self, request, queryset):
        if len(queryset) != 1:
            self.message_user(request, '请选择"CTOS同步"记录进行数据同步', level=messages.ERROR)
            return

        if queryset[0].realTruck != 'SYN':
            self.message_user(request, '请选择"CTOS同步"记录进行数据同步', level=messages.ERROR)
            return
        list1 = er_truck.objects.filter(ISPCC='Y')
        list2 = Truck.objects.all()
        count = 0
        for tmp in list1:
            update = False
            truckid = tmp.truckid
            for tmp2 in list2:
                if truckid == tmp2.truckID:
                    update = True
                    tmp2.realTruck = tmp.REALTRUCKN
                    tmp2.truckNO = tmp.TRAILNO
                    tmp2.owner = tmp.TRUCKOWNER
                    tmp2.isLock = True if tmp.ISLOCK == 'Y' else False
                    tmp2.weight = tmp.truckheadweight
                    tmp2.isPCC = True if tmp.ISPCC else False

                    tmp2.pcc = tmp.PCCNO
                    tmp2.companyCode = tmp.TRUCKCOMPANYCODE
                    tmp2.basMes = tmp.REMARK
                    tmp2.createMan = tmp.CREATER
                    tmp2.createTime = tmp.CREATETIME
                    tmp2.updateMan = tmp.LASTUPDATEMAN
                    tmp2.updateTime = tmp.LASTUPDATETIME

                    tmp2.save()
                    count += 1
                    break
            if update is False:
                q = Truck(truckID=tmp.truckid, realTruck=tmp.REALTRUCKNO, truckNO=tmp.TRAILNO, owner=tmp.TRUCKOWNER,
                          isLock=True if tmp.ISLOCK == 'Y' else False, weight=tmp.truckheadweight, pcc=tmp.PCCNO,
                          companyCode=tmp.TRUCKCOMPANYCODE, basMes=tmp.REMARK, createMan=tmp.CREATER,
                          createTime=tmp.CREATETIME, updateMan=tmp.LASTUPDATEMAN, updateTime=tmp.LASTUPDATETIME,
                          isPCC=True if tmp.ISPCC else False)

                q.createManCName = tmp.CREATER
                q.updateManCName = tmp.LASTUPDATEMAN
                q.save()
                count += 1
        list2 = Truck.objects.all()
        d = {'': ''}
        pguest = {'': ''}
        for tmp2 in list2:
            if d.get(tmp2.createMan) is not None:
                tmp2.createManCName = d[tmp2.createMan]
            else:
                u1 = pl_user.objects.filter(US_LOGID=tmp2.createMan)
                if len(u1) > 0:
                    tmp2.createManCName = u1[0].US_NAME
                    d[tmp2.createMan] = u1[0].US_NAME

            if d.get(tmp2.updateMan) is not None:
                tmp2.updateManCName = d[tmp2.updateMan]
            else:
                u1 = pl_user.objects.filter(US_LOGID=tmp2.updateMan)
                if len(u1) > 0:
                    tmp2.updateManCName = u1[0].US_NAME
                    d[tmp2.updateMan] = u1[0].US_NAME

            if pguest.get(tmp2.companyCode) is not None:
                tmp2.company = pguest[tmp2.companyCode]
            else:
                pu = pl_guests.objects.filter(GUESTCODE=tmp2.companyCode)
                if len(pu) > 0:
                    tmp2.company = pu[0].CNAME
                    pguest[tmp2.companyCode] = pu[0].CNAME

            tmp2.save()
        self.message_user(request, '已同步%d条数据' % count)

    def delete_queryset(self, request, queryset):
        for tmp in queryset:
            if tmp.realTruck == 'SYN':
                self.message_user(request, '不能删除用于"CTOS同步"的记录', level=messages.ERROR)
                return
        super().delete_queryset(request, queryset)

    my_syn.short_description = "同步CTOS数据"
    actions = [export_to_csv, my_syn]


class TruckIllegalAdmin(admin.ModelAdmin):

    list_display = ('illegalTime', 'code', 'truck', 'driverName', 'status', 'desc',
                    'lockStartTime', 'lockEndTime', 'checkMan')

    autocomplete_fields = ['truck']
    actions = [export_to_csv]


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




