"""App urls."""

from django.contrib.auth.views import LoginView
from django.urls import include, path, reverse_lazy

from . import views

urlpatterns = (
    path('', views.CategoryListView.as_view(), name='categories'),

    path('suppliers', views.SupplierListView.as_view(), name='suppliers'),
    path('supplier/<uuid:pk>', views.SupplierDetailView.as_view(), name='supplier'),
    path('supplier/create/', views.SupplierCreate.as_view(), name='create_supplier'),
    path('supplier/delete/<uuid:pk>', views.SupplierDelete.as_view(), name='delete_supplier'),
    path('supplier/update/<uuid:pk>', views.SupplierUpdate.as_view(), name='update_supplier'),

    path('category/<uuid:pk>', views.CategoryDetailView.as_view(), name='category'),

    path('product/<uuid:pk>', views.ProductDetailView.as_view(), name='product'),
    path('product/create/', views.ProductCreate.as_view(), name='create_product'),
    path('product/delete/<uuid:pk>', views.ProductDelete.as_view(), name='delete_product'),
    path('product/update/<uuid:pk>', views.ProductUpdate.as_view(), name='update_product'),

    path('review/create', views.ReviewCreate.as_view(), name='create_review'),
    path('review/delete/<uuid:pk>', views.ReviewDelete.as_view(), name='delete_review'),
    path('review/update/<uuid:pk>', views.ReviewUpdate.as_view(), name='update_review'),

    path('account/login/', LoginView.as_view(next_page=reverse_lazy('account')), name='login'),
    path('account/', include('django.contrib.auth.urls')),
    path('logout/', views.logout, name='logout'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('account/register/', views.UserRegistrationView.as_view(), name='register'),
)
