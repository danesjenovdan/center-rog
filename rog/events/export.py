from wagtail.contrib.modeladmin.helpers import ButtonHelper, AdminURLHelper
from wagtail.contrib.modeladmin.views import IndexView

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.urls import path
from django.http import HttpResponse

import csv


class ExportButtonHelper(ButtonHelper):
    export_button_classnames = ["icon", "icon-download"]

    def export_button(self, classnames_add=None, classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []

        classnames = self.export_button_classnames + classnames_add
        cn = self.finalise_classname(classnames, classnames_exclude)
        text = _("Export {} to CSV".format(self.verbose_name_plural.title()))

        return {
            "url": self.url_helper.get_action_url(
                "export", query_params=self.request.GET
            ),
            "label": text,
            "classname": cn,
            "title": text,
        }


class ExportAdminURLHelper(AdminURLHelper):
    non_object_specific_actions = ("create", "choose_parent", "index", "export")

    def get_action_url(self, action, *args, **kwargs):
        query_params = kwargs.pop("query_params", None)

        url_name = self.get_action_url_name(action)
        if action in self.non_object_specific_actions:
            url = reverse(url_name)
        else:
            url = reverse(url_name, args=args, kwargs=kwargs)

        if query_params:
            url += "?{params}".format(params=query_params.urlencode())

        return url

    def get_action_url_pattern(self, action):
        if action in self.non_object_specific_actions:
            return self._get_action_url_pattern(action)

        return self._get_object_specific_action_url_pattern(action)


class ExportEventRegistrationView(IndexView):
    model_admin = None

    def export_csv(self):
        data = []
        registrations = self.queryset.filter(registration_finished=True)
        for registration in registrations:
            data.append(
                {
                    "email": registration.user.email,
                    "name": registration.name,
                    "surname": registration.surname,
                    "no. children": registration.event_registration_children.count(),
                    "phone": str(registration.phone),
                    "disabilities": registration.disabilities,
                    "allergies": registration.allergies,
                    "agreement_responsibility": registration.agreement_responsibility,
                    "allow_photos": registration.allow_photos,
                    "gender": "",
                    "birth_date": (
                        registration.user.birth_date.isoformat() if registration.user.birth_date else ""
                    ),
                }
            )
            for child in registration.event_registration_children.all():
                data.append(
                    {
                        "email": "↳",
                        "name": child.child_name,
                        "surname": child.child_surname,
                        "no. children": "",
                        "phone": str(child.parent_phone),
                        "disabilities": "",
                        "allergies": "",
                        "agreement_responsibility": "",
                        "allow_photos": "",
                        "birth_date": (
                            child.birth_date.isoformat() if child.birth_date else ""
                        ),
                        "gender": (
                            child.gender_other if child.gender == "O" else child.gender
                        ),
                    }
                )

        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="export.csv"'},
        )
        try:
            writer = csv.DictWriter(response, fieldnames=data[0].keys())
        except IndexError:
            return response
        writer.writeheader()
        writer.writerows(data)

        return response

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        return self.export_csv()


class ExportModelAdminMixin(object):
    button_helper_class = ExportButtonHelper
    url_helper_class = ExportAdminURLHelper
    export_view_class = ExportEventRegistrationView

    def get_admin_urls_for_registration(self):
        urls = super().get_admin_urls_for_registration()
        urls += (
            path(
                self.url_helper.get_action_url_pattern("export"),
                self.export_view_class.as_view(model_admin=self),
                name=self.url_helper.get_action_url_name("export"),
            ),
        )
        return urls

    def export_view(self, request):
        kwargs = {"model_admin": self}
        view_class = self.export_view_class
        return view_class.as_view(**kwargs)(request)
