import os
import shutil
import filetype
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from .models import Actions, Erased
import json

home = settings.MEDIA_ROOT
domain = "http://127.0.0.1:8000/dirmode/"



class DIRECTORY_DATA:

    def get_Details(self, path):
        fname = []
        for f in sorted(os.listdir(path)):
            ftype = self.get_Type(os.path.join(path, f))
            size = self.get_Size(os.path.join(path, f))
            fname.append({ "name" : f, "size" : size, "type" : ftype })
        return fname

    def get_Size(self, path):
        total = 0
        if os.path.isfile(path):
            return os.path.getsize(path)
        for dirlist in os.listdir(path):
            if os.path.isdir(os.path.join(path, dirlist)):
                total += self.get_Size(os.path.join(path, dirlist))
            else:
                total += os.path.getsize(os.path.join(path, dirlist))
        return total

    def get_Type(self, path):
        ftype = None
        if os.path.isdir(path):
            ftype = "Folder"
        else:
            ftype = filetype.guess(path)
            if ftype == None:
                ftype = (os.path.splitext(path)[-1][1:]).capitalize()
                if ftype == "":
                    ftype = "Unknown"
            else:
                ftype = ftype.mime.capitalize()
        return ftype

    def find(self, name, location):
        folderlist = []
        for directory in os.listdir(location):
            if directory.find(name) > -1:
                folderlist.append(os.path.join(location, directory))
            if os.path.isdir(os.path.join(location, directory)):
                folderlist += self.find(name, os.path.join(location, directory))
        return folderlist
    
    def opendirectory(self,user,path):
        if path != "":
            parent = []
            a = path
            while True:
                a, b = os.path.split(a)
                parent.insert(0, b)
                if a == "":
                    break
            parentlink = []
            link = ""
            for par in parent:
                link += par + "/"
                parentlink.append((reverse("directory") + link, par))
        else:
            parentlink = []
        context = {
            "disable" : "",
            "search" : "",
            "parentlink" : parentlink,
            "parentall" : path,
            "directories" : self.get_Details(os.path.join(home, user, path)),
            "dropdown" : True,
            "login" : True,
        }
        return context
    
    def openfile(self, path):
        ftype = self.get_Type(os.path.join(home, path))
        context = {
            "disable" : "disabled",
            "type" : ftype,
            "search" : "",
            "src" : settings.MEDIA_URL + path,
        }
        return context

dirobj=DIRECTORY_DATA()

@login_required
def dispatch(request, path = ""):
    uname = str(request.user)
    if os.path.isdir(os.path.join(home, uname, path)):
        context = dirobj.opendirectory(uname, path)
        return render(request, "Folder.html", context)
    elif os.path.isfile(os.path.join(home, uname, path)):
        context = dirobj.openfile(os.path.join(uname, path))
        return render(request, "File.html", context)
    else:
        raise Http404("Folder does not exist.")

@login_required
def searchPost(request):
    base = os.path.join(home, str(request.user), "")
    name = request.POST["search"]
    dirlist = dirobj.find(name, base)
    fname = []
    for f in sorted(dirlist):
        ftype = dirobj.get_Type(f)
        size = dirobj.get_Size(f)
        fname.append({"name": f.replace(base,""), "size": size, "type": ftype})
    context = {
        "disable": "disabled",
        "search": name,
        "parentlink": "",
        "parentall": "",
        "directories": fname,
    }
    return render(request, "Folder.html", context)

def rollback():
    Erased.objects.all().delete()
    for act in Actions.objects.all().order_by("-pk"):
        if act.action == "copy" or act.action == "move":
            act.delete()
        else:
            break


