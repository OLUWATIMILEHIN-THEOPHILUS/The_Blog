from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:pk>/', views.post, name='post'),
    path('about', views.about, name='about'),

    path('sign-up/', views.sign_up, name='sign_up'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('sign-out/', views.sign_out, name='sign_out'),

    path('create-post/', views.create_post, name='create-post'),
    path('edit-post/<int:pk>/', views.edit_post, name='edit-post'),
    path('delete-post/<int:pk>/', views.delete_post, name='delete-post'),
    path('delete-comment/<int:pk>/', views.delete_comment, name='delete-comment'),
]
