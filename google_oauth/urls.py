from os import name
from django.urls import path
from . import views

app_name = "oauth"
urlpatterns = [
     path('login/', views.GoogleLogin.as_view(), name="login"),
     path('logout/', views.GoogleLogout.as_view(), name="logout"),
     path('sync-event/', views.GoogleSyncEvent.as_view(), name="sync")
]
