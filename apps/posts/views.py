from django.contrib.auth.decorators import login_required 
from django.shortcuts import redirect, render, get_object_or_404
from .forms import PostModelForm
from .models import Post
from django.urls import reverse, reverse_lazy


login = reverse_lazy('login')

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
            form.save_m2m()
            return redirect(reverse('post-detail', kwargs={'post_id': obj.id}))
    else:   
        form = PostModelForm()

    template_name = 'posts/post_create.html'
    context = {'form': form}
    return render(request, template_name, context) 
