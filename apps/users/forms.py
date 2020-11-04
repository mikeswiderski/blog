from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.core.files.images import get_image_dimensions


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("This email has already been used. Please use another email.")
        return email 

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self, *args, **kwargs):
        instance = self.instance
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if instance is not None:
            qs = qs.exclude(id=instance.id)
        if qs.exists():
            raise forms.ValidationError("This email has already been used. Please use another email.")
        return email 

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
        
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 800*1024:
                raise forms.ValidationError("Image file too large! max 800kb")
            w, h = get_image_dimensions(image)
            if w <= 400:
               raise forms.ValidationError("The image is %i pixel wide. It's supposed to be at least 400 x 400 px" % w)
            if h <= 400:
               raise forms.ValidationError("The image is %i pixel high. It's supposed to be at least 400 x 400 px" % h)
            return image
        else:
            raise forms.ValidationError("Couldn't read uploaded image")
