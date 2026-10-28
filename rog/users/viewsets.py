from wagtail.users.views.users import UserViewSet

from users.forms import CustomUserCreationForm, CustomUserEditForm


class CustomUserViewSet(UserViewSet):
    def get_form_class(self, for_update=False):
        if for_update:
            return CustomUserEditForm
        return CustomUserCreationForm
