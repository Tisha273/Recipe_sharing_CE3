from django.contrib import admin
from .models import*

admin.site.register(Recipe)
admin.site.register(RecipeStep)
admin.site.register(Ingredient)

