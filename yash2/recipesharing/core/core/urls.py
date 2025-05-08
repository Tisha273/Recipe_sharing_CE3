from django.contrib import admin
from django.urls import path,include
from home.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('recipes/', recipes_list, name='recipes'),
    path('recipe/add/', add_recipe, name='add_recipe'),
    path('about/', about, name='about'),
    path('recipe/edit/<int:recipe_id>/', edit_recipe, name='edit_recipe'),
    path('recipe/delete/<int:recipe_id>/', delete_recipe, name='delete_recipe'),
    path('recipe/view/<int:recipe_id>/', view_recipe, name='view_recipe'),
    path('recipe/edit/<int:recipe_id>/', edit_recipe, name='edit_recipe'),
    path('api/', include('home.urls')),
      path('search/', search_flask_api, name='search-flask-api'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


