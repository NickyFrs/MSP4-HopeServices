from django.shortcuts import render, get_object_or_404

# store views from here.
from store.models import Product, Category


def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})


def all_products(request):
    # grab what to show
    products = Product.objects.all()
    return render(request, 'store/lessons/all.html', {'products': products})


def categories(request):
    return {
        'categories': Category.objects.all()
    }


def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/lessons/lessons.html', {'category': category, 'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, active=True)
    return render(request, 'store/lessons/detail.html', {'product': product})