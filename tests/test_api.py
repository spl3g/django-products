"""API tests."""

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

USERNAME_NAME = 'username'
PSSWORD_NAME = 'password'
NAME = 'name'
ID = 'id'
SLASH = '/'
DESCRIPTION = 'description'
PHONE = 'phone'
PRICE = 'price'

user_creds = {
    USERNAME_NAME: 'abc',
    PSSWORD_NAME: 'abc',
}

superuser_creds = {
    USERNAME_NAME: 'def',
    PSSWORD_NAME: 'def',
    'is_superuser': True,
}


class CategoryAPITest(APITestCase):
    """Test suite for the Category API endpoints."""

    url = '/api/v1/categories/'

    def setUp(self):
        """Set up the test case with a regular user and a superuser."""
        self.user = User.objects.create(**user_creds)
        self.token = Token(user=self.user)
        self.superuser = User.objects.create_superuser(**superuser_creds)
        self.superuser_token = Token(user=self.superuser)
        self.client.force_authenticate(
            user=self.superuser, token=self.superuser_token)

    def create_category(self):
        """
        Help method to create a test category.

        Returns:
            post
        """
        jdata = {NAME: 'TestCategory', DESCRIPTION: 'Test description'}
        return self.client.post(self.url, jdata)

    def test_get_all_categories(self):
        """Ensure we can retrieve all categories."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category(self):
        """Ensure we can create a new category."""
        response = self.create_category()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_category(self):
        """Ensure we can retrieve a single category by its ID."""
        category = self.create_category().json()[ID]
        response = self.client.get(self.url + category + SLASH)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category(self):
        """Ensure we can update an existing category."""
        category = self.create_category().json()[ID]
        jdata = {NAME: 'Updated Category', DESCRIPTION: 'Updated description'}
        response = self.client.put(self.url + category + SLASH, jdata)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        """Ensure we can delete a category."""
        category = self.create_category().json()[ID]
        response = self.client.delete(self.url + category + SLASH)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProductAPITest(APITestCase):
    """Test suite for the Product API endpoints."""

    category_url = '/api/v1/categories/'
    supplier_url = '/api/v1/suppliers/'
    url = '/api/v1/products/'

    def setUp(self):
        """
        Set up the test case with a regular user and a superuser.

        Create a test supplier.
        """
        self.user = User.objects.create(**user_creds)
        self.token = Token(user=self.user)
        self.superuser = User.objects.create_superuser(**superuser_creds)
        self.superuser_token = Token(user=self.superuser)
        self.client.force_authenticate(user=self.user, token=self.token)
        jdata = {NAME: 'TestSupplier', PHONE: '88005553535'}
        self.supplier = self.client.post(self.supplier_url, jdata)

    def create_category(self):
        """
        Help method to create a test category.

        Returns:
            - return: post response
        """
        self.client.force_authenticate(user=self.superuser, token=self.superuser_token)
        jdata = {NAME: 'Test Category', DESCRIPTION: 'Test description'}
        response = self.client.post(self.category_url, jdata)
        self.client.force_authenticate(user=self.user, token=self.token)
        return response

    def create_product(self):
        """
        Help method to create a test product.

        Returns:
            - return: post response
        """
        category = self.create_category().json()[ID]
        supplier = self.supplier.json()[ID]

        jdata = {NAME: 'Test Product', PRICE: 10, 'category': category, 'supplier': supplier}
        return self.client.post(self.url, jdata)

    def test_get_all_products(self):
        """Ensure we can retrieve all products."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_product(self):
        """Ensure we can create a new product."""
        response = self.create_product()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_product(self):
        """Ensure we can retrieve a single product by its ID."""
        response = self.create_product()
        product_id = response.json()[ID]
        response = self.client.get(self.url + product_id + SLASH)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product(self):
        """Ensure we can update an existing product."""
        category_id = self.create_category().json()[ID]
        product_id = self.create_product().json()[ID]
        supplier_id = self.supplier.json()[ID]

        jdata = {
            NAME: 'Updated Product',
            PRICE: 20,
            'category': category_id,
            'supplier': supplier_id,
        }
        response = self.client.put(self.url + product_id + SLASH, jdata)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product(self):
        """Ensure we can delete a product."""
        response = self.create_product()
        product_id = response.json()[ID]
        response = self.client.delete(self.url + product_id + SLASH)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_price_validator(self):
        """Ensure the price validator works as expected."""
        jdata = {NAME: 'Test Product', PRICE: -10}
        response = self.client.post(self.url, jdata)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReviewAPITest(APITestCase):
    """Test suite for the Review API endpoints."""

    url = '/api/v1/reviews/'
    category_url = '/api/v1/categories/'
    product_url = '/api/v1/products/'
    supplier_url = '/api/v1/suppliers/'

    def setUp(self):
        """Set up the test case with a regular user and a superuser."""
        self.user = User.objects.create(**user_creds)
        self.token = Token(user=self.user)
        self.superuser = User.objects.create_superuser(**superuser_creds)
        self.superuser_token = Token(user=self.superuser)
        self.client.force_authenticate(user=self.user, token=self.token)

    def create_supplier(self):
        """
        Help method to create a test supplier.

        Returns:
            - return: post response
        """
        jdata = {NAME: 'Test Supplier', PHONE: '88005553535'}
        return self.client.post(self.supplier_url, jdata)

    def create_category(self):
        """
        Help method to create a test category.

        Returns:
            - return: post response
        """
        self.client.force_authenticate(user=self.superuser, token=self.superuser_token)
        jdata = {NAME: 'Test Category', DESCRIPTION: 'Test description'}
        response = self.client.post(self.category_url, jdata)
        self.client.force_authenticate(user=self.user, token=self.token)
        return response

    def create_product(self):
        """
        Help method to create a test product.

        Returns:
            - return: post response
        """
        category = self.create_category().json()[ID]
        supplier = self.create_supplier().json()[ID]

        jdata = {NAME: 'Test Product', PRICE: 10, 'category': category, 'supplier': supplier}
        return self.client.post(self.product_url, jdata)

    def create_review(self):
        """
        Help method to create a test review.

        Returns:
            - return: post response
        """
        product_id = self.create_product().json()[ID]

        jdata = {'product_id': product_id, 'rating': 5, 'text': 'Test review'}
        return self.client.post(self.url, jdata)

    def test_get_all_reviews(self):
        """Ensure we can retrieve all reviews."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_review(self):
        """Ensure we can create a new review."""
        response = self.create_review()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_review(self):
        """Ensure we can retrieve a single review by its ID."""
        response = self.create_review()
        review_id = response.json()[ID]
        response = self.client.get(self.url + review_id + SLASH)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_review(self):
        """Ensure we can update an existing review."""
        response = self.create_review()
        review_id = response.json()[ID]
        jdata = {'rating': 4, 'text': 'Updated review'}
        response = self.client.patch(self.url + review_id + SLASH, jdata)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_review(self):
        """Ensure we can delete a review."""
        response = self.create_review()
        review_id = response.json()[ID]
        response = self.client.delete(self.url + review_id + SLASH)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_rating_validator(self):
        """Ensure the rating validator works as expected."""
        product_id = self.create_product().json()[ID]
        jdata = {'product_id': product_id, 'rating': 6, 'text': 'Test review'}
        response = self.client.post(self.url, jdata)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SupplierAPITest(APITestCase):
    """Test suite for the Supplier API endpoints."""

    url = '/api/v1/suppliers/'

    def setUp(self):
        """Set up the test case with a regular user and a superuser."""
        self.user = User.objects.create(**user_creds)
        self.token = Token(user=self.user)
        self.superuser = User.objects.create_superuser(**superuser_creds)
        self.superuser_token = Token(user=self.superuser)
        self.client.force_authenticate(user=self.user, token=self.token)

    def create_supplier(self):
        """
        Help method to create a test supplier.

        Returns:
            post
        """
        jdata = {NAME: 'Test Supplier', PHONE: '88005553535'}
        return self.client.post(self.url, jdata)

    def test_get_all_suppliers(self):
        """Ensure we can retrieve all suppliers."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_supplier(self):
        """Ensure we can create a new supplier."""
        response = self.create_supplier()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_single_supplier(self):
        """Ensure we can retrieve a single supplier by its ID."""
        response = self.create_supplier()
        supplier_id = response.json()[ID]
        response = self.client.get(self.url + supplier_id + SLASH)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_supplier(self):
        """Ensure we can update an existing supplier."""
        response = self.create_supplier()
        supplier_id = response.json()[ID]
        jdata = {NAME: 'Updated Supplier', PHONE: '88005553534'}
        response = self.client.put(self.url + supplier_id + SLASH, jdata)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_supplier(self):
        """Ensure we can delete a supplier."""
        response = self.create_supplier()
        supplier_id = response.json()[ID]
        response = self.client.delete(self.url + supplier_id + SLASH)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_phone_validator(self):
        """Ensure the phone number validator works as expected."""
        jdata = {NAME: 'Test Supplier', PHONE: '12'}
        response = self.client.post(self.url, jdata)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
