from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet

# Initialize the DefaultRouter
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router for messages under each conversation
conversation_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Define urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # Include main router URLs
    path('', include(conversation_router.urls)),  # Include nested router URLs
]