def redoPost(request, path):
    erd = Erased.objects.all().order_by("-pk")
    if not erd:
        return HttpResponseRedirect(domain + path)
    erd = erd[0]
    if erd.action == "paste":
        destination = erd.path
        for rerd in Erased.objects.all().order_by("-pk")[1:]:
            if rerd.action == "copy":
                if os.path.isdir(rerd.path):
                    if not os.path.split(rerd.path)[-1] in os.listdir(destination):
                        shutil.copytree(rerd.path, destination + os.path.split(rerd.path)[-1])
                else:
                    shutil.copy(rerd.path, destination)
            elif rerd.action == "move":
                if os.path.isdir(rerd.path):
                    if not os.path.split(rerd.path)[-1] in os.listdir(destination):
                        shutil.copytree(rerd.path, destination + os.path.split(rerd.path)[-1])
                    if not rerd.path == destination:
                        shutil.rmtree(rerd.path)
                else:
                    if os.path.split(rerd.path)[-1] in os.listdir(destination) and not(rerd.path == destination):
                        os.remove(act.path)
                    else:
                        shutil.move(rerd.path, destination)
            else:
                break
            act = Actions()
            act.action = rerd.action
            act.path = rerd.path
            act.save()
            rerd.delete()
        act = Actions()
        act.action = erd.action
        act.path = erd.path
        act.save()
        erd.delete()
    elif erd.action == "rename":
        old, new = erd.path.split("@#$#@")
        os.rename(old, os.path.split(old)[0]+ "/" + new)
        act = Actions()
        act.action = erd.action
        act.path = erd.path
        act.save()
        erd.delete()
    elif erd.action == "remove":
        if os.path.isdir(erd.path):
            if not os.path.split(erd.path)[-1] in os.listdir(user+'@BIN'):
                shutil.copytree(erd.path, user+'@BIN' + os.path.split(erd.path)[-1])
            shutil.rmtree(erd.path)
        else:
            shutil.move(erd.path, user+'@BIN')
        act = Actions()
        act.action = erd.action
        act.path = erd.path
        act.save()
        erd.delete()
    elif erd.action == "upload":
        shutil.copy(user+'@BIN' + os.path.split(erd.path)[-1], erd.path)
        act = Actions()
        act.action = erd.action
        act.path = erd.path
        act.save()
        erd.delete()
    elif erd.action == "new":
        if not os.path.exists(erd.path):
            os.mkdir(erd.path)
        act = Actions()
        act.action = erd.action
        act.path = erd.path
        act.save()
        erd.delete()
    return HttpResponseRedirect(domain + path)


def undoPost(request, path):
    act = Actions.objects.all().order_by("-pk")
    if not act:
        return HttpResponseRedirect(domain + path) 
    act = act[0]
    if act.action == "paste":
        destination = act.path
        for ract in Actions.objects.all().order_by("-pk")[1:]:
            if ract.action == "copy":
                if os.path.isdir(ract.path):
                    shutil.rmtree(destination + os.path.split(ract.path)[-1])
                else:
                    os.remove(destination + os.path.split(ract.path)[-1])
            elif ract.action == "move":
                if os.path.isdir(ract.path):
                    shutil.copytree(destination + os.path.split(ract.path)[-1], ract.path)
                    shutil.rmtree(destination + os.path.split(ract.path)[-1])
                else:
                    shutil.move(destination + os.path.split(ract.path)[-1], ract.path)
            else:
                break
            erd = Erased()
            erd.action = ract.action
            erd.path = ract.path
            erd.save()
            ract.delete()
        erd = Erased()
        erd.action = act.action
        erd.path = act.path
        erd.save()
        act.delete()
    elif act.action == "rename":
        old, new = act.path.split("@#$#@")
        os.rename(os.path.split(old)[0]+ "/" + new, old)
        erd = Erased()
        erd.action = act.action
        erd.path = act.path
        erd.save()
        act.delete()
    elif act.action == "new":
        shutil.rmtree(act.path)
        erd = Erased()
        erd.action = act.action
        erd.path = act.path
        erd.save()
        act.delete()
    elif act.action == "upload":
        shutil.move(act.path, user+'@BIN')
        erd = Erased()
        erd.action = act.action
        erd.path = act.path
        erd.save()
        act.delete()
    elif act.action == "remove":
        if os.path.isdir(act.path):
            if not os.path.exists(act.path):
                shutil.copytree(user+'@BIN' + os.path.split(act.path)[-1], act.path)
        else:
            shutil.copy(user+'@BIN' + os.path.split(act.path)[-1], act.path)
        erd = Erased()
        erd.action = act.action
        erd.path = act.path
        erd.save()
        act.delete()
    return HttpResponseRedirect(domain + path)


