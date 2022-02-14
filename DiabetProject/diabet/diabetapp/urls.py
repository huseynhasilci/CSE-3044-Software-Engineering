from django.urls import path
from diabetapp import views

app_name = 'diabetapp'

urlpatterns=[

    path('register/',views.register,name='register'),
    path('user_login/',views.user_login,name='user_login'),
    path('calorieIntake/',views.calculateCalorieIntake,name='calorieIntake'),
    path('amIinRisk/',views.amIinRisk,name='amIinRisk'),
    path('userinfofunc',views.userInfosFunc,name='userinfofunc'),
    path('update_amiinrisk', views.update_amiinrisk, name='update_amiinrisk')

]
