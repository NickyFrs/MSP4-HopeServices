from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from store.models import Category, Product


# Test codes from here.


class TestBasketViews(TestCase):
    def setUp(self):
        Category.objects.create(name="music-lessons", slug="music-lessons")
        User.objects.create(username="admin")
        Product.objects.create(
            category_id=1,
            name="piano-lessons",
            created_by_id=1,
            slug="piano-lessons-beginners",
            price="20.00",
            active=True,
        )
        Product.objects.create(
            category_id=1,
            name="flute-lessons",
            created_by_id=1,
            slug="flute-lessons-beginners",
            price="20.00",
            active=True,
        )
        Product.objects.create(
            category_id=1,
            name="violin-lessons",
            created_by_id=1,
            slug="violin-lessons-beginners",
            price="20.00",
            active=True,
        )
        self.client.post(
            reverse("basket:basket_add"),
            {"productid": 1, "productqty": 1, "action": "post"},
            xhr=True,
        )
        self.client.post(
            reverse("basket:basket_add"),
            {"productid": 2, "productqty": 2, "action": "post"},
            xhr=True,
        )
        # xhr = XMLHttpRequest an API in the form of an object to transfer data front and backend.

    def test_basket_url(self):
        """
        Test homepage
        """
        response = self.client.get(reverse("basket:basket_review"))
        self.assertEqual(response.status_code, 200)

    def test_basket_add(self):
        """
        Test adding to basket
        """

        response = self.client.post(
            reverse("basket:basket_add"),
            {"product": 3, "productqty": 1, "action": "post"},
            xhr=True,
        )
        self.assertEqual(response.json(), {"qty": 4})

        response = self.client.post(
            reverse("basket:basket_add"),
            {"productid": 2, "productqty": 1, "action": "post"},
            xhr=True,
        )
        self.assertEqual(response.json(), {"qty": 3})

    def test_basket_delete(self):
        """
        Test deleting from basket
        """
        response = self.client.post(
            reverse("basket:basket_delete"),
            {"productid": 2, "action": "post"},
            xhr=True,
        )
        self.assertEqual(response.json(), {"qty": 1, "subtotal": 20.00})

    def test_basket_update(self):
        """
        Test Updating basket
        """
        response = self.client.post(
            reverse("basket:basket_update"),
            {"productid": 2, "productqty": 1, "action": "post"},
            xhr=True,
        )
        self.assertEqual(response.json(), {"qty": 2, "subtotal": 40.0})
