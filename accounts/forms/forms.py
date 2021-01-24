from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import atomic
from django.forms import CharField, Textarea
from django.contrib.auth.models import User
from django.forms import ImageField, ModelForm

from accounts.models import Profile


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email']

    about = CharField(label='About me', widget=Textarea, min_length=10)

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        result = super().save(commit)
        about = self.cleaned_data['about']
        profile = Profile(about=about, user=result)
        if commit:
            profile.save()
        return result


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']
