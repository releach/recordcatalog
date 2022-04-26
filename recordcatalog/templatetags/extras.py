from django import template
from recordcatalog.models import Album, Genre, Artist
from django.db.models import CharField, Value as V, Count, Q
from django.db.models.functions import Cast, Coalesce, Concat

register = template.Library()


@register.filter
def lower(value):  # Only one argument.
    return value.lower()


@register.simple_tag
def genre_count():
    gcount = Album.objects.values_list("genre").annotate(genre_count=Count("genre"))
    return gcount


@register.inclusion_tag("recordcatalog/latest_records.html")
def recently_added():
    recent_records = Album.objects.filter().order_by("-id")[:3]
    return {"recent_records": recent_records}


@register.simple_tag
def top_genres():
    topgenres = (
        Album.objects.values_list("genre")
        .annotate(genre_count=Count("genre"))
        .order_by("-genre_count")[:3]
    )
    genrelist = []
    genrelist.append(
        (
            Genre.objects.values_list("name", flat=True).get(pk=(topgenres[0][0])),
            topgenres[0][1],
            topgenres[0][0],
        )
    )
    genrelist.append(
        (
            Genre.objects.values_list("name", flat=True).get(pk=(topgenres[1][0])),
            topgenres[1][1],
            topgenres[1][0],
        )
    )
    genrelist.append(
        (
            Genre.objects.values_list("name", flat=True).get(pk=(topgenres[2][0])),
            topgenres[2][1],
            topgenres[2][0],
        )
    )
    return genrelist


@register.simple_tag
def top_artists():
    topartist = (
        Album.objects.values_list("artist")
        .annotate(artist_count=Count("artist"))
        .order_by("-artist_count")[:3]
    )
    artistlist = []
    artistlist.append(
        (
            Artist.objects.annotate(full_name=Concat("first_name", V(" "), "last_name"))
            .values_list("full_name", flat=True)
            .get(pk=(topartist[0][0]))
            .strip(),
            topartist[0][1],
            topartist[0][0],
        )
    )
    artistlist.append(
        (
            Artist.objects.annotate(full_name=Concat("first_name", V(" "), "last_name"))
            .values_list("full_name", flat=True)
            .get(pk=(topartist[1][0]))
            .strip(),
            topartist[1][1],
            topartist[1][0],
        )
    )
    artistlist.append(
        (
            Artist.objects.annotate(full_name=Concat("first_name", V(" "), "last_name"))
            .values_list("full_name", flat=True)
            .get(pk=(topartist[2][0]))
            .strip(),
            topartist[2][1],
            topartist[2][0],
        )
    )
    return artistlist
