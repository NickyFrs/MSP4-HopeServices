from importlib import import_module

from django.http import HttpRequest
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

from store.views import all_products
from store.models import Category, Product


# tests from here.


class TestViewResponses(TestCase):

    # create the entries into the testing DB to be used for testing
    def setUp(self):
        self.c = Client()
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

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get("/")
        self.assertEqual(response.status_code, 200)
        response = self.c.get("/", HTTP_HOST="")
        self.assertEqual(response.status_code, 200)
        response = self.c.get("/", HTTP_HOST="myshop.com")
        self.assertEqual(response.status_code, 400)

    def test_product_details_url(self):
        """
        Test product detail url status
        """
        response = self.c.get(
            reverse("store:product_detail", args=["piano-lessons-beginners"])
        )
        self.assertEqual(response.status_code, 200)

    def test_categories_url(self):
        """
        Test categories url status response
        """
        response = self.c.get(reverse("store:category_list", args=["music-lessons"]))
        self.assertEqual(response.status_code, 200)

    def test_home_html(self):
        request = HttpRequest()

        # session engine allow us to simulate a new session within the request
        engine = import_module(settings.SESSION_ENGINE)
        request.session = engine.SessionStore()

        response = all_products(request)
        html = response.content.decode("utf8")
        print(html)
        self.assertIn("<title>Home</title>", html)
        self.assertTrue(html.startswith("\n<!doctype html\n"))
        self.assertEqual(response.status_code, 200)
