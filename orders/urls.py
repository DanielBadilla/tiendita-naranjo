from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order, name='order'),
    path('leave_review/', views.leave_review, name='leave_review'),
]