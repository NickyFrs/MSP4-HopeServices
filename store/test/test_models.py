from django.test import TestCase
from django.contrib.auth.models import User

from store.models import Category, Product


class CategoryModelTest(TestCase):

    # create the entries into the testing DB to be used for testing
    def setUp(self):
        self.data1 = Category.objects.create(name='music lessons', slug='music-lessons')

    # the test functions
    def test_category_model_entry(self):
        """
        Test Category model model data insertion/types/field attribute
        """
        data = self.data1  # data entered from setUp above
        self.assertTrue(isinstance(data, Category))

    def test_category_models_return(self):
        """
        Test Category model return
        """
        data = self.data1
        self.assertEqual(str(data), 'music lessons')

    class TestProductModel(TestCase):

        # create the entries into the testing DB to be used for testing
        def setUp(self):
            Category.objects.create(name='music-lessons', slug='music-lessons')
            User.objects.create(username='admin')

            self.data1 = Product.objects.create(category_id=1, name='piano-lessons',
                                                created_by_id=1, slug='piano-lessons-beginners',
                                                price='20.00', active=True
                                                )

        def test_product_model_entry(self):
            """
            Test Category model model data insertion/types/field attribute
            """
            data = self.data1
            self.assertTrue(isinstance(data, Product))
            self.assertEqual(str(data), 'piano-lessons')