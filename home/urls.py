from django.contrib import admin
from django.urls import include, path

from home import views

urlpatterns = [
    path('', views.loginUser , name='login'),
    path('home/', views.home , name='home'),
    path('login/', views.loginUser, name='login'),
    path('add_contact/', views.addContact, name='add_contact'),
    path('edit_contact/<int:contact_id>/', views.editContact, name='edit_contact'),
    path('delete_contact/', views.deleteContact, name='delete_contact'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='password_reset_confirm'),
]
