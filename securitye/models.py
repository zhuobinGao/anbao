from django.db import models
from other.models import *

verbose_name = '安保系统'


class TruckBodyPrj(models.Model):
    code = models.CharField(max_length=30, primary_key=True, verbose_name='拖架号')
    bodyType = models.CharField(max_length=20, null=True, blank=True, verbose_name='拖架类型')
    weight = models.FloatField(null=True, blank=True, verbose_name='拖架重量(kg)')
    truckCompany = models.CharField(max_length=30, verbose_name='所属外拖公司')
    basMes = models.CharField(max_length=50, null=True, blank=True, verbose_name='备注')
    cnameCompany = models.CharField(max_length=30, verbose_name='所属外拖公司',null=True, blank=True, default=None)

    def __str__(self):
        return '拖架管理:%s' % self.code

    class Meta:
        verbose_name = '5.0 托架管理'


class ViolationCode(models.Model):
    vid = models.BigIntegerField(unique=True, verbose_name='主键')
    code = models.CharField(max_length=42, null=True, blank=True, verbose_name='违章代码')
    penalty = models.FloatField(null=True, blank=True, verbose_name='罚分数值')
    content = models.CharField(max_length=100, null=True, blank=True, verbose_name='违章内容')
    is_penalty = models.BooleanField(default=False, blank=True, verbose_name='是否统计罚分')

    def __str__(self):
        return '违章代码管理:%s' % self.code

    class Meta:
        verbose_name = '4.0 违章代码'


class DriverCompany(models.Model):
    code = models.CharField(max_length=10, default=None, verbose_name='车队代码')
    companyName = models.CharField(max_length=30, verbose_name='车队名称')
    contactMan = models.CharField(max_length=40, verbose_name='法人', null=True, blank=True, default=None)
    lxr1 = models.CharField(max_length=40, verbose_name='联系人1', null=True, blank=True, default=None)
    phone1 = models.CharField(max_length=40, verbose_name='电话1', null=True, blank=True, default=None)
    tel1 = models.CharField(max_length=40, verbose_name='手机1', null=True, blank=True, default=None)
    fax = models.CharField(max_length=40, verbose_name='传真', null=True, blank=True, default=None)
    lxr2 = models.CharField(max_length=40, verbose_name='联系人2', null=True, blank=True, default=None)
    phone2 = models.CharField(max_length=40, verbose_name='电话2', null=True, blank=True, default=None)
    tel2 = models.CharField(max_length=40, verbose_name='手机2', null=True, blank=True, default=None)
    mail = models.CharField(max_length=40, verbose_name='邮箱', null=True, blank=True, default=None)
    address = models.CharField(max_length=240, verbose_name='注册地址', null=True, blank=True, default=None)
    createMan = models.CharField(max_length=40, verbose_name='创建人', null=True, blank=True, default=None)
    createTime = models.DateTimeField(verbose_name='创建时间', null=True, blank=True, default=None)
    updateMan = models.CharField(max_length=40, verbose_name='更新人', null=True, blank=True, default=None)
    updateTime = models.DateTimeField(verbose_name='更新时间', null=True, blank=True, default=None)
    isDelete = models.BooleanField(default=False, verbose_name='是否有效', editable=False)
    createManCname = models.CharField(max_length=40, verbose_name='创建人', null=True, blank=True, default=None)
    updateManCname = models.CharField(max_length=40, verbose_name='更新人', null=True, blank=True, default=None)

    def __str__(self):
        return '拖车公司:%s' % self.companyName

    class Meta:
        verbose_name = '1.0 拖车公司'


class Driver(models.Model):
    driverName = models.CharField(max_length=15, blank=False, verbose_name='司机姓名')
    driverType = models.ForeignKey(CarModel, on_delete=models.DO_NOTHING, verbose_name='准驾类型', null=True, blank=True)
    telPhone = models.CharField(max_length=20, verbose_name='司机电话', null=True, blank=True)
    idCardNO = models.CharField(max_length=20, blank=False, verbose_name='身份证号码')
    truckCompanyCode = models.ForeignKey(DriverCompany, on_delete=models.DO_NOTHING, verbose_name='车队', null=True, blank=True)
    truckNO = models.CharField(max_length=20, verbose_name='驾驶车辆', null=True, blank=True)
    firstCardDate = models.DateField(verbose_name='初次发证日期', null=True, blank=True)
    illegalCount = models.IntegerField(verbose_name='违章次数', null=True, blank=True)
    isDelete = models.BooleanField(default=False, editable=False)

    # def delete(self, using=None, keep_parents=False):
    #     self.isDelete = True
    #     self.save()

    def __str__(self):
        return '司机信息:%s(%s)' % (self.driverName, self.idCardNO)

    class Meta:
        verbose_name = '6.0 司机信息'


