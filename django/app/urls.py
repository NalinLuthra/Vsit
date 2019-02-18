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
    path('login/', views.login),
    url(r'^aadhar/$', views.aadhar),
    url(r'^aadhar2/$', views.aadhar2),
    path('about/', views.about),
    path('contact/', views.contact),
    path('login_only_redirect/', views.login_only_redirect),
    path('direct_test/', views.direct_test),
    path('diagnosis_registered/', views.diagnosis_registered),
    path('notifyform/', views.notifyform),
    path('notifyformexec/', views.notifyformexec),
    path('genform/', views.genform),
]