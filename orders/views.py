from http import HTTPStatus

import stripe
from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, TemplateView, ListView, DetailView

from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import Basket
from store import settings
from store.settings import DOMAIN_NAME, STRIPE_WEBHOOK_SECRET

stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.


class SuccessTemplateView(TitleMixin, TemplateView):
    title = "Store - Спасибо за заказ!"
    template_name = "orders/success.html"


class CanceledTemplateView(TitleMixin, TemplateView):
    template_name = "orders/canceled.html"


class OrderListView(TitleMixin, ListView):
    template_name = "orders/orders.html"
    title = "Store - orders"
    queryset = Order.objects.all()
    ordering = ("-created",)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderDetailView(DetailView):
    template_name = "orders/order.html"
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Store - Order #{self.object.id}"
        return context


class OrderCreateView(TitleMixin, CreateView):
    title = "Store - Оформление заказа"
    template_name = "orders/order-create.html"
    form_class = OrderForm
    success_url = reverse_lazy("orders:order_create")

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user = self.request.user)

        checkout_session = stripe.checkout.Session.create(
            line_items= baskets.stripe_products(),
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url="{}{}".format(settings.DOMAIN_NAME, reverse('orders:order_success')),
            cancel_url="{}{}".format(settings.DOMAIN_NAME, reverse('orders:order_canceled')),
        )

        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user

        return super().form_valid(form)


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        # line_items = session.line_items
        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.update_after_payment()
