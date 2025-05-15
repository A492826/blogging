from django.shortcuts import render

def my_view(request):
    return render(request, 'blog/blog.html')  # Assuming your template is in blog/templates/blog/blog.html

def contact(request):
    return render(request, 'blog/contact.html')

def postdetails(request):
    return render(request, 'blog/postdetails.html')

def about(request):
    return render(request, 'blog/about.html')

