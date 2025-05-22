from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Post, Comment, Category, Tag, ContactMessage
from .forms import CommentForm, ContactForm, PostForm, SignUpForm

def home(request):
    """Homepage view showing featured/latest posts"""
    featured_posts = Post.objects.filter(status='published').select_related(
        'author', 'category'
    ).prefetch_related('tags').order_by('-created_at')[:3]
    return render(request, 'blog/blog.html', {'featured_posts': featured_posts})

def post_list(request):
    """List all published posts with pagination"""
    post_list = Post.objects.filter(status='published').select_related(
        'author', 'category'
    ).prefetch_related('tags').order_by('-created_at')
    paginator = Paginator(post_list, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})

def about(request):
    """Static about page"""
    return render(request, 'blog/about.html')

def contact(request):
    """Handle contact form submissions"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})

def post_detail(request, post_id):
    """Show post details and handle comments"""
    post = get_object_or_404(
        Post.objects.select_related('author', 'category').prefetch_related('tags'),
        id=post_id,
        status='published'
    )
    comments = post.comments.filter(active=True).select_related('post')
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(request, 'Your comment has been submitted and is awaiting moderation.')
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

def signup(request):
    """User registration view"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form})

@login_required
def create_post(request):
    """Create new blog post"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save many-to-many relationships (tags)
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', post_id=post.id)
        else:
            messages.error(request, 'Form is invalid. Please correct the errors.')
            print(form.errors)  # Optional: helpful for debugging during development
    else:
        form = PostForm(initial={'status': 'draft'})

    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def edit_post(request, post_id):
    """Edit existing post"""
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponseForbidden("You don't have permission to edit this post.")
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/post_form.html', {'form': form, 'post': post})

@login_required
def delete_post(request, post_id):
    """Delete post with confirmation"""
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponseForbidden("You don't have permission to delete this post.")
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

@login_required
def dashboard(request):
    """User dashboard showing their posts"""
    user_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/dashboard.html', {'posts': user_posts})

def category_posts(request, category_id):
    """Show posts by category"""
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(
        category=category,
        status='published'
    ).select_related('author').prefetch_related('tags').order_by('-created_at')
    return render(request, 'blog/category_posts.html', {
        'category': category,
        'posts': posts
    })

def tag_posts(request, tag_id):
    """Show posts by tag"""
    tag = get_object_or_404(Tag, id=tag_id)
    posts = Post.objects.filter(
        tags=tag,
        status='published'
    ).select_related('author', 'category').order_by('-created_at')
    return render(request, 'blog/tag_posts.html', {
        'tag': tag,
        'posts': posts
    })