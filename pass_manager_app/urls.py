# pass_manager_app/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, basename ='hello-viewset')
router.register('profile', views.UserProfileViewSet)
router.register('feed', views.UserProfileFeedViewSet)
urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view(), name='hello-view'),
    path('login/', views.UserLoginApiView.as_view()), 
    path('', include(router.urls))
    # Other URL patterns for the pass_manager_app
]
