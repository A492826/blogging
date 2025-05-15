from django.urls import path, include  # ✅ Correct import
from . import views

urlpatterns = [
    path('', views.my_view, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('postdetails/', views.postdetails, name='postdetails'),

    path('about/', views.about, name='about'),
    
]
