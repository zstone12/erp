from django.db import models
from django.utils import timezone


class School(models.Model):
    school_name = models.CharField(max_length=50)
    def __str__(self):
        return self.school_name
    class Meta:

        verbose_name = '学校'
        verbose_name_plural = '学校'

class Student(models.Model):
    tb_username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    school = models.ForeignKey("School", on_delete=models.CASCADE, )
    state = models.BooleanField(default=False)





class Shop(models.Model):
    shop_name = models.CharField(max_length=100)
    cooperate_state = models.BooleanField(default=True)
    students = models.ManyToManyField(Student, through='StudentShop')
    def __str__(self):
        return self.shop_name
    class Meta:

        verbose_name = '店铺'
        verbose_name_plural = '店铺'

class StudentShop(models.Model):
    shop = models.ForeignKey("Shop", on_delete=models.CASCADE, )
    student = models.ForeignKey("Student", on_delete=models.CASCADE, )
    order_time = models.DateTimeField(default=timezone.now)
    money = models.IntegerField(default=0,blank=True)
    order_number = models.CharField(default=0,max_length=100,blank=True)
