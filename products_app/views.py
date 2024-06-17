"""Views."""

from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from rest_framework import viewsets

from .forms import (ProductCreationForm, RegistrationForm, ReviewCreationForm,
                    SupplierRegistrationForm)
from .models import Category, Product, Review, Supplier
from .permissions import AdminOrReadOnly, UserAdminPermission
from .serializers import (CategorySerializer, ProductSerializer,
                          ReviewSerializer, SupplierSerializer)

ACCOUNT = 'account'


class Customloginrequiredmixin(LoginRequiredMixin):
    """Mixin for requiring login for views."""

    login_url = reverse_lazy('login')


def create_viewset(model, my_serializer, permissions=None):
    """Create a viewset for a given model and serializer.

    Args:
        model (django.db.models.Model): The Django model class.
        my_serializer (rest_framework.serializers.Serializer): Serializer class for the model.
        permissions (list, optional): List of permissions. Defaults to None.

    Returns:
        viewsets.ModelViewSet: Viewset class for the model.
    """
    class ViewSet(viewsets.ModelViewSet):
        """ViewSet class for CRUD operations on the model."""

        queryset = model.objects.all()
        serializer_class = my_serializer
        permission_classes = permissions if permissions else [UserAdminPermission]

        def perform_create(self, serializer):
            """
            Create method.

            Args:
                serializer: serializer for the model
            """
            if permissions:
                serializer.save()
            else:
                serializer.save(owner=self.request.user)

    return ViewSet


ProductViewSet = create_viewset(Product, ProductSerializer)
ReviewViewSet = create_viewset(Review, ReviewSerializer)
SupplierViewSet = create_viewset(Supplier, SupplierSerializer)
CategoryViewSet = create_viewset(Category, CategorySerializer, [AdminOrReadOnly])


class UserRegistrationView(CreateView):
    """View for user registration."""

    template_name = 'registration/register.html'
    model = User
    form_class = RegistrationForm
    success_url = reverse_lazy('login')


def logout(request):
    """
    Logout view.

    Args:
        request: logout request

    Returns:
        categories
    """
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('categories')


def create_list_view(model_class, template, context):
    """Create a list view for a given model class.

    Args:
        model_class (django.db.models.Model): The Django model class.
        template (str): Template name for rendering the view.
        context (str): Context object name for the template.

    Returns:
        - ListView: ListView class for the model.
    """
    class CustomListView(ListView):
        """ListView class for listing instances of the model."""

        model = model_class
        template_name = template
        context_object_name = context

    return CustomListView


CategoryListView = create_list_view(Category, 'categories.html', 'categories')
SupplierListView = create_list_view(Supplier, 'suppliers.html', 'suppliers')


class CategoryDetailView(DetailView):
    """View for displaying details of a category."""

    model = Category
    template_name = 'category.html'


class ProductDetailView(DetailView):
    """View for displaying details of a product."""

    model = Product
    template_name = 'product.html'


class SupplierDetailView(DetailView):
    """View for displaying details of a supplier."""

    model = Supplier
    template_name = 'supplier.html'


class AccountView(Customloginrequiredmixin, DetailView):
    """View for displaying account details."""

    login_url = reverse_lazy('login')
    model = User
    template_name = 'account.html'

    def get_object(self):
        """
        Get the user object for the authenticated user.

        Returns:
            user: the authenticated user
        """
        return self.request.user


class SupplierCreate(Customloginrequiredmixin, CreateView):
    """View for creating a new supplier."""

    template_name = 'forms/supplier_create.html'
    form_class = SupplierRegistrationForm
    success_url = reverse_lazy(ACCOUNT)

    def form_valid(self, form):
        """
        Validate and save the form data.

        Args:
            form: original form

        Returns:
            form: changed form
        """
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductCreate(Customloginrequiredmixin, CreateView):
    """View for creating a new product."""

    template_name = 'forms/product_create.html'
    form_class = ProductCreationForm
    success_url = reverse_lazy(ACCOUNT)

    def form_valid(self, form):
        """Validate and save the form data.

        Args:
            form: original form

        Returns:
            form: changed form
        """
        form.instance.owner = self.request.user
        supplier_id = form.data['supplier']
        form.instance.supplier = Supplier.objects.filter(id=supplier_id).first()
        return super().form_valid(form)


class ReviewCreate(CreateView):
    """View for creating a new review."""

    template_name = 'forms/review_create.html'
    form_class = ReviewCreationForm

    def form_valid(self, form):
        """Validate and save the form data.

        Args:
            form: original form

        Returns:
            form: changed form
        """
        form.instance.owner = self.request.user
        product_id = form.data['product_id']
        form.instance.product_id = Product.objects.filter(id=product_id).first()
        self.success_url = reverse_lazy('product', args=[product_id])
        return super().form_valid(form)


def create_delete_view(model_class):
    """Create a delete view for a given model class.

    Args:
        model_class (django.db.models.Model): The Django model class.

    Returns:
        DeleteView: DeleteView class for the model.
    """
    class CustomDeleteView(Customloginrequiredmixin, DeleteView):
        """DeleteView class for deleting an instance of the model."""

        model = model_class
        success_url = reverse_lazy(ACCOUNT)

    return CustomDeleteView


ProductDelete = create_delete_view(Product)
ReviewDelete = create_delete_view(Review)
SupplierDelete = create_delete_view(Supplier)


def create_update_view(model_class, template, fields_list):
    """Create an update view for a given model class.

    Args:
        model_class (django.db.models.Model): The Django model class.
        template (str): Template name for rendering the view.
        fields_list (tuple): Tuple of fields to be included in the form.

    Returns:
        - UpdateView: UpdateView class for updating an instance of the model.
    """
    class CustomUpdateView(Customloginrequiredmixin, UpdateView):
        """UpdateView class for updating an instance of the model."""

        model = model_class
        template_name = template
        fields = fields_list
        success_url = reverse_lazy(ACCOUNT)

    return CustomUpdateView


ProductUpdate = create_update_view(Product, 'forms/product_update.html',
                                   ('name', 'price', 'category'))
SupplierUpdate = create_update_view(Supplier, 'forms/supplier_update.html', ('name', 'phone'))


class ReviewUpdate(Customloginrequiredmixin, UpdateView):
    """View for updating a review."""

    model = Review
    template_name = 'forms/review_update.html'
    fields = ('rating', 'text')

    def form_valid(self, form):
        """
        Validate.

        Args:
            form: original form

        Returns:
            form: changed form
        """
        form.instance.owner = self.request.user
        product_id = form.data['product_id']
        form.instance.product_id = Product.objects.filter(id=product_id).first()
        self.success_url = reverse_lazy('product', args=[product_id])
        return super().form_valid(form)
