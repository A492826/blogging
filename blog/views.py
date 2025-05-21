from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm
from .forms import ContactForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, PostForm
from .forms import SignUpForm
from django.http import HttpResponseForbidden


# Rename or alias 'my_view' to 'home'
def home(request):
    return render(request, 'blog/blog.html')  # This will act as your homepage


def my_view(request):
    return render(request, 'blog/blog.html')  # Assuming your template is in blog/templates/blog/blog.html

def posts(request):
    posts = Post.objects.all()
    return render(request, 'blog/post.html', {'posts': posts})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():   
            form.save()
            return redirect('contact')  # Optionally redirect or show a success message
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST) 
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()

    return render(request, 'blog/postdetails.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Automatically set current user
            post.save()
            return redirect('post_list')  # or any page
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # logged-in user
            post.save()
            return redirect('post_list')  # redirects to All Posts page
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()

    # Only the author can edit/delete
    if request.method == 'POST':
        if 'edit_post' in request.POST:
            if post.author != request.user:
                return HttpResponseForbidden("You cannot edit this post.")
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('post_detail', post_id=post.id)
        elif 'delete_post' in request.POST:
            if post.author != request.user:
                return HttpResponseForbidden("You cannot delete this post.")
            post.delete()
            return redirect('post_list')  # redirect after delete
        else:
            # Handle comments form submit or other POSTs
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.save()
                return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
        post_form = PostForm(instance=post)

    return render(request, 'blog/postdetails.html', {
        'post': post,
        'comments': comments,
        'form': form,         # comment form
        'post_form': post_form  # edit post form
    })


from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    print(f"Post author: {post.author}, Current user: {request.user}")
    if post.author.id != request.user.id:
        return HttpResponseForbidden("You cannot edit this post.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponseForbidden("You cannot delete this post.")

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    
    return render(request, 'blog/delete_post_confirm.html', {'post': post})



@login_required
def dashboard(request):
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')  # or your date field
    return render(request, 'blog/dashboard.html', {'posts': user_posts})