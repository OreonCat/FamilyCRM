from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, RedirectView
from django.db import models

from buyapp.models import ShoppingList, Product, CheckCart


#Покупки
class ShoppingListView(ListView):
    model = ShoppingList
    context_object_name = 'old_list'
    template_name = 'buyapp/index.html'
    paginate_by = 20

    def get_queryset(self):
        return ShoppingList.objects.exclude(status=ShoppingList.Status.ACTUAL)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['actual_list'] = ShoppingList.objects.filter(status=ShoppingList.Status.ACTUAL)
        context['title'] = 'Покупки'
        return context

class ShoppingListDetailView(DetailView):
    model = ShoppingList
    context_object_name = 'list'
    template_name = 'buyapp/shopping_list_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.time_created
        context['cart'] = self.object.check_cart_list.all()
        context['cart_sum'] = CheckCart.get_product_sum(context['cart'])
        return context

class AddShoppingListView(LoginRequiredMixin, CreateView):
    model = ShoppingList
    context_object_name = 'new_list'
    template_name = 'buyapp/add_shopping_list.html'
    fields = {'user_from',  'user_to'}
    field_order = ['user_from', 'user_to']
    extra_context  = {'title': 'Добавить список'}

    def form_valid(self, form):
        form.instance.status = ShoppingList.Status.ACTUAL
        form.save()
        return super().form_valid(form)

class AddToCart(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'buyapp/add_to_cart.html'
    context_object_name = 'object'
    extra_context = {'title': "Добавить продукт в лист"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = self.kwargs['pk']
        return context

    def get_queryset(self):
        cart = CheckCart.objects.filter(list=self.kwargs['pk'])
        list_of_cart = cart.values_list('product', flat=True)
        return Product.objects.exclude(id__in=list_of_cart)

class AddToCartLogic(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = False
    def get_redirect_url(self, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs['product'])
        list_of = ShoppingList.objects.get(id=self.kwargs['pk'])
        cart = CheckCart(product=product, list=list_of, status=CheckCart.Status.ACTUAL)
        cart.save()
        return reverse_lazy('buyapp:add_to_cart', kwargs={'pk': self.kwargs['pk']})

class BuyCartLogic(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = False
    def get_redirect_url(self, *args, **kwargs):
        Cart = CheckCart.objects.get(id=self.kwargs['cart'])
        Cart.status = Cart.Status.BOUGHT
        Cart.save()
        return reverse_lazy('buyapp:shopping_list_detail', kwargs={'pk': self.kwargs['pk']})

class CancelCartLogic(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = False
    def get_redirect_url(self, *args, **kwargs):
        Cart = CheckCart.objects.get(id=self.kwargs['cart'])
        Cart.status = Cart.Status.CANCELED
        Cart.save()
        return reverse_lazy('buyapp:shopping_list_detail', kwargs={'pk': self.kwargs['pk']})

class DoneListLogic(LoginRequiredMixin, RedirectView):
    permanent = False
    query_string = False
    def get_redirect_url(self, *args, **kwargs):
        shop_list = ShoppingList.objects.get(id=self.kwargs['pk'])
        cart = shop_list.check_cart_list.filter(status=ShoppingList.Status.BOUGHT)
        if cart:
            shop_list.status = ShoppingList.Status.BOUGHT
        else:
            shop_list.status = ShoppingList.Status.CANCELED
        shop_list.save()
        return reverse_lazy('buyapp:shopping_list_detail', kwargs={'pk': self.kwargs['pk']})

#Продукты
class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'buyapp/product_list.html'
    extra_context = {
        'title': "Продукты"
    }

class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    fields = '__all__'
    template_name = 'buyapp/add_product.html'
    success_url = reverse_lazy('buyapp:products')
    extra_context = {
        'title': "Добавить продукт"
    }

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'buyapp/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context

class EditProductView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = '__all__'
    template_name = 'buyapp/edit_product.html'
    extra_context = {
        'title': "Редактировать продукт"
    }

class DeleteProductView(LoginRequiredMixin,DeleteView):
    model = Product
    template_name = 'buyapp/delete_product.html'
    success_url = reverse_lazy('buyapp:products')
    extra_context = {
        'title': "Удалить продукт"
    }