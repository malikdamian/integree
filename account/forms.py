from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from account.utils import base_name_url

from unidecode import unidecode

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name',
                  'last_name', 'organization')

    def save(self, commit=True):
        instance = super().save(commit=False)
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        name = f'{first_name}.{last_name}'.lower()
        email = name + '@' + base_name_url(instance.organization.url)
        instance.email = unidecode(email)
        if commit:
            instance.save()
        return instance


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',)
