from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('reservations/', views.reservations, name="reservations"),
    path('menu-page/', views.menu, name="menu-page"),
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),  
    path('bookings', views.bookings, name='bookings'),
    path('menu/', views.MenuItemsView.as_view(), name="menu-list"),
    path('menu/<int:pk>/', views.SingleMenuItemView.as_view(), name="menu-detail"),
]
