from django.test import TestCase
from django.test import Client
from fiche_produit.models import Product

class TestTest(TestCase):
    def setUp(self):
        Product.objects.create(name_fr='product1')
        Product.objects.create(name_fr='product2')
    
    def testSiteView(self):
        self.client = Client()
        products = self.client.get('/api/products/')
        self.assertEqual(len(products.json()),2)