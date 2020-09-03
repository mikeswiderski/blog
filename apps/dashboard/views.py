from django.shortcuts import render
from apps.posts.models import Post
from django.core.paginator import Paginator


def home(request):
    post_list = Post.objects.all().order_by('-id')
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    template_name = 'dashboard/home.html'
    context = {
        'posts': posts 
    }
    return render(request, template_name, context)
