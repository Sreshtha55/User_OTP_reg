from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.mail import send_mail
import math, random
from django.conf import settings
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required

# from django.contrib.auth.hashers import check_password

def home(request):
    if request.method=="POST":
        email=request.POST.get("email")
        print("Email: ",email)
        # password=request.POST["password"]
        obj=Profile.objects.filter(user__username=email)
        if obj.exists():
            request.session['email']=email
            if Profile.objects.get(user__username=email).is_verified:
                return render(request,"success.html",{"email":request.session['email']})
            else:
                return redirect("verify")
        else:
            # user_obj=User.objects.create_user(username = email,password=password)
            user_obj=User.objects.create(username = email)
            # user_obj.save()
            p_obj=Profile.objects.create(
                user=user_obj,
                email_otp=generateOTP()
            )
            messages.info(request,"Profile Created")
            request.session['email']=email
            return send_otp(request,request.session['email'],p_obj.email_otp)


    return render(request, "home.html")

def verify(request):
    email=request.session.get("email")
    if request.method=="POST":
        otp=request.POST.get("otp")
        obj=Profile.objects.get(email_otp=otp,user__username=email)
        if obj:
            if obj.is_verified:
                return render(request,"verification.html",{"email":request.session['email']})
            else:
                obj.is_verified=True
                obj.save()
                return render(request,"success.html",{"email":email})
        # return True
    if request.method=="GET":
        obj=Profile.objects.get(user__username=email)
        if obj.is_verified:
            return render(request,"success.html",{"email":email})
        else:
            return render(request,"verification.html",{"email":email})
        # return False
    


def generateOTP() :
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def send_otp(request,email,otp):
    print(email)
    try:
        subject="OTP to verify your Email"
        emai_from=settings.EMAIL_HOST_USER
        recepient_list=[email,]
        htmlgen = f'Your OTP is {otp}.'
        send_mail(subject,htmlgen,emai_from,recepient_list, fail_silently=False)
    except Exception as e:
        print(e)
        return HttpResponse("Email failed to send with error: "+e)
    # return HttpResponse(o)
    
    return redirect("verify")
