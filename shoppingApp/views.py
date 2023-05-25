from typing import Any, Optional
from django.db import models
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DeleteView, View, DetailView, UpdateView, CreateView, TemplateView
from .models import *
from django.urls import reverse
import json
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Q

# **************** To ignore content between () ******************
def getName(value):
    name=""
    for i in value:
        if i == "(":
            break
        name+=i
    return name

# **************** Function for Add to Cart Products ******************
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
  
# **************** Function for Count Price after discount and count average ******************      
def disc(request, amount):
    for i in amount:
        i.disc = i.price - i.discount_amount
        i.avg = int(100-((i.disc/i.price)*100))
    return amount

# **************** Home Page ******************
class HomeView(ListView):
    model = Products
    template_name = "index.html"
    
    def post(self, request):
        id = request.POST.get('id')
        addToCart(request, id)
        return redirect('home')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = Products.objects.all()
        offer = obj.order_by('-discount_amount')
        disc(self.request, offer)
        context["offer"] = offer[:4]
        return context

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
        request.session.pop('login')
        # request.session.clear_expired()
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


# **************** For View Cart ******************
class viewCartView(ListView):
    model = AddToCart
    template_name = "viewCart.html"
    
    def post(self, request):
        user = self.request.session.get('login')
        name = Products.objects.get(Product_name=request.POST.get('p_name'))
        obj = AddToCart.objects.filter(user=user, product=name)
        obj.delete()
        return redirect('view_cart')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'login' in self.request.session.keys():
            obj = AddToCart.objects.filter(user = self.request.session['login'])
            context["obj"] = obj 
            return context
        else:
            messages.warning(self.request, "You are not Login!")
    
# **************** Filtered Products for Household's Products ******************        
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
        disc(self.request, cleaning)
        utensils = Products.objects.filter(product_type = "utensils")
        disc(self.request, utensils)
        context = {
            "cleaning": cleaning,
            "utensils": utensils
        }
        return context

# **************** Filtered Products for Vegitables and Fruits's Products ******************     
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
        disc(self.request, obj)
        context["obj"] = obj
        return context 

# **************** Single Product View ****************** 
class SingleView(DetailView):
    model = Products
    template_name = "single.html"
    # context_object_name="obj"                      or
    # by default in html page: object_list.example     

class ShortCodesView(TemplateView):
    template_name = "short-codes.html"
    
class PrivacyView(TemplateView):
    template_name = "privacy.html"

# **************** Filtered Products for Pet's Products ******************     
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
        disc(self.request, obj)
        context["obj"] = obj
        return context
    
    
class KitchenView (TemplateView):
    template_name = "kitchen.html"

# **************** Filtered Products for Frozen's Products ****************** 
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
        disc(self.request, obj)
        context["obj"] = obj
        return context    
    
class FaqsView (TemplateView):
    template_name = "faqs.html"

# **************** Filtered Products for Drink's Products ******************     
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
        disc(self.request, soft_drinks)
        juices = Products.objects.filter(product_type = "juice")
        disc(self.request, juices)
        energy_drinks = Products.objects.filter(product_type = "Energy Drinks")
        disc(self.request, energy_drinks)
        context = {
            "soft_drinks": soft_drinks,
            "juices": juices,
            "energy_drinks": energy_drinks
        }
        return context

# **************** Filtered Products for Bread & Bakery's Products ******************     
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
        disc(self.request, obj)
        context["obj"] = obj
        return context

# **************** All Products List with Hot Offer Products  ******************     
class AllProductsView(ListView):
    model = Products
    template_name = "allProducts.html"
    
    def post(self, request):
        id = request.POST.get('id')
        addToCart(request, id)
        return redirect('all_products')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["listOfProducts"] =[getName(x.Product_name) for x in Products.objects.all()]    
        sort_option = self.request.GET.get('sortby')
        obj = Products.objects.all()
        offer = obj.order_by('-discount_amount')
        disc(self.request, offer)
        context["offer"] = offer[:4]
        disc(self.request, obj)
        if sort_option == "htolprice":
            obj = obj.order_by('-price')
            disc(self.request, obj)
        elif sort_option == "ltohprice":
            obj = obj.order_by('price')
            disc(self.request, obj)
        elif sort_option == "offer":
            obj = obj.order_by('-discount_amount')
            disc(self.request, obj)
        elif sort_option == "asc":
            obj = obj.order_by('Product_name')
            disc(self.request, obj)
        elif sort_option == "desc":
            obj = obj.order_by('-Product_name')
            disc(self.request, obj)
        context["obj"] = obj
        
        return context

# **************** Filtered Products Using Search Bar ******************         
class SearchView(ListView):
    model = Products
    template_name = "search.html"
    context_object_name = "obj"
    
    # def get(self, request, *args, **kwargs):
    #     return super.get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        # context = self.get_context_data(**kwargs)
        search_query = request.POST.get("Product")
        search_results = Products.objects.filter(Product_name__icontains = search_query)
        context = {
            "search_query": search_query,
            "search_results": search_results,
        }
        return render(request, self.template_name, context)
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     obj = Products.objects.all()
    #     context["obj"] = obj
    #     return context
    
    


#################################### extra.............
# class indexView(ListView):
#     model = hotels
#     template_name = 'home.html'
#     context_object_name = 'hotels'

#     def get_queryset(self):
#         form = searchCityHotelForm(self.request.GET)
#         queryset = super().get_queryset()

#         if form.is_valid():
#             name = form.cleaned_data.get('name')
#             city = form.cleaned_data.get('city')
#             # Apply filters based on form data
#             if name:
#                 queryset = queryset.filter(name__icontains=name)
#             if city:
                
#                 queryset = queryset.filter(city__name__icontains=city)
#         return queryset

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         city_list = citys.objects.all()
#         hotel_list = hotels.objects.all()
#         context['cityList'] = [city.name for city in city_list]
#         context['hotelnames'] = [hotel.name for hotel in hotel_list]
#         context['form'] = searchCityHotelForm(self.request.GET)

#         return context
