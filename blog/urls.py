from django.urls import path, include  # ✅ Correct import
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
     path('', views.home, name='home'),                         # Home page
    path('blog/', views.my_view, name='blog'),                 # Blog landing page
    path('contact/', views.contact, name='contact'),           # Contact form
    path('about/', views.about, name='about'),                 # About page
    path('posts/', views.posts, name='post_list'),             # ✅ Post list view
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),  # Post detail
    path('signup/', views.signup, name='signup'),
    path('create-post/', views.create_post, name='create_post'),
     path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('posts/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('dashboard/', views.dashboard, name='dashboard'),


    
]
