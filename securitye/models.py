from django.db import models

# Create your models here.


class CarModel(models.Model):
    driverType = models.CharField(max_length=3, primary_key=True, verbose_name='准驾类型')
    desc = models.CharField(max_length=20, verbose_name='描述')

    def __str__(self):
        return '%s(%s)' % (self.driverType, self.desc)

    class Meta:
        verbose_name = '准驾类型'


class DriverCompany(models.Model):
    companyName = models.CharField(max_length=30, verbose_name='车队名称')
    isDelete = models.BooleanField(default=False, verbose_name='是否有效')
    recordMan = models.CharField(max_length=15, verbose_name='记录人')
    recordTime = models.DateField(auto_now_add=True, verbose_name='记录时间')
    cancelMan = models.CharField(max_length=15, verbose_name='更新人')
    cancelTime = models.DateTimeField(verbose_name='更新时间')

    def __str__(self):
        return self.companyName

    class Meta:
        verbose_name = '车队'


class Driver(models.Model):
    driverName = models.CharField(max_length=15, blank=False, verbose_name='司机姓名')
    driverType = models.ForeignKey(CarModel, on_delete=models.DO_NOTHING, verbose_name='准驾类型')
    telPhone = models.CharField(max_length=20, verbose_name='司机电话')
    idCardNO = models.CharField(max_length=20, blank=False, verbose_name='身份证号码')
    truckCompanyCode = models.ForeignKey(DriverCompany, on_delete=models.DO_NOTHING, verbose_name='车队')
    truckNO = models.CharField(max_length=20, verbose_name='驾驶车辆')
    firstCardDate = models.DateField(verbose_name='初次发证日期')
    illegalCount = models.IntegerField(verbose_name='违章次数')
    isDelete = models.BooleanField(default=False)

    class Meta:
        verbose_name = '1.司机信息'


