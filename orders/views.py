from django.http.response import JsonResponse

from basket.basket import Basket
from .models import Orders, OrderItem


# views from here.


def add(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":

        order_key = request.POST.get("order_key")
        user_id = request.user.id
        baskettotal = basket.get_total_price()

        # to check if order exists
        if Orders.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Orders.objects.create(
                user_id=user_id,
                full_name="name",
                address1="add1",
                address2="add2",
                total_paid=baskettotal,
                order_key=order_key,
            )
            order_id = order.pk
            for item in basket:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["qty"],
                )

        response = JsonResponse({"success": "All done"})
        return response


# to change the payment status to True
def payment_confirmation(data):
    Orders.objects.filter(order_key=data).update(billing_status=True)


def user_orders(request):
    user_id = request.user.id
    orders = Orders.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders
