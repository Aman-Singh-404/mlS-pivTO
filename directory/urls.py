from django.urls import path
from . import views

urlpatterns = [
    path("search/",views.searchPost, name="searchPost"),
    path("redo<path:path>",views.redoPost, name="redoPost"),
    path("undo<path:path>",views.undoPost, name="undoPost"),
    path("copy<path:source>",views.copyPost, name="copyPost"),
    path("move<path:source>",views.movePost, name="movePost"),
    path("paste<path:destination>",views.pastePost, name="pastePost"),
    path("rename<path:path>",views.renamePost, name="renamePost"),
    path("remove<path:path>",views.removePost, name="removePost"),
    path("newdir?=<path:path>",views.newPost, name="newPost"),
    path("newdir?=",views.newPost, name="newPost"),    
    path("upload<path:destination>",views.uploadPost, name="uploadPost"),
    path("upload",views.uploadPost, name="uploadPost"),
    path("<path:path>/", views.dispatch,name="directory"),
    path("",views.dispatch, name="directory"),
]