from django.urls import path

from .views import EditGalleryView

urlpatterns = [
    path('edit-gallery/', EditGalleryView.as_view(), name='edit-gallery'),
]
