from . import models
from rest_framework import serializers


class StringListSerializer(serializers.ListSerializer):
    child = serializers.CharField()


class AlbumSerializer(serializers.ModelSerializer):
    genres = StringListSerializer()
    labels = StringListSerializer()
    artist_name = serializers.ReadOnlyField(source="artist.__str__")

    class Meta:
        model = models.Album
        fields = (
            "title",
            "artist_name",
            "genres",
            "labels",
            "album_notes",
            "album_format",
            "release_date",
        )


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Artist
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = "__all__"


class WantedSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Wanted
        fields = "__all__"


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Label
        fields = "__all__"
