from django.urls import path

from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('camera/cholesterol/', views.cholesterol_, name='cholesterol_'),
    path('camera/bilirubin/', views.bilirubin_, name='bilirubin_'),
    path('camera/catarct/', views.catarct_, name='catarct_'),
]
