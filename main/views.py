from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from common.views import TitleMixin

from .models import Bag, Product


class IndexView(TitleMixin, TemplateView):
    template_name = 'main/index.html'
    title = 'Keramik'


class AboutView(TitleMixin, TemplateView):
    template_name = 'main/about.html'
    title = 'about'


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'main/shop.html'
    title = 'shop'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        context['products'] = Product.objects.all()
        return context


class PlateListView(ListView):
    model = Product
    template_name = 'main/plate_page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PlateListView, self).get_context_data()
        product_id = self.kwargs.get('product_id')
        context['title'] = Product.objects.filter(id=product_id).first().name.lower()
        context['product'] = Product.objects.get(id=product_id)
        return context


class BagView(TitleMixin, TemplateView):
    template_name = 'main/bag.html'
    title = 'bag'


@login_required
def bag_add(request, product_id):
    product = Product.objects.get(id=product_id)
    bags = Bag.objects.filter(user=request.user, product=product)

    if not bags.exists():
        Bag.objects.create(user=request.user, product=product, quantity=1)
    else:
        bag = bags.first()
        bag.quantity += 1
        bag.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def bag_remove(request, bag_id):
    bag = Bag.objects.get(id=bag_id)
    bag.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def bag_minus(request, bag_id):
    bag = Bag.objects.get(id=bag_id)
    if bag.quantity == 1:
        bag.delete()
    else:
        bag.quantity -= 1
        bag.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def bag_plus(request, bag_id):
    bag = Bag.objects.get(id=bag_id)
    product = Product.objects.get(id=bag.product_id)

    if product.quantity > bag.quantity:
        bag.quantity += 1
        bag.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
