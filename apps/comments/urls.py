from django.urls import path
from . import views 


urlpatterns = [
    path('<int:post_id>/', views.comment_create_view, name='comment-create'),
]
