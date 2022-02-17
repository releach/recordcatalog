from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf.urls import url
from django.contrib.staticfiles.storage import staticfiles_storage

from django.views.generic.base import RedirectView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("recordcatalog.urls")),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
]

urlpatterns += [
    path("recordcatalog/", include("recordcatalog.urls")),
]

from django.views.generic import RedirectView

urlpatterns += [
    path("", RedirectView.as_view(url="recordcatalog/", permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path("accounts/", include("django.contrib.auth.urls")),
]
