from django.urls import path
from . import views

app_name = "oauth"
urlpatterns = [
     path('login/', views.GoogleLogin.as_view(), name="google_login")
]
