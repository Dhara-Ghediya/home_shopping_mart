from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, View, DetailView, UpdateView, CreateView, TemplateView
from .models import User
from django.http import HttpResponse

# Create your views here.
class HomeView(TemplateView):
    template_name = "index.html"

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        uname = request.POST.get('Username')
        password = request.POST.get('Password')
        obj = User.objects.filter(username=uname, password=password)
        if obj:
            request.session['login'] = uname
            return redirect('home')
        else:
            email = request.POST.get('Email')
            mobile = request.POST.get('Phone')
            user = User(username=uname, password=password, email=email, phone=mobile)
            user.save()
            return redirect('login')
    
        
# class UserCreateView(CreateView):
#     model = User
#     fields = ['username', 'password', 'email', 'phone']
#     template_name = 'login.html'
#     success_url = 'login'

class LogoutView(View):
    def get(self, request):
        request.session.flush()
        request.session.clear_expired()
        return redirect('home')