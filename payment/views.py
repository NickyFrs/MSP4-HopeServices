import json
import stripe

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from basket.basket import Basket
from orders.views import payment_confirmation
from env import STRIPE_SK

# views from here.



@login_required
def BasketView(request):
    basket = Basket(request)
    # turn the decimal figure from total price in to a string for strips intent
    total = str(basket.get_total_price())
    # to replace the dot in the decimal figure with nothing
    total = total.replace('.', '')
    # now tun it back into an integer
    total = int(total)

    # grab the public key from stripe
    stripe.api_key = STRIPE_SK

    # and create a payment intent
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='gbp',
        metadata={'userid': request.user.id}
    )

    return render(request, 'payment/pago.html', {'client_secret': intent.client_secret})