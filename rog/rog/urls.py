from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from wagtailautocomplete.urls.admin import urlpatterns as autocomplete_admin_urls

from search import views as search_views

from django.contrib.auth import views as auth_views

from home.views import (
    MyProfileView,
    EditProfileView,
    SearchProfileView,
    UserProfileView,
    PurchasePlanView,
    PurchaseMembershipView,
    RegistrationView,
    RegistrationMailConfirmationView,
    RegistrationMembershipView,
    RegistrationInformationView,
    RegistrationProfileView,
    # RegistrationPaymentView,
    # RegistrationSuccessView,
)

from users.views import (
    CheckTokenView,
    TestCalendarTemplateView,
)

# Non-translatable URLs
urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/autocomplete/", include(autocomplete_admin_urls)),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("i18n/", include("django.conf.urls.i18n")),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Translatable URLs
# These will be available under a language code prefix.
urlpatterns = urlpatterns + i18n_patterns(
    path("search/", search_views.search, name="search"),
    path("prijava/", auth_views.LoginView.as_view(), name="login"),
    path("odjava/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "pozabljeno-geslo/",
        auth_views.PasswordResetView.as_view(
            html_email_template_name="registration/password_reset_email.html",
            email_template_name="registration/password_reset_email_txt.html",
        ),
        name="password_reset",
    ),
    path(
        "ponastavi-geslo/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "geslo-je-ponastavljeno/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("registracija/", RegistrationView.as_view(), name="registration"),
    path(
        "registracija/potrditev",
        RegistrationMailConfirmationView.as_view(),
        name="registration-email-confirmation",
    ),
    path(
        "registracija/clanarina",
        RegistrationMembershipView.as_view(),
        name="registration-membership",
    ),
    path(
        "registracija/podatki",
        RegistrationInformationView.as_view(),
        name="registration-information",
    ),
    path(
        "registracija/profil",
        RegistrationProfileView.as_view(),
        name="registration-profile",
    ),
    # path('registracija/placilo', RegistrationPaymentView.as_view(), name='registration-payment'),
    # path('registracija/uspeh', RegistrationSuccessView.as_view(), name='registration-success'),
    path("profil/uredi/", EditProfileView.as_view(), name="profile-edit"),
    path("profil/isci/", SearchProfileView.as_view(), name="profile-search"),
    path("profil/nakup/", PurchasePlanView.as_view(), name="profile-purchase-plan"),
    path(
        "profil/clanstvo/",
        PurchaseMembershipView.as_view(),
        name="profile-purchase-membership",
    ),
    path("profil/<int:id>/", UserProfileView.as_view(), name="profile-user"),
    path("profil/", MyProfileView.as_view(), name="profile-my"),
    path("placilo/", include("payments.urls")),
    path("prijava-na-dogodek/", include("events.urls")),
    path("ulagtoken", CheckTokenView.as_view(), name="check-token"),
    path(
        "test-calendar-embed/",
        TestCalendarTemplateView.as_view(),
        name="test-calendar-embed",
    ),
    path("users/", include("users.urls")),
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
    prefix_default_language=False,
)
