from django.db import models


class er_truck(models.Model):
    truckid = models.IntegerField(primary_key=True)
    truckheadweight = models.FloatField()
    REALTRUCKNO = models.CharField(max_length=40)
    PCCNO = models.CharField(max_length=40)
    TRUCKOWNER = models.CharField(max_length=40)
    TRAILNO = models.CharField(max_length=40)
    ISLOCK = models.CharField(max_length=40)
    REMARK = models.CharField(max_length=40)
    LASTUPDATEMAN = models.CharField(max_length=40)

    class Meta:
        db_table = 'er_truck'


class pl_guests(models.Model):
    GUESTCODE = models.CharField(max_length=40, primary_key=True)
    CNAME = models.CharField(max_length=40)
    CONTACTMAN = models.CharField(max_length=40)
    ADDRESS = models.CharField(max_length=40)
    CONTACTPERSON = models.CharField(max_length=40)
    CONTACTTEL = models.CharField(max_length=40)
    CONTACTMOBIL = models.CharField(max_length=40)
    FAX = models.CharField(max_length=40)
    CONTACTMAN2 = models.CharField(max_length=40)
    TELEPHONE2 = models.CharField(max_length=40)
    CELLPHONE = models.CharField(max_length=40)
    EMAIL = models.CharField(max_length=40)
    MEMO = models.CharField(max_length=400)
    CREATEMAN = models.CharField(max_length=40)
    CREATETIME = models.DateTimeField()
    LASTUPDATEMAN = models.CharField(max_length=40)
    LASTUPDATETIME = models.DateTimeField()
    ISTRUCKCOMPANY = models.CharField(max_length=1)

    class Meta:
        db_table = 'pl_guests'


class er_truckbody_prj(models.Model):
    TRUCKBODYCODE_PRJ = models.CharField(max_length=40, primary_key=True)
    TRUCKBODYTYPECODE_PRJ = models.CharField(max_length=40)
    WEIGHT_PRJ = models.IntegerField()
    TRUCKCOMPANY_PRJ = models.CharField(max_length=40)
    MEMO_PRJ = models.CharField(max_length=400)

    class Meta:
        db_table = 'er_truckbody_prj'


class er_violationcode(models.Model):
    VIOLATIONCODEID = models.IntegerField(primary_key=True)
    VIOLATIONCODE = models.CharField(max_length=40)
    PENALTY = models.FloatField()
    CONTENT = models.CharField(max_length=140)
    ISPENALTY = models.CharField(max_length=2)
    LASTUPDATEMAN = models.CharField(max_length=40)
    LASTUPDATETIME = models.DateTimeField()

    class Meta:
        db_table = 'er_violationcode'
