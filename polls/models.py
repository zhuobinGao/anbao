import uuid
from django.db import models

# Create your models here.

#
# class Poll_Question(models.Model):
#     question_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     question_text = models.CharField(max_length=200)
#     pub_date = models.DateTimeField('date published')
#
#
# class Poll_Choice(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     question = models.ForeignKey(Poll_Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=200)
#     votes = models.IntegerField(default=0)
