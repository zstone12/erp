
from django.db import models
from app01.models import School

class User(models.Model):
    """

    """

    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    c_time = models.DateTimeField(auto_now_add=True)
    school = models.ManyToManyField(School,blank=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '员工用户'
        verbose_name_plural = '员工用户'