class DriverJobCard(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    startTime = models.DateField(verbose_name='开始有效期')
    endTime = models.DateField(verbose_name='结束有效期')
    recordMan = models.CharField(max_length=15, blank=False, verbose_name='记录人')
    recordTime = models.DateField(auto_now_add=True, verbose_name='记录时间')
    cancelMan = models.CharField(max_length=15, blank=False, verbose_name='取消人')
    cancelTime = models.DateTimeField(verbose_name='取消时间')
    isOn = models.CharField(default='Y', max_length=1, verbose_name='是否有效')
    isDelete = models.BooleanField(default=False)

    class Meta:
        verbose_name = '司机从业资格证'


class DriverTran(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    status = models.TextField(verbose_name='培训情况')
    recordMan = models.CharField(max_length=20, verbose_name='记录人')
    recordTime = models.DateField(auto_now_add=True, verbose_name='记录时间')
    cancelMan = models.CharField(max_length=20, verbose_name='取消人')
    cancelTime = models.DateField(verbose_name='取消时间')
    isOn = models.CharField(default='Y', max_length=1, verbose_name='是否有效')
    isDelete = models.BooleanField(default=False)

    class Meta:
        verbose_name = '司机培训'


class DriverTest(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    testScore = models.FloatField(verbose_name='考试成绩')
    testDate = models.DateTimeField(verbose_name='记录时间')
    recordMan = models.CharField(max_length=15, blank=False, verbose_name='记录人')
    recordTime = models.DateField(auto_now_add=True, verbose_name='记录时间')
    cancelMan = models.CharField(max_length=15, blank=False, verbose_name='取消人')
    cancelTime = models.DateTimeField(verbose_name='取消时间')
    isOn = models.CharField(default='Y', max_length=1, verbose_name='是否有效')
    isDelete = models.BooleanField(default=False)

    class Meta:
        verbose_name = '司机考试'


class DriverLearnCard(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    startTime = models.DateField(verbose_name='开始有效期')
    endTime = models.DateField(verbose_name='结束有效期')
    recordMan = models.CharField(max_length=15, blank=False, verbose_name='记录人')
    recordTime = models.DateField(auto_now_add=True, verbose_name='记录时间')
    cancelMan = models.CharField(max_length=15, blank=False, verbose_name='取消人')
    cancelTime = models.DateTimeField(verbose_name='取消时间')
    isOn = models.CharField(default='Y', max_length=1, verbose_name='是否有效')
    isDelete = models.BooleanField(default=False)

    class Meta:
        verbose_name = '司机学习证'


class DriverTempInCard(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    startTime = models.DateField(verbose_name='开始有效期')
    endTime = models.DateField(verbose_name='结束有效期')
    recordMan = models.CharField(max_length=15, blank=False, verbose_name='记录人')
    recordTime = models.DateField(auto_now_add=True, verbose_name='记录时间')
    cancelMan = models.CharField(max_length=15, blank=False, verbose_name='取消人')
    cancelTime = models.DateTimeField(verbose_name='取消时间')
    isOn = models.CharField(default='Y', max_length=1, verbose_name='是否有效')
    isDelete = models.BooleanField(default=False)

    class Meta:
        verbose_name = '临时进港证'


class DriverLongInCard(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    startTime = models.DateField(verbose_name='开始有效期')
    endTime = models.DateField(verbose_name='结束有效期')
    recordMan = models.CharField(max_length=15, blank=False, verbose_name='记录人')
    recordTime = models.DateField(auto_now_add=True, verbose_name='记录时间')
    cancelMan = models.CharField(max_length=15, blank=False, verbose_name='取消人')
    cancelTime = models.DateTimeField(verbose_name='取消时间')
    isOn = models.CharField(default='Y', max_length=1, verbose_name='是否有效')
    isDelete = models.BooleanField(default=False)

    class Meta:
        verbose_name = '长期进港证'

#end driver


class OutMan(models.Model):
    cname = models.CharField(max_length=15, blank=False, verbose_name='姓 名')
    sex = models.CharField(max_length=2, verbose_name='性别')
    cardID = models.CharField(max_length=20, verbose_name='身份证号码')
    telPhone = models.CharField(max_length=20, verbose_name='联系电话')
    inPortNO = models.CharField(max_length=20, verbose_name='进港证编号')
    unitName = models.CharField(max_length=45, verbose_name='单 位')
    position = models.CharField(max_length=15, verbose_name='职务')
    lxr = models.CharField(max_length=15, verbose_name='单位联系人')
    unitPhone = models.CharField(max_length=20, verbose_name='单位联系人电话')
    certificateDate = models.DateField(verbose_name='初次发证时间')
    vaildStartDate = models.DateField(verbose_name='有效期')
    vaildEndDate = models.DateField(verbose_name='有效期')
    illegalCount = models.IntegerField(default=0, verbose_name='违章次数')
    bakMsg = models.TextField(max_length=100, verbose_name='备注')
    isDelete = models.BooleanField(default=False)

    class Meta:
        verbose_name = '外来人员'


class OutCar(models.Model):
    truckNO = models.CharField(max_length=15, verbose_name='车牌号')
    driverName = models.CharField(max_length=15, verbose_name='驾驶者姓名')
    sex = models.CharField(max_length=2, verbose_name='性别')
    cardID = models.CharField(max_length=20, verbose_name='身份证号码')
    telPhone = models.CharField(max_length=20, verbose_name='联系电话')
    inPortNO = models.CharField(max_length=20, verbose_name='进港证编号')
    unitName = models.CharField(max_length=45, verbose_name='单 位')
    position = models.CharField(max_length=15, verbose_name='职务')
    lxr = models.CharField(max_length=15, verbose_name='单位联系人')
    unitPhone = models.CharField(max_length=20, verbose_name='单位联系人电话')
    inResion = models.TextField(verbose_name='进港理由')
    trainStatus = models.CharField(max_length=20, verbose_name='培训情况')
    firstCardDate = models.DateField(verbose_name='初次发证时间')
    vaildStartDate = models.DateField(verbose_name='有效期')
    vaildEndDate = models.DateField(verbose_name='有效期')
    illegalCount = models.IntegerField(default=0, verbose_name='违章次数')
    bakMsg = models.TextField(verbose_name='备注')
    isDelete = models.BooleanField(default=False)

    class Meta:
        verbose_name = '外来车辆'


class Illegal(models.Model):
    illegalDate = models.DateField(verbose_name='违章日期')
    illegalAttribute = models.CharField(max_length=15, verbose_name='违章性质')
    illegalCode = models.CharField(max_length=15, verbose_name='违章代码')
    illegalDesc = models.TextField(verbose_name='三违行为概述')
    illegalMan = models.CharField(max_length=120, verbose_name='违章者')
    resDept = models.CharField(max_length=120, verbose_name='责任部门(或公司)')
    resGroup = models.CharField(max_length=120, verbose_name='班组')
    handle = models.CharField(max_length=20, verbose_name='处理情况')
    resMoney = models.FloatField(verbose_name='罚金(元')
    allRes = models.TextField(verbose_name='连带责任')
    checkMan = models.CharField(max_length=120, verbose_name='查处人')
    bakMsg = models.TextField(verbose_name='备 注')
    isDelete = models.BooleanField(default=False)

    class Meta:
        verbose_name = '人员违章'


class IllegalImage(models.Model):
    illegal = models.ForeignKey(Illegal, on_delete=models.CASCADE, verbose_name='IllegalID')
    image = models.ImageField()
    cTime = models.DateField(auto_now_add=True, verbose_name='图片日期')
    isDelete = models.BooleanField(default=False)

    class Meta:
        verbose_name = '人员违章图片'





class OutCarTran(models.Model):
    driver = models.ForeignKey(OutCar, on_delete=models.CASCADE)
    status = models.TextField(verbose_name='培训情况')
    recordMan = models.CharField(max_length=20, verbose_name='记录人')
    recordTime = models.DateField(auto_now_add=True, verbose_name='记录时间')
    cancelMan = models.CharField(max_length=20, verbose_name='取消人')
    cancelTime = models.DateField(verbose_name='取消时间')
    isOn = models.CharField(default='Y', max_length=1, verbose_name='是否有效')
    isDelete = models.BooleanField(default=False)

    class Meta:
        verbose_name = '外车培训'





class OutCarCard(models.Model):
    carID = models.ForeignKey(OutCar, on_delete=models.CASCADE)
    startTime = models.DateField(verbose_name='开始有效期')
    endTime = models.DateField(verbose_name='结束有效期')
    recordMan = models.CharField(max_length=15, blank=False, verbose_name='记录人')
    recordTime = models.DateField(auto_now_add=True, verbose_name='记录时间')
    cancelMan = models.CharField(max_length=15, blank=False, verbose_name='取消人')
    cancelTime = models.DateTimeField(verbose_name='取消时间')
    isOn = models.CharField(default='Y', max_length=1, verbose_name='是否有效')
    isDelete = models.BooleanField(default=False)

    class Meta:
        verbose_name = '外车进港证有效期'


class OutManCard(models.Model):
    manID = models.ForeignKey(OutMan, on_delete=models.CASCADE)
    startTime = models.DateField(verbose_name='开始有效期')
    endTime = models.DateField(verbose_name='结束有效期')
    recordMan = models.CharField(max_length=15, blank=False, verbose_name='记录人')
    recordTime = models.DateField(auto_now_add=True, verbose_name='记录时间')
    cancelMan = models.CharField(max_length=15, blank=False, verbose_name='取消人')
    cancelTime = models.DateTimeField(verbose_name='取消时间')
    isOn = models.CharField(default='Y', max_length=1, verbose_name='是否有效')
    isDelete = models.BooleanField(default=False)

    class Meta:
        verbose_name = '外来人员进港证有效期'


class IllegalAttribute(models.Model):
    illegalAttribute = models.CharField(max_length=15, verbose_name='违章性质', unique=True)

    class Meta:
        verbose_name = '违章性质'


class ResDept(models.Model):
    resDept = models.CharField(max_length=120, verbose_name='责任部门(或公司)', unique=True)

    class Meta:
        verbose_name = '责任部门(或公司)'


class ResGroup(models.Model):
    resGroup = models.CharField(max_length=120, verbose_name='班组', unique=True)

    class Meta:
        verbose_name = '责任班组'


class CheckMan(models.Model):
    checkMan = models.CharField(max_length=120, verbose_name='查处人', unique=True)

    class Meta:
        verbose_name = '检查人'

