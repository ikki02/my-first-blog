from django.contrib import admin
from .models import Post

# To make our model visible on the admin page
admin.site.register(Post)
