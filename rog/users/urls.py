from django.urls import path

from .views import (
    EditGalleryView,
    DeleteGalleryView,
    ConfirmUserView,
    ResendConfirmationMailView,
)

urlpatterns = [
    path("edit-gallery/", EditGalleryView.as_view(), name="edit-gallery"),
    path("delete-gallery/", DeleteGalleryView.as_view(), name="delete-gallery"),
    path("confirm-user/", ConfirmUserView.as_view(), name="confirm-user"),
    path(
        "resend-confirm-user/",
        ResendConfirmationMailView.as_view(),
        name="resend-confirm-user",
    ),
]
