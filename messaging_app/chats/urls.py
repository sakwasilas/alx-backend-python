from django.urls import path, include
from rest_framework.routers import DefaultRouter  # Make sure this import is included
from .views import ConversationViewSet, MessageViewSet

# Create a router and register the viewsets with the router
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('api/', include(router.urls)),  # Include the generated URLs from the router
]