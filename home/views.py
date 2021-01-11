import os
import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.password_validation import validate_password
from user.models import UserProfile

home = "media"
message = ""
display = "none"

# Create your views here.
def passwordValidation(request):
    if request.body.decode('utf-8') == "":
        return Http404("False Value")
    try:
        validate_password(request.body.decode('utf-8'))
        return HttpResponse("true")
    except Exception as e:
        return HttpResponse(e)


def createUserID(fname, lname):
    value = str(random.randrange(999999))
    numberID = "".join("0" for i in range(6-len(value))) + value
    if lname == "":
        i, j, k = random.randrange(0, len(fname), 3), random.randrange(0, len(fname), 3), random.randrange(0, len(fname), 3)
        return fname[i] + fname[j] + fname[k] + numberID
    else:
        i, j, k = random.randrange(0, len(fname), 3), random.randrange(0, len(lname), 3), random.randrange(0, len(fname), 3)
        return fname[i] + lname[j] + fname[k] + numberID

def homepage(request):
    uname = str(request.user)
    context = {
        "login" : False,
        "message" : message,
        "display" : display,
        "dropdown" : False,
    }
    if uname != "AnonymousUser":
        context["login"] = True
    return render(request, "homepage.html", context)


def createAccount(request):
    uname = str(request.user)
    if uname == "AnonymousUser":
        return render(request, "signup.html", {})
    else:
        return HttpResponseRedirect(reverse("homepage"))


def signup(request):
    if request.POST["name"] == "" or request.POST["password"] == "" or request.POST["email"] == "" or request.POST["phone"] == "" or request.POST["gender"] == "":
        return Http404("False Value")
    first_name = ""
    last_name = ""
    name = request.POST["name"].split(" ", 1)
    if len(name) == 2:
        first_name = name[0]
        last_name = name[1]
    else:
        first_name = name[0]
        last_name = ""
    password = request.POST["password"]
    email = request.POST["email"]
    username = createUserID(first_name, last_name)
    new_user = User.objects.create_user(username, email, password)
    new_user.first_name = first_name
    new_user.last_name = last_name
    new_user.save()
    CustomUser(user = new_user, phone = request.POST["phone"], gender = request.POST["gender"]).save()
    login(request, new_user)
    os.mkdir(os.path.join("media", username))
    os.mkdir(os.path.join("media", username + "@BIN"))
    if request.POST["next"] != "":
        return HttpResponseRedirect(request.POST["next"])
    return HttpResponseRedirect(reverse("directory"))


def userlogin(request):
    if request.POST["email"] == "" or request.POST["psw"] == "":
        return Http404("False Value")
    global message, display
    email = request.POST["email"]
    password = request.POST["psw"]
    if not User.objects.filter(email = email).exists():
        message = "Email ID is incorrect!"
        display = "block"
        return HttpResponseRedirect(reverse("homepage"))
    elif not User.objects.get(email = email).check_password(password):
        message = "Password is incorrect!"
        display = "block"
        return HttpResponseRedirect(reverse("homepage"))
    user = authenticate(username = User.objects.get(email = email).username, password = password)
    if not os.path.exists(os.path.join(home, user.username)):
        os.mkdir(os.path.join(home, user.username))
    login(request, user)
    message = ""
    display = ""
    if request.POST["next"] != "":
        return HttpResponseRedirect(request.POST["next"])
    return HttpResponseRedirect(reverse("directory"))


def userlogout(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))
