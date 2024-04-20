from django.urls import path
from mainpage import views

app_name = 'mainpage'

urlpatterns = [
    path('',views.index),
    # path('detail/', views.detail,name='detail'),
    path('detail/<str:start>/<str:end>/', views.detail, name='detail'),
]
