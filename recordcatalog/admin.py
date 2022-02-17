from django.contrib import admin
from .models import Artist, Genre, Album, Label, Place, Wanted

admin.site.register(Genre)
admin.site.register(Label)
admin.site.register(Place)


class AlbumInline(admin.TabularInline):
    model = Album


class ArtistAdmin(admin.ModelAdmin):
    list_display = (
        "last_name",
        "first_name",
        "date_active_start",
        "date_active_end",
        "location",
    )
    fields = (
        "last_name",
        "first_name",
        ("date_active_start", "date_active_end"),
        "location",
    )


admin.site.register(Artist, ArtistAdmin)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("title", "artist", "display_genre")
    list_filter = ("genre", "label", "artist", "condition")
    fields = [
        "title",
        "artist",
        "genre",
        "label",
        "condition",
        ("album_format", "release_date"),
        "album_notes",
        "internal_notes",
        ("catalog_number"),
        "album_image",
    ]


@admin.register(Wanted)
class WantedAdmin(admin.ModelAdmin):
    list_display = ("artist", "title")
