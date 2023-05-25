from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login', views.LoginView.as_view(), name='login'), 
    path('logout', views.LogoutView.as_view(), name="logout"), 
    path('events', views.EventsView.as_view(), name="events"),
    path('about', views.AboutUsView.as_view(), name="aboutus"),
    path('products', views.ProductsView.as_view(), name="products"),
    path('services', views.ServicesView.as_view(), name="services"), 
    path('mail', views.MailView.as_view(), name="mail"), 
    path('household', views.HouseholdView.as_view(), name="household"),
    path('vegetables', views.VegitablesView.as_view(), name="vegetables"),
    path('single/<pk>', views.SingleView.as_view(), name="single"), 
    path('short-codes', views.ShortCodesView.as_view(), name="short_codes"), 
    path('privacy', views.PrivacyView.as_view(), name="privacy"), 
    path('kitchen', views.KitchenView.as_view(), name="kitchen"), 
    path('frozen', views.FrozenView.as_view(), name="frozen"), 
    path('faqs', views.FaqsView.as_view(), name="faqs"), 
    path('drinks', views.DrinksView.as_view(), name="drinks"), 
    path('bread', views.BreadView.as_view(), name="bread"), 
    path('pet', views.PetView.as_view(), name="pet"),
    path('all-products', views.AllProductsView.as_view(), name="all_products"),
    # path('add-to-cart', views.AddToCartView.as_view(), name="add_to_cart"),
    path('view-cart', views.viewCartView.as_view(), name="view_cart"),
    path('search', views.SearchView.as_view(), name="search")

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)