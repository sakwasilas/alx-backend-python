from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter  # Import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Create the main router
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)

# Create a nested router for messages, with conversations as the parent
conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Include the generated URLs from the router and nested router under 'api/'
urlpatterns = [
    path('api/', include(router.urls)),  # Include the main API paths
    path('api/', include(conversations_router.urls)),  # Include nested messages under conversations
]