from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from store.models import Product
from .basket import Basket


# views from here.


def basket_review(request):
    basket = Basket(request) # making an instance of the class Basket in basket.py
    return render(request, 'basket/review.html', {'basket': basket})
