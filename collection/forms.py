from django import forms
from django.contrib.auth.forms import UserCreationForm

from collection.models import Collection, Gamer, Game


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = "__all__"

    game = forms.ModelMultipleChoiceField(
        queryset=Game.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super(CollectionForm, self).__init__(*args, **kwargs)
        self.fields["name"].widget.attrs.update({"class": "form-control"})


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ["title", "platform", "release_date", "price", "genre"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "platform": forms.TextInput(attrs={"class": "form-control"}),
            "release_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "genre": forms.Select(attrs={"class": "form-control"}),
        }


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
