from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='dashboard-home'),
    path('posts/<int:post_id>/', views.post_detail_view, name='post-detail'),
    path('posts/new/', views.post_create_view, name='post-create'),
]
