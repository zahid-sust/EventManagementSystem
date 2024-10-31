from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('events/', views.event_list, name='event_list'),
    path('create/', views.create_event, name='create_event'),
    path('search/', views.search_events, name='search_events'),  
    path('book/<int:event_id>/', views.book_event, name='book_event'),
    path('create/', views.create_event, name='create_event'),
    path('update/<int:event_id>/', views.update_event, name='update_event'),
    path('delete/<int:event_id>/', views.delete_event, name='delete_event'),
]
