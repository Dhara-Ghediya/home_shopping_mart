from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DeleteView, View, DetailView, UpdateView, CreateView, TemplateView
from .models import *
from django.http import HttpResponse

# Create your views here.
# **************** Home Page ******************
class HomeView(TemplateView):
    template_name = "index.html"

# **************** For User Sign-in & Sign-Up ******************
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

# **************** For User Sign-out ******************
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

class SingleView(DetailView):
    model = Products
    template_name = "single.html"
    # context_object_name="obj"                      or
    # by default in html page: object_list.example     

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
    
class BreadView (ListView):
    model = Products
    template_name = "bread.html"
    # context_object_name="obj"                        or
    # by default in html page: object_list.example     or
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p_type = "Bread & Bakery"
        obj = Products.objects.filter(product_type = p_type)
        context["obj"] = obj
        return context