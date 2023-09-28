from django.urls import path
from . import views

urlpatterns = [
    path('test_fibonacci/', views.fib_test, name='fib_test')
]
