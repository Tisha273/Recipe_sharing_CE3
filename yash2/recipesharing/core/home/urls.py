from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyModelViewSet  # Ensure this matches the viewset name in views.py

router = DefaultRouter()
router.register(r'mymodel', MyModelViewSet)  # This should also match your model name

urlpatterns = [
    path('', include(router.urls)),
]





# urls.py
# from django.urls import path
# from .views import search_flask_api  # Ensure this matches the view name

# urlpatterns = [
#     path('search/', search_flask_api, name='search-flask-api'),
# ]
