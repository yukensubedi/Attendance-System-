from django.urls import path
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from .views import (
    UserRegisterView, 
    UserLoginView, 
    UserUpdateView, 
    LogoutConfirmView
    )

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),   
    path('login/', UserLoginView.as_view(), name='login'),          
    path('update/', UserUpdateView.as_view(), name='update_user'),  
    path('logout-confirm/', LogoutConfirmView.as_view(), name='logout-confirm'),

     path('logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
]
