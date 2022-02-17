from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from . import serializers
from . import models


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "albumsAPI": reverse("api_albums", request=request, format=format),
            "artistsAPI": reverse("api_artists", request=request, format=format),
            "genresAPI": reverse("api_genres", request=request, format=format),
            "labelsAPI": reverse("api_labels", request=request, format=format),
            "wantedAPI": reverse("api_wanted", request=request, format=format),
        }
    )


class AlbumListAPIView(ListAPIView):
    serializer_class = serializers.AlbumSerializer

    def get_queryset(self):
        return models.Album.objects.all()


class ArtistListAPIView(ListAPIView):
    serializer_class = serializers.ArtistSerializer

    def get_queryset(self):
        return models.Artist.objects.all()


class GenreListAPIView(ListAPIView):
    serializer_class = serializers.GenreSerializer

    def get_queryset(self):
        return models.Genre.objects.all()


class WantedListAPIView(ListAPIView):
    serializer_class = serializers.WantedSerializer

    def get_queryset(self):
        return models.Wanted.objects.all()


class LabelListAPIView(ListAPIView):
    serializer_class = serializers.LabelSerializer

    def get_queryset(self):
        return models.Label.objects.all()
