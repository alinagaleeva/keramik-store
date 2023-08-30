from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from common.views import TitleMixin

from .forms import OrderForm
from .models import Order


class ShippingView(TitleMixin, CreateView):
    template_name = 'orders/shipping.html'
    form_class = OrderForm
    success_url = reverse_lazy('payment_confirmation')
    title = 'shipping'

    def post(self, request, *args, **kwargs):
        super(ShippingView, self).post(request, *args, **kwargs)
        order_id = int(self.object.id)
        order = Order.objects.get(id=order_id)
        order.update_after_payment()
        return HttpResponseRedirect(reverse('payment_confirmation'))

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(ShippingView, self).form_valid(form)


class PaymentConfirmationView(TitleMixin, TemplateView):
    template_name = 'orders/payment_confirmation.html'
    title = 'payment confirmation'


class OrdersProfileView(TitleMixin, ListView):
    model = Order
    template_name = 'orders/orders.html'
    title = 'orders'

    def get_context_data(self,  *, object_list=None, **kwargs):
        context = super(OrdersProfileView, self).get_context_data()
        context['data'] = Order.objects.filter(initiator=self.request.user).last()
        return context
