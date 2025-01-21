from django.urls import path, include
from rest_framework.routers import DefaultRouter  # Import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Create a router and register the viewsets with the router
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

# Include the generated URLs from the router under 'api/'
urlpatterns = [
    path('api/', include(router.urls)),  # This will map the routes under /api/
]