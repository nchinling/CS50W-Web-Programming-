
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"), 
    path("new_post", views.new_post, name="new_post"), 
    path("profile/<int:id>", views.profile, name="profile"), 
    path("follow", views.follow, name="follow"), 
    path("unfollow", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("add_like/<int:post_id>", views.add_like, name="add_like"),
    path("delete_like/<int:post_id>", views.delete_like, name="delete_like"),

]
