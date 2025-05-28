from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.ad_list, name='ad_list'),
    path('create/', views.ad_create, name='ad_create'),
    path('edit/<int:ad_id>/', views.ad_edit, name='ad_edit'),
    path('delete/<int:ad_id>/', views.ad_delete, name='ad_delete'),
    path('proposal/to/<int:ad_id>/', views.create_proposal, name='create_proposal'),
    path('proposals/', views.proposal_list, name='proposal_list'),
    path('proposal/<int:proposal_id>/set/<str:status>/', views.update_proposal_status, name='update_proposal_status'),
    path('login/', auth_views.LoginView.as_view(template_name='ads/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    
]
