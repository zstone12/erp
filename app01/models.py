from django.db import models
from django.utils import timezone


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    admin_right = models.BooleanField(default=False)


class Student(models.Model):
    tb_username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    school = models.ForeignKey("School", on_delete=models.CASCADE, )
    state = models.BooleanField(default=False)


class School(models.Model):
    school_name = models.CharField(max_length=50)
    user = models.ManyToManyField(User,blank=True)


class Shop(models.Model):
    shop_name = models.CharField(max_length=100)
    cooperate_state = models.BooleanField(default=True)
    students = models.ManyToManyField(Student, through='StudentShop')


class StudentShop(models.Model):
    shop = models.ForeignKey("Shop", on_delete=models.CASCADE, )
    student = models.ForeignKey("Student", on_delete=models.CASCADE, )
    order_time = models.DateTimeField(default=timezone.now)
    money = models.IntegerField(default=0,blank=True)
    order_number = models.CharField(default=0,max_length=100,blank=True)
