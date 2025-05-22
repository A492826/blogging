from django.contrib import admin
from .models import ContactMessage,Post, Tag, Category
admin.site.register(ContactMessage)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Category)

# Register your models here.
