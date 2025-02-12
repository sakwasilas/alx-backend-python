from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Initialize the DefaultRouter
router = DefaultRouter()

# Register the viewsets with the router
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    # Include the router URLs in the main URL patterns
    path('api/', include(router.urls)),
]