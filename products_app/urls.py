from django.urls import path
from . import views

urlpatterns = (
    path("", views.CategoryListView.as_view(), name='categories'),
    path("suppliers", views.SupplierListView.as_view(), name='suppliers'),
    path("supplier/<uuid:pk>", views.SupplierDetailView.as_view(), name='supplier'),
    path("category/<uuid:pk>", views.CategoryDetailView.as_view(), name='category'),
    path("product/<uuid:pk>", views.ProductDetailView.as_view(), name='product'),
    path("account/", views.AccountView.as_view(), name='account'),
    path("register/", views.UserRegistrationView.as_view(), name='register'),
    path("login/", views.UserLoginView.as_view(), name='login'),
)
