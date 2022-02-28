from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from account.managers import CustomUserManager
from account.utils import base_name_url
from organizations.models import Organization


class CustomUser(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    organization = models.ForeignKey(Organization, null=True,
                                     on_delete=models.CASCADE,
                                     related_name='custom_users',
                                     verbose_name='organizacja')
    alias = models.CharField(max_length=64, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Pracownik'
        verbose_name_plural = 'Pracownicy'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if not self.alias and self.organization:
            alias_email = self.email.split('@')
            alias_url = base_name_url(self.organization.url)
            if alias_url == alias_email[1]:
                self.alias = alias_email[0]
        return super().save(*args, **kwargs)
