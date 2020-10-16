from django.contrib.auth.decorators import login_required 
from django.shortcuts import redirect, render, get_object_or_404
from .forms import CommentModelForm
from .models import Comment 
from apps.posts.models import Post
from django.urls import reverse, reverse_lazy


login = reverse_lazy('login')

@login_required(login_url=login)
def comment_create_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentModelForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(reverse('post-detail', kwargs={'post_id': post.id}))
    else:   
        form = CommentModelForm()

    template_name = 'comments/comment.html'
    context = {'form': form}
    return render(request, template_name, context) 
