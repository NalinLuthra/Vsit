from django.urls import path
from django.conf.urls import url

from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('camera/cholesterol/', views.cholesterol_, name='cholesterol_'),
    path('camera/bilirubin/', views.bilirubin_, name='bilirubin_'),
    path('camera/catarct/', views.catarct_, name='catarct_'),
    path('search-form/', views.search_form),
    url(r'^search/$', views.search),
]