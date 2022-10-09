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

        # function to create the class iterable
        def __iter__(self):
            """
            Make the class iterable
            """
            product_ids = self.basket.keys()
            products = Product.products.filter(id__in=product_ids)
            basket = self.basket.copy()

            for product in products:
                basket[str(product.id)]['product'] = product

            for item in basket.values():
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['qty']
                yield item

        # function to calculate the quantity with the basket
        def __len__(self):
            """
            get basket data and count the qty of items in the basket
            """
            return sum(int(item['qty']) for item in self.basket.values())

        def add(self, product, qty):
            """
            Function to add the data of user's basket session
            """
            product_id = product.id
            if product_id not in self.basket:
                self.basket[product_id] = {'price': str(product.price), 'qty': int(qty)}
            self.save()

        def update(self, product, qty):
            """
            Update items values in the basket in the session data
            """
            product_id = str(product)

            if product_id in self.basket:
                self.basket[product_id]['qty'] = qty
            else:
                self.basket[product_id] = {'price': str(product.price), 'qty': qty}
            self.save()

        def delete(self, product):
            """
            Delete items from the basket from the session data
            """
            product_id = str(product)

            if product_id in self.basket:
                del self.basket[product_id]

            self.save()

        # save session changes
        def save(self):
            """
            save session changes
            """
            self.session.modified = True

        def get_total_price(self):

            subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

            # for the total if shipping price wanted
            if subtotal == 0:
                shipping = Decimal(0.00)
            else:
                shipping = Decimal(0.00)
            total = subtotal + Decimal(shipping)
            return total

        def clear(self):
            """
            Remove all items from the basket session
            """
            del self.session[settings.BASKET_SESSION_ID]
            self.save()

    """
    Code in this file has been inspired/reworked from other known works. Plese ensure that
    the License below is included in any of your work that is directly copied from
    this source file.
    MIT License
    Copyright (c) 2019 Packt
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NON INFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    """
