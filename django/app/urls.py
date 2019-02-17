from django.urls import path
from django.conf.urls import url

from . import views


urlpatterns = [
    #path('signup/', views.SignUp.as_view(), name='signup'),
    path('camera/cholesterol/', views.cholesterol_, name='cholesterol_'),
    path('camera/bilirubin/', views.bilirubin_, name='bilirubin_'),
    path('camera/cataract/', views.cataract_, name='cataract_'),
    path('home/', views.search_form),
    url(r'^signup/$', views.signup),
    url(r'^login/$', views.login),
    url(r'^aadhar/$', views.aadhar),
    url(r'^aadhar2/$', views.aadhar2),
    path('about/', views.search_form),
    path('contact/', views.search_form),
    path('direct_test/', views.direct_test),
    path('login_only/', views.search_form),
    path('diagnosis_registered/', views.search_form),
    path('notifyform/', views.search_form),
    path('genform/', views.search_form),
]