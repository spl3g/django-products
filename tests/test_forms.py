"""Test forms."""

from django.contrib.auth.models import User
from django.test import TestCase
from products_app.forms import (RegistrationForm, ReviewCreationForm,
                                SupplierRegistrationForm)

USERNAME = 'username'
PSWD2 = 'password2'
PSWD = 'pa$$word12345'
NAME = 'name'
PHONE = 'phone'


class FormTests(TestCase):

    def test_registration_form_valid(self):
        form_data = {
            USERNAME: 'newuser',
            'password1': PSWD,
            PSWD2: PSWD,
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_registration_form_invalid_username(self):
        User.objects.create_user(username='existinguser', password=PSWD)
        form_data = {
            USERNAME: 'existinguser',
            'password1': PSWD,
            PSWD2: PSWD,
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(USERNAME, form.errors)
        self.assertEqual(form.errors[USERNAME], ['A user with that username already exists.'])

    def test_registration_form_password_mismatch(self):
        form_data = {
            USERNAME: 'newuser',
            'password1': PSWD,
            PSWD2: 'password54321',
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(PSWD2, form.errors)

    def test_review_creation_form_valid(self):
        form_data = {
            'text': 'This is a review',
            'rating': 5,
            'product_id': '123',
        }
        form = ReviewCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_review_creation_form_invalid(self):
        form_data = {
            'text': '',
            'rating': '',
            'product_id': '123',
        }
        form = ReviewCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)

    def test_supplier_registration_form_valid(self):
        form_data = {
            NAME: 'Supplier Name',
            PHONE: '1234567890',
        }
        form = SupplierRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_supplier_registration_form_invalid(self):
        form_data = {
            NAME: '',
            PHONE: '',
        }
        form = SupplierRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(NAME, form.errors)
        self.assertIn(PHONE, form.errors)
        self.assertEqual(form.errors[NAME], ['This field is required.'])
        self.assertEqual(form.errors[PHONE], ['This field is required.'])