class Truck(models.Model):
    TRUCK_TYPE_CHOICES = (
        ('牵引车', '牵引车'),
        ('挂车', '挂车')
    )
    truckID = models.BigIntegerField(primary_key=True)
    realTruck = models.CharField(max_length=12, verbose_name='真实车牌号', null=True, blank=True)
    truckNO = models.CharField(max_length=12, verbose_name='车号', null=True, blank=True)
    owner = models.CharField(max_length=40, verbose_name='车主', null=True, blank=True)
    isLock = models.BooleanField(default=False, verbose_name='是否锁定', blank=True)
    weight = models.IntegerField(verbose_name='拖头重(kg)', null=True, blank=True)
    pcc = models.CharField(max_length=15, verbose_name='PCC卡号', null=True, blank=True)
    companyCode = models.CharField(max_length=48, verbose_name='所属拖车公司', null=True, blank=True)
    company = models.CharField(max_length=48, verbose_name='所属拖车公司', null=True, blank=True)

    basMes = models.CharField(max_length=200, verbose_name='备注', null=True, blank=True)
    truckType = models.CharField(max_length=15, verbose_name='车辆类型', null=True, blank=True, choices=TRUCK_TYPE_CHOICES)
    fileNO = models.CharField(max_length=48, verbose_name='档案号', null=True, blank=True)
    isZX = models.BooleanField(default=False, verbose_name='是否自卸', blank=True)
    regDate = models.DateField(verbose_name='注册日期', null=True, blank=True)
    checkDate = models.DateField(verbose_name='年审月份', null=True, blank=True)
    tranNO = models.CharField(max_length=48, verbose_name='道路运输证号', null=True, blank=True)
    insuranceNO = models.CharField(max_length=48, verbose_name='保险单号', null=True, blank=True)

    driver = models.ForeignKey(Driver,  on_delete=models.DO_NOTHING, null=True, blank=True)
    createMan = models.CharField(max_length=15, verbose_name='创建人', null=True, blank=True)
    createTime = models.DateTimeField(verbose_name='创建时间', null=True, blank=True)
    updateMan = models.CharField(max_length=40, verbose_name='更新人', null=True, blank=True)
    updateTime = models.DateTimeField(verbose_name='更新时间', null=True, blank=True)
    createManCName = models.CharField(max_length=15, verbose_name='创建人', null=True, blank=True)
    updateManCName = models.CharField(max_length=40, verbose_name='更新人', null=True, blank=True)
    isPCC = models.BooleanField(default=False, verbose_name='是否启用IC卡', blank=True)

    def __str__(self):
        return '外拖:%s(%s)' % (self.truckNO if self.truckNO is not None else '', self.realTruck)

    class Meta:
        verbose_name = '2.0 拖车信息'


class TruckIIllegal(models.Model):
    TRUCK_TYPE_CHOICES = (
        ('已处理', '已处理'),
        ('待处理', '待处理')
    )
    illegalTime = models.DateTimeField(verbose_name='违章时间')
    code = models.ForeignKey(ViolationCode, on_delete=models.DO_NOTHING, verbose_name='违章代码', null=True, blank=True)
    truck = models.ForeignKey(Truck, on_delete=models.DO_NOTHING, verbose_name='拖车', null=True, blank=True)
    driverName = models.CharField(max_length=20, verbose_name='司机姓名', null=True, blank=True)
    status = models.CharField(max_length=10, choices=TRUCK_TYPE_CHOICES, verbose_name='状态', null=True, blank=True)
    desc = models.TextField(verbose_name='描述', null=True, blank=True)
    lockStartTime = models.DateTimeField(verbose_name='锁车开始时间', null=True, blank=True)
    lockEndTime = models.DateTimeField(verbose_name='锁车结束时间', null=True, blank=True)
    checkMan = models.ForeignKey(CheckMan, on_delete=models.DO_NOTHING, verbose_name='查处人', null=True, blank=True)

    def __str__(self):
        return '违章管理:%s(%s)' % (self.illegalTime, self.code)

    class Meta:
        verbose_name = '3.0违章管理'


