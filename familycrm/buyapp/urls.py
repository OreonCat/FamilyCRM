from django.urls import path
from buyapp import views

app_name = 'buyapp'
urlpatterns = [
    path('', views.ShoppingListView.as_view(), name='index'),
    path('products', views.ProductListView.as_view(), name='products'),
    path('products/add', views.AddProductView.as_view(), name='add_product'),
    path('products/<int:pk>', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/edit', views.EditProductView.as_view(), name='edit_product'),
    path('products/<int:pk>/delete', views.DeleteProductView.as_view(), name='delete_product'),
    path('shopping_list/<int:pk>', views.ShoppingListDetailView.as_view(), name='shopping_list_detail'),
    path('shopping_list/add', views.AddShoppingListView.as_view(), name='add_shopping_list'),
    path('shopping_list/<int:pk>/add_to_cart', views.AddToCart.as_view(), name='add_to_cart'),
    path('shopping_list/<int:pk>/add_to_cart/<int:product>', views.AddToCartLogic.as_view(), name='add_to_cart_logic'),
    path('shopping_list/<int:pk>/buy/<int:cart>', views.BuyCartLogic.as_view(), name='buy_cart'),
    path('shopping_list/<int:pk>/cancel/<int:cart>', views.CancelCartLogic.as_view(), name='cancel_cart'),
    path('shopping_list/<int:pk>/done', views.DoneListLogic.as_view(), name='done_list'),
]