from django.contrib import admin
from django.urls import path,include
from .views import instagram_callback

urlpatterns = [
    path("auth/", view=instagram_callback, name="instagram_callback")
]