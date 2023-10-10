from django.urls import path

from .views import EditGalleryView, DeleteGalleryView

urlpatterns = [
    path('edit-gallery/', EditGalleryView.as_view(), name='edit-gallery'),
    path('delete-gallery/', DeleteGalleryView.as_view(), name='delete-gallery'),
]
