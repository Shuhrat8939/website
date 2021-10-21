from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.LoginView, name='login'),
    path('register/', views.RegisterView, name='register'),
    path('checkout/', views.CheckoutView, name='checkout'),
    path('menu', views.menu, name='menu'),
    path('menu/<int:post_id>', views.show_product, name='post'),
    path('news', views.news, name='news'),
    path('news/<int:shownews_id>', views.show_news, name='shownews'),
    path('about', views.about, name='about'),
    path('sales', views.sales, name='sales'),
    path('sales/<int:sale_id>', views.show_sales, name='sale'),
    path('delivery', views.delivery, name='delivery'),
    path('contacts', views.contacts, name='contacts')
]
