from django.urls import path
from . import views 


urlpatterns = [
    path('<int:post_id>/', views.comment_create_view, name='comment-create'),
    path('<int:post_id>/all/', views.comment_list_view, name='comment-all'),
]
