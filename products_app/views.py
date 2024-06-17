from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, UpdateView)
from django.views.generic.edit import FormMixin, ModelFormMixin
from rest_framework import permissions, views, viewsets
from rest_framework.authtoken.models import Token

from .forms import (ProductCreationForm, RegistrationForm, ReviewCreationForm,
                    SupplierRegistrationForm)
from .models import Category, Product, Review, Supplier
from .permissions import AdminOrReadOnly, UserAdminPermission
from .serializers import (CategorySerializer, ProductSerializer,
                          ReviewSerializer, SupplierSerializer)


class OwnerRequiredMixin(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    permission_classes = [UserAdminPermission]

    class Meta:
        abstract = True


class LoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')

    class Meta:
        abstract = True


class ProductViewSet(OwnerRequiredMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ReviewViewSet(OwnerRequiredMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class SupplierViewSet(OwnerRequiredMixin):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AdminOrReadOnly]


class UserRegistrationView(CreateView):
    template_name = 'registration/register.html'
    model = User
    form_class = RegistrationForm
    success_url = reverse_lazy('login')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('categories')


class CategoryListView(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'


class SupplierListView(ListView):
    model = Supplier
    template_name = 'suppliers.html'
    context_object_name = 'suppliers'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'supplier.html'


class AccountView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = User
    template_name = 'account.html'

    def get_object(self):
        return self.request.user


class SupplierCreate(LoginRequiredMixin, CreateView):
    template_name = 'forms/supplier_create.html'
    form_class = SupplierRegistrationForm
    success_url = reverse_lazy('account')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductCreate(LoginRequiredMixin, CreateView):
    template_name = 'forms/product_create.html'
    form_class = ProductCreationForm
    success_url = reverse_lazy('account')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        supplier_id = form.data['supplier']
        form.instance.supplier = Supplier.objects.filter(id=supplier_id).first()
        return super().form_valid(form)


class ReviewCreate(CreateView):
    template_name = 'forms/review_create.html'
    form_class = ReviewCreationForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        product_id = form.data['product_id']
        form.instance.product_id = Product.objects.filter(id=product_id).first()
        self.success_url = reverse_lazy('product', args=[product_id])
        return super().form_valid(form)


class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('account')


class ReviewDelete(LoginRequiredMixin, DeleteView):
    model = Review
    success_url = reverse_lazy('account')


class SupplierDelete(LoginRequiredMixin, DeleteView):
    model = Supplier
    success_url = reverse_lazy('account')


class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'forms/product_update.html'
    fields = ('name', 'price', 'category')
    success_url = reverse_lazy('account')


class ReviewUpdate(LoginRequiredMixin, UpdateView):
    model = Review
    template_name = 'forms/review_update.html'
    fields = ('rating', 'text')
    success_url = reverse_lazy('account')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        product_id = form.data['product_id']
        form.instance.product_id = Product.objects.filter(id=product_id).first()
        self.success_url = reverse_lazy('product', args=[product_id])
        return super().form_valid(form)

    
class SupplierUpdate(LoginRequiredMixin, UpdateView):
    model = Supplier
    template_name = 'forms/supplier_update.html'
    fields = ('name', 'phone')
    success_url = reverse_lazy('account')
