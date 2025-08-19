from django.urls import path, include
from rest_framework import routers

from .views import ItemView

router = routers.DefaultRouter()
# router.register(r"items", ItemView, basename="items")

urlpatterns = [
     path('', include(router.urls)),
     path('items', ItemView.as_view()),
]