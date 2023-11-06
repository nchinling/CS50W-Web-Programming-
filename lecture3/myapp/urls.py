#  Allow for rerouting
from django.urls import path

#  Allow import of functions from views.py
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("brian", views.brian, name="brian"),
    path("david", views.david, name="david"),
    path("<str:name>",views.greet, name="greet")

 ]