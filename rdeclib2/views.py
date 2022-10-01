from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from dashboard.models import faculty
from rdeclib2.forms import *


def home(request):
    return render(request,"home.html")

def register(request):
    if request.method=="POST":
        f = faculty()
        f.Username=request.POST["Username"]
        f.Name=request.POST["Name"]
        f.Email=request.POST["Email"]
        f.Password=request.POST["Password"]
        confirmpassword=request.POST["confirmpassword"]
        if(confirmpassword!=f.Password):
            return HttpResponse("Password is not confirmed")
        
        f.Branch = request.POST["Branch"]
        f.Designation = request.POST["Designation"]
        if "Faculty_image" in request.FILES:
            f.Faculty_image = request.FILES["Faculty_image"]
        myuser = User.objects.create_user(f.Username,f.Email,f.Password)
        myuser.save()
        f.customuser = myuser
        f.save()
        # form = FacultyForm(request.POST, request.FILES)
        # if form.is_valid():
        #     form.save()
        messages.success(request,"Wait till your identity confirm")
        return redirect("/login/")
    return render(request,"pages-register.html")

def handlelogin(request):
    if request.user.username in request.session:
        return redirect("/clgsite/")
    if request.method=="POST":
        loginusername=request.POST["username"]
        loginpassword=request.POST["password"]
        user=authenticate(username=loginusername,password=loginpassword)
        userfaculty = faculty.objects.filter(Username = loginusername).get()
        print(userfaculty is not None)
        # print(user.faculty)
        if (userfaculty.Confirm == False):
            print("You are not allowed")
        if request.POST.get("remember")=="true":
            request.session["loginusername"]=loginpassword
        if user is not None:
            login(request,user)
            return redirect("/clgsite/")
        else:
            return HttpResponse("Invalid Credentials")
    return render(request,"pages-login.html")
def handlelogout(request):
    logout(request)
    return redirect("/")


