from django.urls import path
from . import views
from . import api
from .views import export_users_csv
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("", views.index, name="index"),
    path("albums/", views.AlbumListView.as_view(), name="albums"),
    path("albums/<int:pk>", views.AlbumDetailView.as_view(), name="album-detail"),
    path("artists/", views.ArtistListView.as_view(), name="artists"),
    path("artists/<int:pk>", views.ArtistDetailView.as_view(), name="artist-detail"),
    path("genres/", views.GenreListView.as_view(), name="genres"),
    path("genres/<int:pk>", views.GenreDetailView.as_view(), name="genre-detail"),
    path("export", export_users_csv, name="export_users_csv"),
    path("wanted/", views.WantedListView.as_view(), name="wanted"),
    path("wanted/create/", views.WantedCreate.as_view(), name="wanted-create"),
    path("search_results/", views.search_results, name="search-results"),
    path("albumAPI", api.AlbumListAPIView.as_view(), name="api_albums"),
    path("artistAPI", api.ArtistListAPIView.as_view(), name="api_artists"),
    path("genreAPI", api.GenreListAPIView.as_view(), name="api_genres"),
    path("wantedAPI", api.WantedListAPIView.as_view(), name="api_wanted"),
    path("labelAPI", api.LabelListAPIView.as_view(), name="api_labels"),
    path("root", api.api_root),
]


urlpatterns += [
    path("artists/create/", views.ArtistCreate.as_view(), name="artist-create"),
    path(
        "artists/<int:pk>/update/", views.ArtistUpdate.as_view(), name="artist-update"
    ),
    path(
        "artists/<int:pk>/delete/", views.ArtistDelete.as_view(), name="artist-delete"
    ),
    path("albums/create/", views.AlbumCreate.as_view(), name="album-create"),
    path("albums/<int:pk>/update/", views.AlbumUpdate.as_view(), name="album-update"),
    path("albums/<int:pk>/delete/", views.AlbumDelete.as_view(), name="album-delete"),
]
