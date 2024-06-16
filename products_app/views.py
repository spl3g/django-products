from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from rest_framework import viewsets, views
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, FormView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import auth
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from .models import Product, Category, Supplier, Review
from .permissions import UserAdminPermission, AdminOrReadOnly
from .forms import RegistrationForm
from .serializers import (
    ProductSerializer,
    ReviewSerializer,
    SupplierSerializer,
    CategorySerializer,
)


class OwnerRequiredMixin(viewsets.ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    permission_classes = [UserAdminPermission]

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


class UserRegistrationView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return views.Response(
                {'error': 'Username and password are required'},
                status=views.status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.filter(username=username).first()
        if user is None:
            user = User.objects.create_user(
                username=username, password=password)
            token = Token.objects.create(user=user)
        else:
            return views.Response(
                {'error': 'User already exists'},
                status=views.status.HTTP_400_BAD_REQUEST,
            )
        auth.login(request=request, user=user)
        return views.Response({'token': token.key}, status=views.status.HTTP_200_OK)

    def get(self, request):
        return render(request, 'register.html')


class UserLoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return views.Response(
                {'error': 'Username and password are required'},
                status=views.status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.filter(username=username).first()
        if user is None:
            return views.Response(
                {'error': 'User does not exist'},
                status=views.status.HTTP_400_BAD_REQUEST,
            )
        else:
            user = auth.authenticate(username=username, password=password)
            if user is None:
                return views.Response(
                    {'error': 'Wrong password'},
                    status=views.status.HTTP_400_BAD_REQUEST,
                )
            token, _ = Token.objects.get_or_create(user=user)
        auth.login(request=request, user=user)
        return views.Response({'token': token.key}, status=views.status.HTTP_200_OK)

    def get(self, request):
        return render(request, 'login.html')


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('main_page')


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


class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'supplier.html'


class AccountView(DetailView):
    model = User
    template_name = 'account.html'

    def get_object(self):
        return self.request.user
