from django.urls import path
from . import views


urlpatterns = [
    path('<int:post_id>/', views.post_detail_view, name='post-detail'),
    path('new/', views.post_create_view, name='post-create'),
    path('<int:post_id>/update/', views.post_update_view, name='post-update'),
    path('my-posts/', views.post_user_list_view, name='post-user-list'),
]
