from django.urls import path
from . import views
from django.shortcuts import redirect

app_name='myproject.scanner'
urlpatterns = [
      path('', views.index, name='index'),
      path('about/', views.about, name='name_about'),
      path('fa/', views.fa, name='name_fa'),
      path('api/', views.api, name='name_api'),
      path('terms/', views.terms, name='name_terms'),
      path('docs/', views.docs, name='name_docs'),
      path('grade/', views.grade, name='name_grade'),
]
