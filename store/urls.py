from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'store'
urlpatterns = [
    path('cart/', views.basket, name="basket"),
    path('thankyou/', views.thanks, name="thanks"),
    path('cancel/', views.cancel, name="cancel"),
    path('checkout/', views.create_checkout_session, name="create_checkout_session"),
    path('authentication/', views.authentication, name="authentication"),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('specialeditions/', views.special, name="special"),
    path('privacy-policy/', views.privacy, name="privacy"),
    path('terms&conditions/', views.terms_conditions, name="terms_conditions"),
    path("logout/", views.logout_request, name= "logout_request"),
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('<slug:club_name>/<str:season>/<str:type>/', views.product_detail, name='product_detail'),
    path('<str:club_name>/', views.team, name="team"),
    path('league/<str:categorie>/', views.categories, name="categories"),
    
    

    path("", views.home, name="home"),
    
    
]

