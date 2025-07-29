from wagtail_modeladmin.helpers import ButtonHelper, AdminURLHelper
from wagtail_modeladmin.views import IndexView

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
        registrations = registrations.select_related(
            "user",
            "event"
        ).prefetch_related(
            "event_registration_children",
            "event_registration_extra_people",
        ).order_by("event__start_day", "event__start_time")
        for registration in registrations:
            data.append(
                {
                    "email": registration.user.email,
                    "event": registration.event.title,
                    "start_time": registration.event.start_time,
                    "start_day": registration.event.start_day,
                    "name": registration.name,
                    "surname": registration.surname,
                    "no. children": registration.event_registration_children.count(),
                    "no. extra people": registration.event_registration_extra_people.count(),
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

            last_entry = data[-1]
            for item in registration.extra_registration_question_answers.all().prefetch_related(
                "question",
                "question__answer_file",
            ):
                if item.question:
                    if item.answer_file:
                        last_entry[item.question] = item.answer_file.url
                    else:
                        last_entry[item.question] = item.answer

            for child in registration.event_registration_children.all():
                data.append(
                    {
                        "email": "↳ (child)",
                        "name": child.child_name,
                        "surname": child.child_surname,
                        "no. children": "",
                        "no. extra people": "",
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
            for extra_person in registration.event_registration_extra_people.all():
                data.append(
                    {
                        "email": "↳ (extra person)",
                        "name": extra_person.person_name,
                        "surname": extra_person.person_surname,
                        "no. children": "",
                        "no. extra people": "",
                        "phone": "",
                        "disabilities": "",
                        "allergies": "",
                        "agreement_responsibility": "",
                        "allow_photos": "",
                        "birth_date": "",
                        "gender": "",
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
