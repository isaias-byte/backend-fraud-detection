from django.urls import path, include
from . import views
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'transactions', views.TransactionViewSet)

urlpatterns = [
    path('transactions/', views.transactions, name='transactions'),
    path('create-transaction/', views.create_transaction, name='create_transaction'),
    path('update-transaction/<int:id>/', views.update_transaction, name='update_transaction'),
    path('delete-transaction/<int:id>/', views.delete_transaction, name='delete_transaction'),
]
# The last line is for serving media files during development.