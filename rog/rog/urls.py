from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views

from django.contrib.auth import views as auth_views

from home.views import (
    MyProfileView,
    EditProfileView,
    SearchProfileView,
    UserProfileView,
    PurchasePlanView,
    RegistrationView,
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
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
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
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    # TODO: tukaj dodam recimo login
    # path("prijava/", LoginView.as_view()),
    path('prijava/', auth_views.LoginView.as_view(), name='login'),
    path('odjava/', auth_views.LogoutView.as_view(), name='logout'),
    path('pozabljeno-geslo/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('registracija/', RegistrationView.as_view(), name='registration'),
    path('registracija/clanarina', RegistrationMembershipView.as_view(), name='registration-membership'),
    path('registracija/podatki', RegistrationInformationView.as_view(), name='registration-information'),
    path('registracija/profil', RegistrationProfileView.as_view(), name='registration-profile'),
    # path('registracija/placilo', RegistrationPaymentView.as_view(), name='registration-payment'),
    # path('registracija/uspeh', RegistrationSuccessView.as_view(), name='registration-success'),
    path('profil/uredi/', EditProfileView.as_view(), name='profile-edit'),
    path('profil/isci/', SearchProfileView.as_view(), name='profile-search'),
    path('profil/nakup/', PurchasePlanView.as_view(), name='profile-purchase'),
    path('profil/<int:id>/', UserProfileView.as_view(), name='profile-user'),
    path('profil/', MyProfileView.as_view(), name='profile-my'),
    path('placilo/', include('payments.urls')),
    path('ulagtoken', CheckTokenView.as_view(), name='check-token'),
    path('test-calendar-embed/', TestCalendarTemplateView.as_view(), name='test-calendar-embed'),

    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
    prefix_default_language=False,
)
