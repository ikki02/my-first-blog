from django.contrib import admin
from .models import Post, Image

# To make our model visible on the admin page
admin.site.register(Post)
admin.site.register(Image)
