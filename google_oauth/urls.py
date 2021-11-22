from os import name
from django.urls import path
from . import views

app_name = "oauth"
urlpatterns = [
     path('login/', views.GoogleLogin, name="login"),
     path('login/success/', views.GoogleLoginSuccess.as_view(), name="success"),
     path('logout/', views.GoogleLogout.as_view(), name="logout"),
     path('sync-event/', views.GoogleSyncEvent.as_view(), name="sync")
]