def copyPost(request, source):
    rollback()
    for path in request.POST["copy"].split("@#$#@")[:-1]:
        act = Actions()
        act.action = "copy"
        act.path = path
        act.save()
    return HttpResponseRedirect(domain + source)


def movePost(request, source):
    rollback()
    for path in request.POST["move"].split("@#$#@")[:-1]:
        act = Actions()
        act.action = "move"
        act.path = path
        act.save()
    return HttpResponseRedirect(domain + source)


def pastePost(request, destination):
    Erased.objects.all().delete()
    flag = False
    for act in Actions.objects.all().order_by("-pk"):
        if act.action == "copy":
            if os.path.isdir(act.path):
                if not os.path.split(act.path)[-1] in os.listdir(destination):
                    shutil.copytree(act.path, destination + os.path.split(act.path)[-1])
            else:
                if not act.path == destination:
                    shutil.copy(act.path, destination)
            flag=True
        elif act.action == "move":           
            if os.path.isdir(act.path):
                if not os.path.split(act.path)[-1] in os.listdir(destination):
                    shutil.copytree(act.path, destination + os.path.split(act.path)[-1])
                if not act.path == destination:
                    shutil.rmtree(act.path)
            else:
                if os.path.split(act.path)[-1] in os.listdir(destination) and not(act.path == destination):
                    os.remove(act.path)
                else:
                    shutil.move(act.path, destination)
            flag=True
        else:
            break
    if flag:
        act = Actions()
        act.action = "paste"
        act.path = destination
        act.save()
    return HttpResponseRedirect(domain+destination)


def renamePost(request, path):
    rollback()
    old,new = request.POST["rename"].split('@#$#@')
    os.rename(os.path.join(home,user,path,old), os.path.join(home,user,path,new))
    act = Actions()
    act.action = "rename"
    act.path = request.POST["rename"]
    act.save()
    return HttpResponseRedirect(domain + path)


def removePost(request, path):
    rollback()
    opath=path
    trash=os.path.join(home,user+'@BIN')
    path=os.path.join(home,user,path)
    for rpath in request.POST["remove"].split("@#$#@")[:-1]:
        wrpath=os.path.join(path,rpath)
        if os.path.isdir(wrpath):
            if not rpath in os.listdir(trash):
                shutil.copytree(wrpath, os.path.join(trash,rpath))
            shutil.rmtree(wrpath)
        else:
            shutil.move(wrpath, trash)
        act = Actions()
        act.action = "remove"
        act.path = wrpath
        act.save()
    return HttpResponseRedirect(domain + opath)


def newPost(request, path = ""):
    #rollback()
    uname = str(request.user)
    os.mkdir(os.path.join(home, uname, path, request.body.decode('utf-8')))
    act = Actions()
    act.action = "new"
    act.path = os.path.join(home, uname, path, request.body.decode('utf-8'))
    act.save()
    return HttpResponse('')


def uploadPost(request, destination = ""):
    #rollback()
    uname = str(request.user)
    print('pppppppppppp',request.FILES['upload'])
    myfile = request.FILES['upload']
    fs = FileSystemStorage(location=os.path.join(home, uname, destination))
    filename = fs.save(myfile.name, myfile)
    act = Actions()
    act.action = "upload"
    act.path = destination + myfile.name
    act.save()
    context={
        'filetype': ''
    }
    return HttpResponse(json.dumps(context), content_type="application/json")
