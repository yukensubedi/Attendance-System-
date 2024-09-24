from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserCreationForm, UserUpdateForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User
from django.contrib.auth import authenticate
from django.contrib import messages


class UserRegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('login') 
        return super().dispatch(request, *args, **kwargs)

   

class UserLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('attendance_report')  


    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            if user.is_verified:
                return super().form_valid(form)  # Allow login
            else:
                messages.error(self.request, 'Your account is not verified. Please contact administration')
                return self.form_invalid(form)  # Reject login
        else:
            messages.error(self.request, 'Invalid credentials.')
            return self.form_invalid(form)

    def get_success_url(self):
        return self.success_url or super().get_success_url()
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('update_user')   
        return super().dispatch(request, *args, **kwargs)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'update_user.html'
    success_url = reverse_lazy('update_user')  # Redirect after successful update

    def get_object(self, queryset=None):
        return self.request.user  # Update the logged-in user's data

class LogoutConfirmView(LoginRequiredMixin, TemplateView):

      template_name = 'logout.html'