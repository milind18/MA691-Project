from django.shortcuts import render
from .forms import UserForm
from django.conf import settings
import os

##COBRA Model Libraries
import pandas as pd
import numpy as np

from .cobra import Cobra 

##Upload model
def upload_model():
    file_ = open(os.path.join(settings.BASE_DIR, 'insurance.csv'))
    df_claim = pd.read_csv(file_)

    df_claim.sex = pd.Categorical(df_claim.sex).codes
    df_claim.smoker = pd.Categorical(df_claim.smoker).codes
    df_claim.region = pd.Categorical(df_claim.region).codes


    X = df_claim.drop(columns=["expenses"])
    Y = df_claim["expenses"]

    # Train Data
    X_train = np.array(X)
    y_train = np.array(Y)

    ##Training COBRA
    COBRA = Cobra(eps = 5122)
    COBRA.fit(X_train, y_train, 0.5)

    return COBRA

def predict_insurance_premium(COBRA, age, sex1, bmi, children, smoker1, region):
    region_map = {'southwest': 0, 'southeast': 1, 'northwest': 2, 'northeast': 3}
    region = region_map[region]
    if (sex1 == "M"):
        sex = 0
    else:
        sex = 1

    if (smoker1==True):
        smoker = 1
    else:
        smoker = 0


    feature_vector = np.array([[age, sex, bmi, children, smoker, region]])
    print("feature>>>>>>>>>>>>>>>>>>>>>>>>>", feature_vector)
    insurance_premium = COBRA.predict(feature_vector)
    return insurance_premium

# Create your views here.
def home(request):

    #uploading COBRA model
    COBRA = upload_model()

    form = UserForm()
    context = {'form':form, 'data':False, 'insurance_price':10000}
    
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            context['form'] = form
            context['data'] = True
            #context['insurance_price'] = form['age']

            ##Extracting features
            age = form['age'].value()
            sex = form['sex'].value()
            bmi = form['bmi'].value()
            children = form['children'].value()
            smoker = form['smoker'].value()
            region = form['region'].value()
            print(age, sex, bmi, children, region)

            context['insurance_price'] = predict_insurance_premium(COBRA, age, sex, bmi, children, smoker, region)
            
            print(form)
        
    return render(request, 'home.html', context)