class OutMan(models.Model):
    cname = models.CharField(max_length=15, blank=False, verbose_name='姓 名')
    sex = models.CharField(max_length=2, verbose_name='性别', null=True, blank=True)
    cardID = models.CharField(max_length=20, verbose_name='身份证号码')
    telPhone = models.CharField(max_length=20, verbose_name='联系电话', null=True, blank=True)
    inPortNO = models.CharField(max_length=20, verbose_name='进港证编号', null=True, blank=True)
    unitName = models.CharField(max_length=45, verbose_name='单 位', null=True, blank=True)
    position = models.CharField(max_length=15, verbose_name='职务', null=True, blank=True)
    lxr = models.CharField(max_length=15, verbose_name='单位联系人', null=True, blank=True)
    unitPhone = models.CharField(max_length=20, verbose_name='单位联系人电话', null=True, blank=True)
    certificateDate = models.DateField(verbose_name='初次发证时间', null=True, blank=True)
    illegalCount = models.IntegerField(default=0, verbose_name='违章次数', editable=False, null=True, blank=True)
    bakMsg = models.TextField(max_length=100, verbose_name='备注', null=True, blank=True)
    isDelete = models.BooleanField(default=False, editable=False)

    # def delete(self, using=None, keep_parents=False):
    #     self.isDelete = True
    #     self.save()

    class Meta:
        verbose_name = '7.0 外来人员'


class OutCar(models.Model):
    truckNO = models.CharField(max_length=15, verbose_name='车牌号')
    driverName = models.CharField(max_length=15, verbose_name='驾驶者姓名', null=True, blank=True)
    sex = models.CharField(max_length=2, verbose_name='性别', null=True, blank=True)
    cardID = models.CharField(max_length=20, verbose_name='身份证号码', null=True, blank=True)
    telPhone = models.CharField(max_length=20, verbose_name='联系电话', null=True, blank=True)
    inPortNO = models.CharField(max_length=20, verbose_name='进港证编号', null=True, blank=True)
    unitName = models.CharField(max_length=45, verbose_name='单 位', null=True, blank=True)
    position = models.CharField(max_length=15, verbose_name='职务', null=True, blank=True)
    lxr = models.CharField(max_length=15, verbose_name='单位联系人', null=True, blank=True)
    unitPhone = models.CharField(max_length=20, verbose_name='单位联系人电话', null=True, blank=True)
    inResion = models.TextField(verbose_name='进港理由', null=True, blank=True)
    firstCardDate = models.DateField(verbose_name='初次发证时间', null=True, blank=True)
    illegalCount = models.IntegerField(default=0, verbose_name='违章次数', editable=False)
    bakMsg = models.TextField(verbose_name='备注', null=True, blank=True)
    isDelete = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return '外来车辆:%s(%s)' % (self.truckNO, self.driverName)

    class Meta:
        verbose_name = '8.0 外来车辆'


class Illegal(models.Model):
    illegalDate = models.DateField(verbose_name='违章日期')
    illegalAttribute = models.ForeignKey(IllegalAttribute, on_delete=models.DO_NOTHING, verbose_name='违章性质', null=True, blank=True)
    illegalCode = models.ForeignKey(ViolationCode, on_delete=models.DO_NOTHING, verbose_name='违章代码', null=True, blank=True, default=None)
    illegalDesc = models.TextField(verbose_name='三违行为概述', null=True, blank=True)
    illegalMan = models.CharField(max_length=120, verbose_name='违章者', null=True, blank=True)

    resDept = models.ForeignKey(ResDept, on_delete=models.DO_NOTHING, verbose_name='责任部门(或公司)', null=True, blank=True)
    resGroup = models.ForeignKey(ResGroup, on_delete=models.DO_NOTHING, verbose_name='班组', null=True, blank=True)
    handle = models.CharField(max_length=20, verbose_name='处理情况', null=True, blank=True)
    resMoney = models.FloatField(verbose_name='罚金(元', null=True, blank=True)
    allRes = models.TextField(verbose_name='连带责任', null=True, blank=True)

    checkMan = models.ForeignKey(CheckMan, on_delete=models.DO_NOTHING, verbose_name='查处人', null=True, blank=True)
    bakMsg = models.TextField(verbose_name='备 注', null=True, blank=True)
    isDelete = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return '人员违章:%s' % self.illegalDate

    class Meta:
        verbose_name = '9.0 人员违章'




