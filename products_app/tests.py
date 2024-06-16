from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Product


class CategoryAPITest(APITestCase):
    url = "/api/v1/categories/"
    _user_creds = {
        "username": "abc",
        "password": "abc",
    }
    _superuser_creds = {
        "username": "def",
        "password": "def",
        "is_superuser": True,
    }

    def setUp(self):
        self.user = User.objects.create(**self._user_creds)
        self.token = Token(user=self.user)
        self.superuser = User.objects.create_superuser(**self._superuser_creds)
        self.superuser_token = Token(user=self.superuser)
        self.client.force_authenticate(
            user=self.superuser, token=self.superuser_token)

    def create_category(self):
        data = {"name": "Test Category", "description": "Test description"}
        response = self.client.post(self.url, data, format="json")
        return response

    def test_get_all_categories(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        response = self.create_category()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_category(self):
        category = self.create_category().json()["id"]
        response = self.client.get(self.url + category + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category(self):
        category = self.create_category().json()["id"]
        data = {"name": "Updated Category",
                "description": "Updated description"}
        response = self.client.put(
            self.url + category + "/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        category = self.create_category().json()["id"]
        response = self.client.delete(self.url + category + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProductAPITest(APITestCase):
    url = "/api/v1/products/"

    _user_creds = {
        "username": "abc",
        "password": "abc",
    }
    _superuser_creds = {
        "username": "def",
        "password": "def",
        "is_superuser": True,
    }

    def setUp(self):
        self.user = User.objects.create(**self._user_creds)
        self.token = Token(user=self.user)
        self.superuser = User.objects.create_superuser(**self._superuser_creds)
        self.superuser_token = Token(user=self.superuser)
        self.client.force_authenticate(user=self.user, token=self.token)

    def create_product(self):
        data = {"name": "Test Product", "price": 10.00}
        response = self.client.post(self.url, data, format="json")
        return response

    def test_get_all_products(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        response = self.create_product()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_product(self):
        response = self.create_product()
        product_id = response.json()["id"]
        response = self.client.get(self.url + product_id + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product(self):
        response = self.create_product()
        product_id = response.json()["id"]
        data = {"name": "Updated Product", "price": 20.00}
        response = self.client.put(
            self.url + product_id + "/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        response = self.create_product()
        product_id = response.json()["id"]
        response = self.client.delete(self.url + product_id + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_price_validator(self):
        data = {"name": "Test Product", "price": -10.00}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReviewAPITest(APITestCase):
    url = "/api/v1/reviews/"

    _user_creds = {
        "username": "abc",
        "password": "abc",
    }
    _superuser_creds = {
        "username": "def",
        "password": "def",
        "is_superuser": True,
    }

    def setUp(self):
        self.user = User.objects.create(**self._user_creds)
        self.token = Token(user=self.user)
        self.superuser = User.objects.create_superuser(**self._superuser_creds)
        self.superuser_token = Token(user=self.superuser)
        self.client.force_authenticate(user=self.user, token=self.token)

    def create_review(self):
        product = Product.objects.create(
            owner=self.user, name="test", price=5.0)
        data = {"product_id": product.id, "rating": 5, "text": "Test review"}
        response = self.client.post(self.url, data, format="json")
        return response

    def test_get_all_reviews(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_review(self):
        response = self.create_review()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_review(self):
        response = self.create_review()
        review_id = response.json()["id"]
        response = self.client.get(self.url + review_id + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_review(self):
        response = self.create_review()
        review_id = response.json()["id"]
        data = {"rating": 4, "text": "Updated review"}
        response = self.client.patch(
            self.url + review_id + "/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_review(self):
        response = self.create_review()
        review_id = response.json()["id"]
        response = self.client.delete(self.url + review_id + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_rating_validator(self):
        product = Product.objects.create(
            owner=self.user, name="test", price=5.0)
        data = {"product_id": product.id, "rating": 6, "text": "Test review"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SupplierAPITest(APITestCase):
    url = "/api/v1/suppliers/"

    _user_creds = {
        "username": "abc",
        "password": "abc",
    }
    _superuser_creds = {
        "username": "def",
        "password": "def",
        "is_superuser": True,
    }

    def setUp(self):
        self.user = User.objects.create(**self._user_creds)
        self.token = Token(user=self.user)
        self.superuser = User.objects.create_superuser(**self._superuser_creds)
        self.superuser_token = Token(user=self.superuser)
        self.client.force_authenticate(user=self.user, token=self.token)

    def create_supplier(self):
        data = {"name": "Test Supplier", "phone": "88005553535"}
        response = self.client.post(self.url, data, format="json")
        return response

    def test_get_all_suppliers(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_supplier(self):
        response = self.create_supplier()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_supplier(self):
        response = self.create_supplier()
        supplier_id = response.json()["id"]
        response = self.client.get(self.url + supplier_id + "/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_supplier(self):
        response = self.create_supplier()
        supplier_id = response.json()["id"]
        data = {"name": "Updated Supplier", "phone": "88005553534"}
        response = self.client.put(
            self.url + supplier_id + "/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_supplier(self):
        response = self.create_supplier()
        supplier_id = response.json()["id"]
        response = self.client.delete(self.url + supplier_id + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_phone_validator(self):
        data = {"name": "Test Supplier", "phone": "12"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
