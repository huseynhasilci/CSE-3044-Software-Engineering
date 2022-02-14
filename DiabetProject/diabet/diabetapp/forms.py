from django import forms
from django.contrib.auth.models import User
from .models import UserInfos,UserDiabeticInfos,UserDailyCalorie

class UserForm(forms.ModelForm):
        password = forms.CharField(widget=forms.PasswordInput())
        class Meta():
            model = User
            fields = ('username','email','password')

class UserInfosForm(forms.ModelForm):

    class Meta():
        model = UserInfos
        fields = ('name','surname','age','gender','weight','height')

class UserDiabeticInfosForm(forms.ModelForm):

    class Meta():
        model = UserDiabeticInfos
        fields = ('pregnancie','glucose','bloodPressure','skinThickness','insulin','diabetesPedigreeFunction')

class UserCalorieForm(forms.ModelForm):
    class Meta():
        model = UserInfos
        fields = ('calorie',)

#class UserDiabeticInfosFormEdit(forms.ModelForm):

#    class Meta():
#        model = UserDiabeticInfos
