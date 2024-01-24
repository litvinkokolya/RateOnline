from django import forms
from .models import MemberNominationPhoto

class UploadPhotoForm(forms.ModelForm):
    class Meta:
        model = MemberNominationPhoto
        fields = ['photo']
