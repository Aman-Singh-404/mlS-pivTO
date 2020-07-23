from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import os

home = 'media'

# Create your views here.
@login_required
def account(request):
    uname = str(request.user)
    user = User.objects.get(username = uname)
    context = {
        "username" : uname,
        "firstname" : user.first_name,
        "lastname" : user.last_name,
        "email" : user.email,
        "password" : user.password,
        "login" : True,
        "dropdown" : False,
    }
    return render(request, 'account.html', context)

@login_required
def saveCredentails(request):
    uname = str(request.user)
    user = User.objects.get(username = uname)
    response = "Credentails saved."
    for key, value in request.POST.items():
        if key == "firstname":
            user.first_name = request.POST["firstname"]
        elif key == "lastname":
            user.last_name = request.POST["lastname"]
        elif key == "email":
            user.email = request.POST["email"]
    if request.POST.get('username') != None and request.POST.get('username') != uname:
        if not User.objects.filter(username = request.POST["username"]).exists():
            os.rename(os.path.join(home, uname), os.path.join(home, request.POST["username"]))
            user.username = request.POST["username"]
        else:
            response = "Username already exists."
    user.save()
    return HttpResponse(response)

@login_required
def savePassword(request):
    uname = str(request.user)
    user = User.objects.get(username = uname)
    if user.check_password(request.POST["old_password"]):
        user.set_password(request.POST["new_password"])
        user.save()
        return HttpResponse("Password changed.")
    else:
        return HttpResponse("Incorrect password.")
