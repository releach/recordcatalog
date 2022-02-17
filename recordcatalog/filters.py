import django_filters
from recordcatalog.models import Album, Artist, Genre, Wanted
from django.db import models


class AlbumFilter(django_filters.FilterSet):
    class Meta:
        model = Album
        fields = [
            "title",
        ]
        filter_overrides = {
            models.CharField: {
                "filter_class": django_filters.CharFilter,
                "extra": lambda f: {
                    "lookup_expr": "icontains",
                },
            }
        }


class ArtistFilter(django_filters.FilterSet):
    class Meta:
        model = Artist
        fields = {
            "last_name": ["icontains"],
        }


class GenreFilter(django_filters.FilterSet):
    class Meta:
        model = Genre
        fields = {
            "name": ["icontains"],
        }


class WantedFilter(django_filters.FilterSet):
    class Meta:
        model = Wanted
        fields = {
            "title": ["icontains"],
        }
