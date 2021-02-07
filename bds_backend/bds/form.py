from django import forms
from django.core.files.images import get_image_dimensions

from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile

    def clean_avatar(self):
        avatar = self.clean_avatar['avatar']

        try:
            width, height = get_image_dimensions(avatar)

            # validate dimensions:
            max_width = max_height = 100
            if width > max_width or height > max_height:
                raise forms.ValidationError("Please use an image that has width less than ", max_width, ", and length less than ", max_height)

            # validate content type:
            main, sub = avatar.content_type.split('/')

            if not (main == 'image' and sub in ['jpeg', 'pjpeg', 'gif', 'png']):
                raise forms.ValidationError("Please use a JPEG, GIF, or PNG image")

            # validate file size:
            if len(avatar) > (10 * 1024):
                raise forms.ValidationError("Image size must be less than 10MB")

        except AttributeError:
            """
            Handles case when we are updating the user profile
            and do not supply a new avatar
            """
            pass

        return avatar