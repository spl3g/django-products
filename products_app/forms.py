from django.forms import Form, CharField, DecimalField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Supplier
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class SupplierRegistrationForm(UserCreationForm):
    name = CharField(max_length=REGISTER_CHAR_LEN, required=True)
    phone = CharField(max_length=REGISTER_CHAR_LEN, required=True)

    class Meta:
        model = Supplier
        fields = ['Username', 'Name', 'Phone', 'Password', 'Repeat password']
