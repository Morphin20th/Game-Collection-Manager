from django import forms
from django.contrib.auth.forms import UserCreationForm

from collection.models import Collection, Gamer


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["name", "game", ]


class GamerCreationForm(UserCreationForm):
    class Meta:
        model = Gamer
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "bio",)


class GamerBioUpdateForm(forms.ModelForm):
    class Meta:
        model = Gamer
        fields = ("bio",)


class GamerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by username"}),
    )


class GenreSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by genre"}),
    )

class CollectionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by collection"}),
    )

class GameSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by title"}),
    )