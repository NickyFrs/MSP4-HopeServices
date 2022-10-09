from decimal import Decimal

from django.conf import settings

from store.models import Product


class Basket():
    """
    Basket configuration. User Session check and/or creation.
    Default behavior.
    """
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket