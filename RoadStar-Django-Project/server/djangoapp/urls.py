from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("dealer/<int:dealer_id>", views.dealer_detail, name="dealer_detail"),
    path("review/<int:dealer_id>", views.review_dealer, name="review_dealer"),

    path("djangoapp/get_dealers", views.api_get_dealers, name="api_get_dealers"),
    path("djangoapp/dealer/<int:dealer_id>", views.api_get_dealer, name="api_get_dealer"),
    path("djangoapp/reviews/dealer/<int:dealer_id>", views.api_get_dealer_reviews, name="api_get_dealer_reviews"),
    path("djangoapp/get_cars", views.api_get_cars, name="api_get_cars"),
    path("djangoapp/analyze/<str:text>", views.api_analyze, name="api_analyze"),
    path("djangoapp/login", views.api_login, name="api_login"),
    path("djangoapp/logout", views.api_logout, name="api_logout"),
    path("djangoapp/register", views.api_register, name="api_register"),
]
