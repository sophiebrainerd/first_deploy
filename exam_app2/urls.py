from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('success', views.success),
    path('quotes', views.all_quotes),
    path('quotes/<int:quoteid>', views.quote_page),
    path('users/<int:userid>', views.user_page),
    path('favorite', views.favorite),
    path('remove', views.remove),
    path('delete/<int:quoteid>', views.delete),
    path('add_quote', views.add_quote),
    path('edit/<int:quoteid>', views.edit)
]