
from django.db import models
from securitye.models import *

# Create your models here.


class DriverJobCard(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='司机')
    startTime = models.DateField(verbose_name='开始有效期')
    endTime = models.DateField(verbose_name='结束有效期')

    isDelete = models.BooleanField(default=False, editable=False)

    def delete(self, using=None, keep_parents=False):
        self.isDelete = True
        self.save()

    def __str__(self):
        return '从业资格证:%s至%s' % (self.startTime, self.endTime)

    class Meta:
        verbose_name = '司机从业资格证'


class DriverTest(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='司机')
    testScore = models.FloatField(verbose_name='考试成绩')
    testDate = models.DateTimeField(verbose_name='考试时间')

    isDelete = models.BooleanField(default=False, editable=False, null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        self.isDelete = True
        self.save()

    def __str__(self):
        return '考试:%s至%s' % (self.testDate, self.testScore)

    class Meta:
        verbose_name = '司机考试'


class DriverLearnCard(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='司机')
    startTime = models.DateField(verbose_name='开始有效期')
    endTime = models.DateField(verbose_name='结束有效期')

    isDelete = models.BooleanField(default=False, editable=False)

    def delete(self, using=None, keep_parents=False):
        self.isDelete = True
        self.save()

    def __str__(self):
        return '学习证:%s至%s' % (self.startTime, self.endTime)

    class Meta:
        verbose_name = '司机学习证'


class DriverTempInCard(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    startTime = models.DateField(verbose_name='开始有效期')
    endTime = models.DateField(verbose_name='结束有效期')

    isDelete = models.BooleanField(default=False, editable=False)

    def delete(self, using=None, keep_parents=False):
        self.isDelete = True
        self.save()

    def __str__(self):
        return '临时进港证:%s至%s' % (self.startTime, self.endTime)

    class Meta:
        verbose_name = '临时进港证'


class DriverLongInCard(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    startTime = models.DateField(verbose_name='开始有效期')
    endTime = models.DateField(verbose_name='结束有效期')

    isDelete = models.BooleanField(default=False, editable=False)

    def delete(self, using=None, keep_parents=False):
        self.isDelete = True
        self.save()

    def __str__(self):
        return '长期进港证:%s至%s' % (self.startTime, self.endTime)

    class Meta:
        verbose_name = '长期进港证'


class OutManCard(models.Model):
    manID = models.ForeignKey(OutMan, on_delete=models.CASCADE, verbose_name='外来人员')
    startTime = models.DateField(verbose_name='开始有效期')
    endTime = models.DateField(verbose_name='结束有效期')
    isDelete = models.BooleanField(default=False, editable=False)

    def delete(self, using=None, keep_parents=False):
        self.isDelete = True
        self.save()

    class Meta:
        verbose_name = '外来人员进港证有效期'


class OutCarTran(models.Model):
    driver = models.ForeignKey(OutCar, on_delete=models.CASCADE)
    status = models.TextField(verbose_name='培训情况')
    tranDate = models.DateField(verbose_name='培训时间')
    isDelete = models.BooleanField(default=False, editable=False)

    def delete(self, using=None, keep_parents=False):
        self.isDelete = True
        self.save()

    class Meta:
        verbose_name = '外车培训'


class OutCarCard(models.Model):
    carID = models.ForeignKey(OutCar, on_delete=models.CASCADE)
    startTime = models.DateField(verbose_name='开始有效期')
    endTime = models.DateField(verbose_name='结束有效期')
    isDelete = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        self.isDelete = True
        self.save()

    class Meta:
        verbose_name = '外车进港证有效期'


class IllegalImage(models.Model):
    illegal = models.ForeignKey(Illegal, on_delete=models.CASCADE, verbose_name='IllegalID')
    image = models.ImageField(u'图片', upload_to='photos/%Y/%m/%d')
    cTime = models.DateField(auto_now_add=True, verbose_name='图片日期')
    isDelete = models.BooleanField(default=False, editable=False)

    class Meta:
        verbose_name = '人员违章图片'


class DriverTran(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='司机')
    status = models.TextField(verbose_name='培训情况')
    tranDate = models.DateField(verbose_name='培训时间', default=None)

    isDelete = models.BooleanField(default=False, editable=False, null=True, blank=True)

    def delete(self, using=None, keep_parents=False):
        self.isDelete = True
        self.save()

    def __str__(self):
        return '培训(%s):%s' % (self.tranDate, self.status)

    class Meta:
        verbose_name = '其他:司机培训'
