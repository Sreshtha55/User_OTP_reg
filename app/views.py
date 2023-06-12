from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
import math, random
from django.conf import settings
from django.contrib.auth.models import User
from .models import *
# from django.contrib.auth.hashers import check_password

def home(request):
    if request.method=="POST":
        email=request.POST["email"]
        print("Email: ",email)
        # password=request.POST["password"]
        obj=Profile.objects.filter(user__username=email)
        if obj.exists():
            # if check_password(password,obj.password):
                if Profile.objects.get(user__username=email).is_verified:
                    return render(request,"success.html",{"email":email})
                else:
                    return render(request,"verification.html",{"email":email})
            # else:
            #     return HttpResponse("Email exists but Incorrect Password")
        else:
            # user_obj=User.objects.create_user(username = email,password=password)
            user_obj=User.objects.create(username = email)
            # user_obj.save()
            p_obj=Profile.objects.create(
                user=user_obj,
                email_otp=generateOTP()
            )
            return send_otp(email,p_obj.email_otp)


    return render(request, "home.html")

def verify(request,otp,email):
    try:
        obj=Profile.objects.filter(email_otp=otp,user__username=email).first()
        if obj:
            obj.is_verified=True
            obj.save()
            return HttpResponse("Your account is verified")
        # return True
    except Exception as e:
        print(e)
        return HttpResponse("Invalid Token")
        # return False
    


def generateOTP() :
    digits = "0123456789"
    OTP = ""
    for i in range(4) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def send_otp(email,otp):
    print(email)
    try:
        subject="OTP to verify your Email"
        emai_from=settings.EMAIL_HOST_USER
        recepient_list=[email,]
        htmlgen = f'Your OTP is {otp}.'
        send_mail(subject,htmlgen,emai_from,recepient_list, fail_silently=False)
    except Exception as e:
        print(e)
        return HttpResponse("Email failed to send with error: ",e)
    # return HttpResponse(o)
    return render(request,"verification.html",{"email":email})
