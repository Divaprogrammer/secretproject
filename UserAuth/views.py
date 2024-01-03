from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import ValidateUser
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages

import string
import random
from datetime import datetime, timedelta,timezone
from django.db.models import Q


# Restframe work
from rest_framework.views import APIView




class UserRegistration(APIView):
    def get(self, request):
        return render(request, "signup.html")

    def post(self, request):
        Name = request.POST.get("name",'')
        email = request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(Q(username=email) | Q(email=email)).exists():
            messages.success(request, 'Changes successfully saved.')
            return HttpResponseRedirect('/')

            # return render(request, "signup.html",{'error':'User already registered'})
        user = User.objects.create_user(
            username=email, first_name=Name, last_name=Name, email=email
        )
        user.set_password(password)
        user.save()
        return redirect("/")


class UserLogin(APIView):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")
        messages.error(request, 'Please recheck your user name and password.')
        return HttpResponseRedirect(request.path_info)


class UserLogout(APIView):
    def get(self, request):
        logout(request)
        return redirect('/')

class UserForgot(APIView):
    
    def get(self, request):
        return HttpResponse('Render the html')
    def post(self, request):
        UserObject=User.objects.get(username=request.POST.get('username'))
        email = UserObject.email
        temp_pass = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=8))
        if ValidateUser.objects.get(user=UserObject):
            ValidateUser.objects.get(user=UserObject).delete()
        SetOtp=ValidateUser(user=UserObject,otp=temp_pass)
        SetOtp.save()
        subject="Accounts verifications"
        email_from=settings.EMAIL_HOST_USER
        message=f"Here is the OTP {temp_pass}"
        send_mail(subject, message, email_from, [email])
        return HttpResponse("This is working")
    def put(self, request):
        username = request.POST.get('username')
        Newpassword= request.POST.get('password')
        if username:
            UserObject = User.objects.get(username = username)
            if UserObject:
                ValidateUserObject=ValidateUser.objects.get(user=UserObject)
                if ValidateUserObject.otp == request.POST.get('OTP'):
                    target_time=ValidateUserObject.created_at
                    current_time = datetime.utcnow().replace(tzinfo=timezone.utc)
                    time_difference = current_time - target_time
                    time_threshold = timedelta(minutes=5)
                    if time_difference < time_threshold:
                        UserObject.set_password(Newpassword)
                        ValidateUserObject.delete()
                        UserObject.save()
                        return HttpResponse('Password is reset')
                    return HttpResponse('Your OTP is expired')
                return HttpResponse ('Provided OTP is not correct')
            return HttpResponse ('Provided username is not correct')
        return HttpResponse('Please Provide a usename')
    
