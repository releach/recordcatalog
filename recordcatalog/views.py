from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from recordcatalog.models import Album, Artist, Genre, Label, Wanted
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .filters import AlbumFilter, ArtistFilter, GenreFilter
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import random
from django.http import HttpResponse
import csv
from datetime import datetime, timedelta
from django.db.models import CharField, Value as V, Count, Q
from django.db.models.functions import Cast, Coalesce, Concat


def index(request):
    num_albums = Album.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_labels = Label.objects.all().count()
    num_artists = Artist.objects.count()

    context = {
        "num_albums": num_albums,
        "num_artists": num_artists,
        "num_genres": num_genres,
    }
    return render(request, "index.html", context=context)


class AlbumListView(generic.ListView):
    model = Album
    paginate_by = 20
    template_name = "recordcatalog/album_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = AlbumFilter(self.request.GET, queryset=self.get_queryset())
        return context


class AlbumDetailView(generic.DetailView):
    model = Album


class GenreDetailView(generic.DetailView):
    model = Genre


class GenreListView(generic.ListView):
    model = Genre
    paginate_by = 20
    template_name = "recordcatalog/genre_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = GenreFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ArtistListView(generic.ListView):
    model = Artist
    paginate_by = 20
    template_name = "recordcatalog/artist_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = ArtistFilter(self.request.GET, queryset=self.get_queryset())
        return context


class ArtistDetailView(generic.DetailView):
    model = Artist


class ArtistCreate(PermissionRequiredMixin, CreateView):
    permission_required = "recordcatalog.internal"
    model = Artist
    fields = ["first_name", "last_name", "date_active_start", "date_active_end"]


class ArtistUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "recordcatalog.internal"
    model = Artist
    fields = (
        "__all__"  # Not recommended (potential security issue if more fields added)
    )


class ArtistDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "recordcatalog.internal"
    model = Artist
    success_url = reverse_lazy("artists")


class AlbumCreate(PermissionRequiredMixin, CreateView):
    permission_required = "recordcatalog.internal"
    model = Album
    fields = "__all__"


class AlbumUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "recordcatalog.internal"
    model = Album
    fields = (
        "__all__"  # Not recommended (potential security issue if more fields added)
    )


class AlbumDelete(PermissionRequiredMixin, DeleteView):
    permission_required = "recordcatalog.internal"
    model = Album
    success_url = reverse_lazy("albums")


def export_users_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="albums.csv"'
    writer = csv.writer(response)
    writer.writerow(
        [
            "title",
            "release_date",
            "album_format",
            "image",
            "catalog_number",
            "genre",
            "label",
            "condition",
            "album_notes",
            "internal_notes",
            "artist",
            "artist_location",
            "artist_active_start",
            "artist_active_end",
            "created_at",
        ]
    )
    qs = Album.objects.prefetch_related("genre", "label")
    for album in qs:
        writer.writerow(
            [
                album.title,
                album.release_date,
                album.album_format,
                album.album_image,
                album.catalog_number,
                "|".join(c.name for c in album.genre.all()),
                "|".join(c.name for c in album.label.all()),
                album.condition,
                album.album_notes,
                album.internal_notes,
                album.artist,
                album.artist.location,
                album.artist.date_active_start,
                album.artist.date_active_end,
                album.created_at,
            ]
        )

    return response
    success_url = reverse_lazy("")


class WantedListView(generic.ListView):
    model = Wanted
    template_name = "recordcatalog/wanted_list.html"


class WantedCreate(PermissionRequiredMixin, CreateView):
    permission_required = "recordcatalog.internal"
    model = Wanted
    fields = "__all__"
    success_url = reverse_lazy("wanted")


def search_results(request):
    if request.method == "POST":
        search_query = request.POST.get("search_query")
        albums = Album.objects.filter(title__icontains=search_query)
        artists = Artist.objects.filter(
            Q(last_name__icontains=search_query) | Q(first_name__icontains=search_query)
        )
        genres = Genre.objects.filter(name__icontains=search_query)
        return render(
            request,
            "recordcatalog/search_results.html",
            {
                "search_query": search_query,
                "albums": albums,
                "artists": artists,
                "genres": genres,
            },
        )
    else:
        return render(request, "recordcatalog/search_results.html", {})
