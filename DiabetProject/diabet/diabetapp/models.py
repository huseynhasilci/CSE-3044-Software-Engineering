from django.db import models
from django.contrib.auth.models import User


class UserInfos(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=256)
    surname = models.CharField(max_length=256)
    age = models.PositiveIntegerField()
    BOOL_CHOICES = ((True, 'Male'), (False, 'Female'))
    gender = models.BooleanField(choices=BOOL_CHOICES, default=False)
    #gender_male = models.BooleanField(default = False)
    #gender_female = models.BooleanField(default = False)
    weight = models.FloatField()
    height = models.PositiveIntegerField()
    #dc_date = models.DateTimeField(auto_now_add=True)
    calorie = models.PositiveIntegerField()
    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username

class UserDiabeticInfos(models.Model):

    userD = models.ForeignKey(UserInfos, on_delete=models.CASCADE)

    pregnancie = models.PositiveIntegerField()
    glucose = models.PositiveIntegerField()
    bloodPressure = models.PositiveIntegerField()
    skinThickness = models.PositiveIntegerField()
    insulin = models.PositiveIntegerField()
    diabetesPedigreeFunction = models.FloatField()

class UserDailyCalorie(models.Model):
    #userDC = models.ForeignKey(UserInfos, on_delete=models.CASCADE)
    calorie = models.PositiveIntegerField()
    dc_date = models.DateTimeField(auto_now_add=True)
