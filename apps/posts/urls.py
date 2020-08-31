from django.urls import path
from . import views 

urlpatterns = [
    path('<int:post_id>/', views.post_detail_view, name='post-detail'),
    path('new/', views.post_create_view, name='post-create'),
]
