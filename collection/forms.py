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
