from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Create a router and register the viewsets with the router
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet)