from django.urls import path

from authentication import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('signup', views.signup_page, name='signup'),
    path('logout', views.logout_view, name='logout'),
]
