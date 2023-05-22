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
    
class EventsView(TemplateView):
    template_name = "events.html"
    
class AboutUsView(TemplateView):
    template_name = "about.html"
    
class ProductsView(TemplateView):
    template_name = "products.html"
    
class ServicesView(TemplateView):
    template_name = "services.html"
    
class MailView(TemplateView):
    template_name = "mail.html"
    
class HouseholdView(TemplateView):
    template_name = "household.html"
    
class VegitablesView(TemplateView):
    template_name = "vegetables.html"
    
class SingleView(TemplateView):
    template_name = "single.html"
    
class ShortCodesView(TemplateView):
    template_name = "short-codes.html"
    
class PrivacyView(TemplateView):
    template_name = "privacy.html"
    
class PetView(TemplateView):
    template_name = "pet.html"
    
class KitchenView (TemplateView):
    template_name = "kitchen.html"
    
class FrozenView (TemplateView):
    template_name = "frozen.html"
    
class FaqsView (TemplateView):
    template_name = "faqs.html"
    
class DrinksView (TemplateView):
    template_name = "drinks.html"
    
class BreadView (TemplateView):
    template_name = "bread.html"