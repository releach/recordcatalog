from django.db import models
from location_field.models.plain import PlainLocationField
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
import uuid
from sorl.thumbnail import ImageField
import requests
import re


class Place(models.Model):
    city = models.CharField(max_length=255)
    location = PlainLocationField(based_fields=["city"], zoom=4)

    class Meta:
        ordering = ["city"]

    def __str__(self):
        return self.city


class Genre(models.Model):
    name = models.CharField(
        max_length=200, help_text="Enter a musical genre (e.g. Folk)"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("genre-detail", args=[str(self.id)])

    class Meta:
        ordering = ["name"]


class Label(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a label (e.g. Elektra)")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Album(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    artist = models.ForeignKey("Artist", on_delete=models.SET_NULL, null=True)
    release_date = models.IntegerField(null=True, blank=True)
    album_notes = models.TextField(blank=True, help_text="Notes about the album")
    internal_notes = models.TextField(blank=True, help_text="Internal notes")
    album_image = models.ImageField(blank=True, upload_to="images")
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this album")
    label = models.ManyToManyField(Label, help_text="Select a label for this album")
    album_format = models.CharField(
        max_length=200, help_text="Enter a format, such as CD, LP, or EP", blank=True
    )
    catalog_number = models.CharField("Catalog number", max_length=25, blank=True)

    CONDITION = (
        ("Excellent", "Excellent"),
        ("Good", "Good"),
        ("Poor", "Poor"),
        ("Unknown", "Unknown"),
    )

    condition = models.CharField(
        max_length=20,
        choices=CONDITION,
        blank=True,
        default="Unknown",
        help_text="Album condition",
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.title

    def get_absolute_url(self):
        return reverse("album-detail", args=[str(self.id)])

    def display_genre(self):
        return ", ".join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = "Genre"

    def display_label(self):
        return ", ".join(label.name for label in self.label.all()[:3])

    display_label.short_description = "Label"

    class Meta:
        permissions = (("internal", "Can view internal data"),)
        ordering = ["title"]

    def genres(self) -> list:
        return [a.name for a in self.genre.all()]

    def labels(self) -> list:
        return [a.name for a in self.label.all()]


class Artist(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100)
    discogs_id = models.CharField("Discogs ID", max_length=50, blank=True, null=True)
    artist_bio = models.TextField("Artist biography", blank=True, null=True)
    image_url = models.URLField(max_length=300, blank=True, null=True)
    date_active_start = models.IntegerField("Active", null=True, blank=True)
    date_active_end = models.IntegerField("Retired", null=True, blank=True)
    location = models.ForeignKey(
        "Place", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        return reverse("artist-detail", args=[str(self.id)])

    def __str__(self):
        if self.first_name:
            return f"{self.last_name}, {self.first_name}"
        else:
            return f"{self.last_name}"

    def bio(self):
        if not self.artist_bio:
            if self.discogs_id:
                CLEANR = re.compile("(\[a=)(.*?)(\])")
                r = requests.get(
                    f"https://api.discogs.com/artists/{self.discogs_id}"
                ).json()
                if "profile" in r:
                    profile = r["profile"]
                    profile = re.sub(CLEANR, r"\2", profile)
                    self.artist_bio = profile
                else:
                    profile = "No profile information available."
                self.save(update_fields=["artist_bio"])
                return profile


class Wanted(models.Model):
    title = models.CharField(blank=True, max_length=240)
    artist = models.CharField(blank=True, max_length=240)
    album_notes = models.TextField(blank=True, help_text="For extra info")

    def __str__(self):
        return self.title
