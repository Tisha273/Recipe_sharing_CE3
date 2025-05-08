from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import Recipe, RecipeStep, Ingredient
from .forms import RecipeForm, UserRegisterForm
from django.db.models import Q

def home(request):
    latest_recipes = Recipe.objects.all().order_by('-created_at')[:6]
    return render(request, 'home/index.html', {'recipes': latest_recipes})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = UserRegisterForm()
    return render(request, 'Auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid credentials.')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
    return render(request, 'Auth/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

@login_required
def dashboard(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    recipes = Recipe.objects.filter(user=request.user)
    
    if search_query:
        recipes = recipes.filter(name__icontains=search_query)
    if category_filter:
        recipes = recipes.filter(category=category_filter)
        
    return render(request, 'User/Dashboard.html', {
        'recipes': recipes,
        'categories': Recipe.CATEGORY_CHOICES,
        'selected_category': category_filter
    })

def recipes_list(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    recipes = Recipe.objects.all().order_by('-created_at')
    
    if search_query:
        recipes = recipes.filter(name__icontains=search_query)
    if category_filter:
        recipes = recipes.filter(category=category_filter)
        
    paginator = Paginator(recipes, 9)  
    page = request.GET.get('page')
    recipes = paginator.get_page(page)
    
    return render(request, 'recipes/recipes.html', {
        'recipes': recipes,
        'categories': Recipe.CATEGORY_CHOICES,
        'selected_category': category_filter
    })

@login_required
def add_recipe(request):
    if request.method == 'POST':
        recipe_data = {
            'name': request.POST.get('name'),
            'description': request.POST.get('description'),
            'category': request.POST.get('category'),
            'image': request.FILES.get('image'),
        }
        
        recipe = Recipe.objects.create(user=request.user, **recipe_data)
        
        steps = request.POST.getlist('steps[]')
        for i, step in enumerate(steps, 1):
            if step.strip():
                RecipeStep.objects.create(recipe=recipe, step_number=i, description=step)
        
        ingredients = request.POST.getlist('ingredients[]')
        quantities = request.POST.getlist('quantities[]')
        for ing, qty in zip(ingredients, quantities):
            if ing.strip() and qty.strip():
                Ingredient.objects.create(recipe=recipe, name=ing, quantity=qty)
        
        messages.success(request, 'Recipe added successfully!')
        return redirect('dashboard')
    
    return redirect('dashboard')

@login_required
def edit_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    
    if request.method == 'POST':
        recipe.name = request.POST.get('name')
        recipe.description = request.POST.get('description')
        recipe.category = request.POST.get('category')
        if 'image' in request.FILES:
            recipe.image = request.FILES['image']
        recipe.save()
        
        recipe.steps.all().delete()
        steps = request.POST.getlist('steps[]')
        for i, step in enumerate(steps, 1):
            if step.strip():
                RecipeStep.objects.create(recipe=recipe, step_number=i, description=step)
        
        recipe.ingredients.all().delete()
        ingredients = request.POST.getlist('ingredients[]')
        quantities = request.POST.getlist('quantities[]')
        for ing, qty in zip(ingredients, quantities):
            if ing.strip() and qty.strip():
                Ingredient.objects.create(recipe=recipe, name=ing, quantity=qty)
        
        messages.success(request, 'Recipe updated successfully!')
        return redirect('dashboard')
    
    return render(request, 'recipes/edit_recipe.html', {
        'recipe': recipe,
        'categories': Recipe.CATEGORY_CHOICES
    })
@login_required
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, user=request.user)
    recipe.delete()
    messages.success(request, 'Recipe deleted successfully!')
    return redirect('dashboard')

def view_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipes/viewrecipes.html', {'recipe': recipe})

def about(request):
    return render(request, 'About/About.html')





# # views.py
# import requests
# from django.shortcuts import render
# from django.http import JsonResponse

# def search_flask_api(request):
#     query = request.GET.get('q', '')
#     if query:
#         # Call Flask API with search query
#         response = requests.get(f'http://127.0.0.1:5000/search?q={query}')
#         data = response.json()
#         return JsonResponse(data, safe=False)  # Or render a template
#     return JsonResponse({'error': 'No query parameter provided'}, status=400)






# views.py
# import requests
# from django.shortcuts import render

# def search_flask_api(request):
#     query = request.GET.get('q', '')
#     data = []
#     if query:
#         try:
#             response = requests.get(f'http://127.0.0.1:5000/search?q={query}')
#             if response.status_code == 200:
#                 data = response.json()
#         except requests.exceptions.ConnectionError:
#             data = [{"name": "Error", "description": "Could not connect to Flask API"}]
#     return render(request, 'search.html', {'data': data, 'query': query})



# views.py
import requests
from django.shortcuts import render

def search_flask_api(request):
    query = request.GET.get('q', '')
    data = []
    if query:
        try:
            response = requests.get(f'http://127.0.0.1:5000/search?q={query}')
            if response.status_code == 200:
                data = response.json()
        except Exception as e:
            print("Error:", e)
            data = [{"name": "Error", "description": "Flask API not reachable"}]
    return render(request, 'search.html', {'data': data, 'query': query})





# home/views.py
# home/views.py
from rest_framework import viewsets
from .models import MyModel  # or whatever your actual model is
from .serializers import MyModelSerializer  # match your serializer name

class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer  


