import json
import stripe

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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

    return render(request, 'payment/pay.html', {'client_secret': intent.client_secret})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)


def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')


