from django.urls import path, include
from rest_framework.routers import DefaultRouter

from trainer import views


router = DefaultRouter()
router.register('students', views.StudentViewSet)
router.register('words', views.WordViewSet)
router.register('wordsets', views.WordSetViewSet)

app_name = 'trainer'

urlpatterns = [
    path('', include(router.urls))
]
