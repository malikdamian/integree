from django.db import models

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_tax_number(tax_number):
    tax_number = tax_number.replace('-', '').replace(' ', '')
    if len(tax_number) != 10 or not tax_number.isdigit():
        raise ValidationError(_('Nieprawidłowy NIP!'))
    digits = list(map(int, tax_number))
    weights = (6, 5, 7, 2, 3, 4, 5, 6, 7)
    check_sum = sum(weight * digit for weight, digit in zip(weights, digits)) % 11
    if check_sum != digits[9]:
        raise ValidationError(_('Nieprawidłowy NIP'))


def upload_to(instance, filename):
    return f'organizations/{instance.name}/{filename}'


class Organization(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='nazwa')
    tax_number = models.CharField(max_length=20,
                                  validators=[validate_tax_number],
                                  verbose_name='NIP')
    country = models.CharField(max_length=256,
                               verbose_name='państwo')
    url = models.URLField()
    logo = models.ImageField(upload_to=upload_to,
                             null=True, blank=True)

    class Meta:
        verbose_name = 'Organizacja'
        verbose_name_plural = 'Organizacje'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.tax_number = self.tax_number.replace('-', '').replace(' ', '')
        super().save(*args, **kwargs)
