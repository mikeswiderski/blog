from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .forms import PostModelForm
from .models import Post
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator


login = reverse_lazy('login')


@login_required(login_url=login)
def post_user_list_view(request):
    post_list = Post.objects.filter(author=request.user)
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    template_name = 'posts/user_posts_list.html'
    context = {'posts': posts}
    return render(request, template_name, context)


def post_detail_view(request, post_id):
    obj = get_object_or_404(Post, id=post_id)
    template_name = 'posts/post_detail.html'
    context = {"object": obj}
    return render(request, template_name, context)


@login_required(login_url=login)
def post_create_view(request):
    if request.method == 'POST':
        form = PostModelForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            return redirect(reverse('post-detail', kwargs={'post_id': obj.id}))
    else:
        form = PostModelForm()

    template_name = 'posts/post_create.html'
    context = {'form': form}
    return render(request, template_name, context)


@login_required(login_url=login)
def post_update_view(request, post_id):
    obj = get_object_or_404(Post, id=post_id, author=request.user)
    form = PostModelForm(instance=obj)
    if request.method == 'POST':
        form = PostModelForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('post-detail', kwargs={'post_id': obj.id}))
    template_name = 'posts/post_update.html'
    context = {"form": form}
    return render(request, template_name, context)
