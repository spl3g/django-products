from django.forms import Form, CharField, DecimalField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

REGISTER_CHAR_LEN = 100


def validate_username(value):
    if User.objects.filter(username=value).exists():
        raise ValidationError(f'The username "{value}" is already in use.')


class RegistrationForm(UserCreationForm):
    username = CharField(max_length=150, validators=[validate_username])

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
