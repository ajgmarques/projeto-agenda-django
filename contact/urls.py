from django.urls import path
from contact import views

app_name = 'contact'

urlpatterns = [
    # contact (CRUD)
    path('contact/<int:contact_id>/detail/', views.contact, name='contact'),
    path('contact/<int:contact_id>/update/', views.update, name='update'),
    path('contact/<int:contact_id>/delete/', views.delete, name='delete'),
    path('contact/create/', views.create, name='create'),  # para criar novo

    # user register
    path('user/create/', views.register, name='register'),
    # user login/logout
    path('user/login/', views.login_view, name='login'),
    path('user/logout/', views.logout_view, name='logout'),
    # user update
    path('user/update/', views.user_update, name='user_update'),

    path('search/', views.search, name='search'),
    path('', views.index, name='index'),
]
