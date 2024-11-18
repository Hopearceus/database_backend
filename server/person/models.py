from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Person(AbstractUser):
    pid = models.AutoField(primary_key=True, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True, 
                             validators=[
                                RegexValidator(
                                regex=r'^\+?1?\d{9,15}$',
                                message=_('Phone number must be entered in the format: +999999999. Up to 15 digits allowed.'),
                                code='invalid_phone'
                            )
                        ])
    email = models.EmailField(
        blank=True,
        null=True,
        validators=[
            EmailValidator(
                message=_('Enter a valid email address.')
            )
        ]
    )
    introduction = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
        ],
        default='Other'
    )


    def clean(self) -> None:
        return super().clean()