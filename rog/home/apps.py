from django.apps import AppConfig


class HomeAppConfig(AppConfig):
    name = 'home'

    def ready(self):
        from .patches.patch_images import patch_images_index_view
        patch_images_index_view()
