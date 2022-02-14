from django.shortcuts import render,redirect
from .forms import UserForm,UserInfosForm,UserDiabeticInfosForm,UserCalorieForm
from .models import UserInfos,UserDiabeticInfos,UserDailyCalorie
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# Create your views here.

class Food:
    def __init__(self,name,species,calorie):
        self.name=name
        self.species=species
        self.calorie=calorie

food_w_caloires= dict()
food_list = pd.read_excel("diabetapp/food_calorie_list.xlsx",sheet_name="Sheet1")

for i in range(len(food_list['Name'])):
    name = food_list['Name'][i]
    species = food_list['Food_Group'][i]
    calorie = food_list['Calories'][i]
    food_w_caloires[name] = [name, species, calorie]



def index(request):
    return render(request,'index.html')
def aboutus(request):
    return render(request,'aboutus.html')

@login_required
def amIinRisk(request):

    guessed = False
    current_user = request.user.id
    getDatas = UserInfos.objects.get(pk=current_user-1)
    if request.method == 'POST':
        postUserDiabeticInfoForm = UserDiabeticInfosForm(request.POST)

        if postUserDiabeticInfoForm.is_valid():
            guessedUserData = postUserDiabeticInfoForm.save(commit=False)
            guessedUserData.userD = UserInfos.objects.get(pk=current_user-1)
            guessedUserData.save()
            guessed = True
        else:
            print(postUserDiabeticInfoForm.errors)

    else:
        postUserDiabeticInfoForm = UserDiabeticInfosForm()

    amIinRiskDict = {'postUserDiabeticInfoForm':postUserDiabeticInfoForm,'guessed':guessed}

    return render(request,'amIinRisk.html',amIinRiskDict)

def update_amiinrisk(request):
    updated = False
    current_user = request.user.id
    userdiabeticinfos = UserDiabeticInfos.objects.get(pk=current_user-1)
    form = UserDiabeticInfosForm(request.POST or None, instance=userdiabeticinfos)
    if form.is_valid():
        form.save()
        updated = True
        return redirect('index')
    return render(request, 'updateAmIinRisk.html',{'userdiabeticinfos': userdiabeticinfos,'form':form,'updated':updated})


@login_required
def userInfosFunc(request):

    current_user = request.user.id
    #print(current_user)
    getDatas = UserInfos.objects.get(pk=current_user-1)
    getUserDiabeticDatas = UserDiabeticInfos.objects.get(pk=current_user-1)
    dataUser = getDatas.user
    dataHeight = getDatas.height
    dataWeight = getDatas.weight
    data2Age = getDatas.age
    userCal = 664+(9.6*dataWeight)+(1.7*dataHeight)-(4.7*data2Age)
    dataName = getDatas.name
    dataSurame = getDatas.surname
    userBMI = dataWeight / (dataHeight**2)*(10000)
    userBMI = float(str(userBMI)[:5])

    if userBMI < 18.5:
        weightStatus = 'Under Weight'
    elif 25 > userBMI >= 18.5:
        weightStatus = 'Normal Weight'
    elif 30 > userBMI >= 25:
        weightStatus = 'Overweight'
    elif 35 > userBMI >= 30:
        weightStatus = 'Obesity Class I'
    elif 40 > userBMI >= 35:
        weightStatus = 'Obesity Class II'
    else:
        weightStatus = 'Obesity Class III'
    #-----------------------------------------------
    dataPregnancie = getUserDiabeticDatas.pregnancie
    dataGlucose = getUserDiabeticDatas.glucose
    dataBloodPressure = getUserDiabeticDatas.bloodPressure
    dataSkinThickness = getUserDiabeticDatas.skinThickness
    dataInsulin = getUserDiabeticDatas.insulin
    dataDiabetesPedigreeFunction = getUserDiabeticDatas.diabetesPedigreeFunction

    #*******************************************************
    df=pd.read_csv('diabetapp/diabetes2.csv')

    X = df.iloc[:,:-1]
    y = df.iloc[:,-1]
    X_train, X_test, y_train, y_test= train_test_split(X,y,test_size=0.25, random_state=0)
    sc=StandardScaler()
    X_train = sc.fit_transform(X_train)
    X_test = sc.transform(X_test)

    array = np.arange(8).reshape(-1, 8)
    #print(array)
    #print('***********************')
    array[0][0]= dataPregnancie #Pregnancies
    array[0][1]= dataGlucose #Glucose
    array[0][2]= dataBloodPressure #BloodPressure
    array[0][3]= dataSkinThickness #SkinThickness
    array[0][4]= dataInsulin #Insulin
    array[0][5]= userBMI #BMI
    array[0][6]= dataDiabetesPedigreeFunction #DiabetesPedigreeFunction
    array[0][7]= data2Age #Age
    #print(array)
    #print('***********************')
    newX_test = sc.transform(array)
    #print(newX_test[0])

    classifier=LogisticRegression()
    classifier.fit(X_train,y_train)
    y_pred = classifier.predict(newX_test)
    prediction = y_pred[0]

    infosDict = {'dataName':dataName,'dataSurame':dataSurame,'data2Age':data2Age,'dataWeight':dataWeight,'dataHeight':dataHeight,'userCal':userCal,'dataUser':dataUser,'dataPregnancie':dataPregnancie,

        'dataGlucose':dataGlucose,'dataBloodPressure':dataBloodPressure,'dataSkinThickness':dataSkinThickness,'dataInsulin':dataInsulin,'dataDiabetesPedigreeFunction':dataDiabetesPedigreeFunction,'prediction':prediction,

        'userBMI':userBMI,'weightStatus':weightStatus

    }


    return render(request,'userInfos.html',infosDict)

