from django.urls import path, include
from rest_framework.routers import DefaultRouter

from trainer import views


router = DefaultRouter()
router.register('student', views.StudentViewSet)

app_name = 'trainer'

urlpatterns = [
    path('', include(router.urls))
]
