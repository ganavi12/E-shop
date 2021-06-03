from . import views
from django.urls import path

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    # path("signup", views.signup, name="signup"),
    path("signup", views.Signup.as_view(), name="signup"),
    path("login", views.Login.as_view(), name="login"),
    path("logout", views.Logout.as_view(), name="logout"),
    path("cart",views.Cart.as_view(),name="cart"), 
]