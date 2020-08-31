from django.shortcuts import render
from apps.posts.models import Post


def home(request):
    template_name = 'dashboard/home.html'
    context = {
        'posts': Post.objects.all() 
    }
    return render(request, template_name, context)
