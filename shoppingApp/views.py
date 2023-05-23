from typing import Any, Optional
from django.db import models
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DeleteView, View, DetailView, UpdateView, CreateView, TemplateView
from .models import *
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Q
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

# inherit AddToCartView class into HouseholdView  
# class AddToCartView(View):
#     def post(self, request):
#         if 'login' in request.session.keys():    
#             user = request.session['login']
#             print("session key ", user)
#             id = request.POST.get('id')
#             product = Products.objects.get(id=id)
#             cart = AddToCart(user=user, product=product)
#             cart.save()
#             return HttpResponseRedirect(reverse(self.view))
#         else:
#             messages.info(request, "You are not login!")
#             return HttpResponseRedirect(reverse(self.view))

def addToCart(request, id):
    if 'login' in request.session.keys():    
        user = request.session['login']
        product = Products.objects.get(id=id)
        print("product", product)
        try:
            check = AddToCart.objects.get(user=user, product=product)
            if check:
                messages.info(request, "Product already added in Cart!")
        except: 
            cart = AddToCart(user=user, product=product)
            cart.save()
            messages.success(request, "Product added in Cart successfully!")
    else:
        messages.info(request, "You are not login!")

class viewCartView(ListView):
    model = AddToCart
    template_name = "viewCart.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'login' in self.request.session.keys():
            obj = AddToCart.objects.filter(user = self.request.session['login'])
            context["obj"] = obj 
            return context
        else:
            messages.warning(self.request, "You are not Login!")
    
        
class HouseholdView(ListView):
    model = Products
    template_name = "household.html"
    # view="HouseholdView"
    
    def post(self, request):
        id = request.POST.get('id')
        addToCart(request, id)
        return redirect('household')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cleaning = Products.objects.filter(product_type = "cleaning")
        utensils = Products.objects.filter(product_type = "utensils")
        context["cleaning"] = cleaning
        context['utensils'] = utensils
        return context
    
class VegitablesView(ListView):
    model = Products
    template_name = "vegetables.html"
    view="VegitablesView"
    
    def post(self, request):
        id = request.POST.get('id')
        addToCart(request, id)
        return redirect('vegetables')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = Products.objects.filter(Q(product_type = "Vegetables") | Q(product_type="Fruits"))
        context["obj"] = obj
        return context 

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
    model = Products
    template_name = "pet.html"
    
    def post(self, request):
        id = request.POST.get('id')
        addToCart(request, id)
        return redirect('pet')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = Products.objects.filter(product_type="Pet Food")
        context["obj"] = obj
        return context
    
    
class KitchenView (TemplateView):
    template_name = "kitchen.html"

class FrozenView (ListView):
    model = Products
    template_name = "frozen.html"
    
    def post(self, request):
        id = request.POST.get('id')
        addToCart(request, id)
        return redirect('frozen')
    
    # context_object_name="obj"                        or
    # by default in html page: object_list.example     or
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = Products.objects.filter(Q(product_type = "Frozen Nonvegs") | Q(product_type="Frozen Snacks"))
        context["obj"] = obj
        return context    
    
class FaqsView (TemplateView):
    template_name = "faqs.html"
    
class DrinksView (ListView):
    model = Products
    template_name = "drinks.html"
    
    def post(self, request):
        id = request.POST.get('id')
        addToCart(request, id)
        return redirect('drinks')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        soft_drinks = Products.objects.filter(product_type = "Soft Drinks")
        juices = Products.objects.filter(product_type = "juice")
        energy_drinks = Products.objects.filter(product_type = "Energy Drinks")
        context["soft_drinks"] = soft_drinks
        context["juices"] = juices
        context["energy_drinks"] = energy_drinks
        return context
    
class BreadView (ListView):
    model = Products
    template_name = "bread.html"
    
    def post(self, request):
        id = request.POST.get('id')
        addToCart(request, id)
        return redirect('bread')
    
    # context_object_name="obj"                        or
    # by default in html page: object_list.example     or
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p_type = "Bread & Bakery"
        obj = Products.objects.filter(product_type = p_type)
        context["obj"] = obj
        return context
    
class AllProductsView(ListView):
    model = Products
    template_name = "allProducts.html"
    
    def post(self, request):
        id = request.POST.get('id')
        print("idddd", id)
        addToCart(request, id)
        return redirect('all_products')