@login_required
def calculateCalorieIntake(request):


    #
    current_user = request.user.id
    #print(current_user)
    getDatas = UserInfos.objects.get(pk=current_user-1)
    #getUserCal = UserDailyCalorie.objects.get(pk=current_user-1)
    #print(getDatas.height)
    c_dataHeight = getDatas.height
    #print(c_dataHeight)

    c_dataWeight = getDatas.weight
    #print(c_dataWeight)

    c_data2Age = getDatas.age
    #print(c_data2Age)

    userCal = 664+(9.6*c_dataWeight)+(1.7*c_dataHeight)-(4.7*c_data2Age)
    #print(userCal)
    cal_taken= 0
    #obj = UserInfos.objects.create(calorie=userCal)
    #obj.save()

    nameList =[]
    speciesList = []
    calorieList = []
    forRange = 120
    for i in range(len(food_list['Name'])):
        nameList.append(food_list['Name'][i])
        speciesList.append(food_list['Food_Group'][i])
        calorieList.append(food_list['Calories'][i])


    #print(type(getDatas.calorie))
    #print(type(getDatas.age))


    #girilendeger  = request.POST.get('key')
    #print(girilendeger)
    dailyCal = UserCalorieForm()
    if 'form_field' in request.POST:
        dailyCal = UserCalorieForm(request.POST)
        if dailyCal.is_valid():
            data = dailyCal.cleaned_data.get("calorie")
            getDatas.calorie += data
            getDatas.save()
            #print(type(data))
                #data.save()
    elif 'set_zero' in request.POST:
        getDatas.calorie = 0
        getDatas.save()
    takenCal = getDatas.calorie
    deneme = (takenCal/userCal)*100
    deneme = int(deneme)
    return render(request,'calorieIntake.html',{'userCal':userCal,'takenCal':takenCal,'deneme':deneme,'nameList':nameList,'speciesList':speciesList,'calorieList':calorieList,'food_w_caloires':food_w_caloires,'forRange':range(120),'dailyCal':dailyCal}) #float((65+((9.6*weight+1.7*height)-4.7*age)) #kadin
    #else:
        #return HttpResponseRedirect(reverse('user_login')) #HttpResponseRedirect(reverse('index'))






@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == 'POST':
        #user = None
        #user_profile = None
        user_form = UserForm(request.POST)
        user_info_form = UserInfosForm(request.POST)

        if(user_form.is_valid() and user_info_form.is_valid()):

            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_profile = user_info_form.save(commit=False)
            user_profile.user = user
            user_profile.calorie = 0
            user_profile.save()
            registered = True
        else:
            print(user_form.errors,user_info_form.errors)

    else:
        user_form = UserForm()
        user_info_form = UserInfosForm()

    return render(request,'register.html',
                          {'user_form':user_form,'registered':registered,'user_profile':user_info_form})
#'user_profile':user_info_form,

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username') # burasi sayesinde template name yerine yazdigimiz degeri cekmis olduk
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)


        if user: # boyle bir user var mi kontrolu
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')
        else:
            print('Someone tried to login and failed!')
            print('Username: {} and Password: {}'.format(username,password))
            return HttpResponse('Invalid login details supplied')
    else:
        return render(request,'login.html',{})
