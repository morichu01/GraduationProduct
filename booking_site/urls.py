from django.urls import path
from . import views

app_name = "booking_site"
urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path('home/<int:pk>/', views.borrwDtail, name="books_detail"),
    path('home/<int:pk>/borrow', views.borrow, name='borrow'),
    path('home/<int:pk>/back/', views.back, name='back'),

    path("signup/", views.signup, name="signup"),
    path("users/<int:pk>/", views.UserDetailView.as_view(), name="users_detail"),
    path("users/<int:pk>/update/",
         views.UserUpdateView.as_view(), name="users_update"),
]
