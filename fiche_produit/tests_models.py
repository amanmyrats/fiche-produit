from django.test import TestCase
from .models import *

class ModelsTest(TestCase):
    def test_product(self):
        product = self.create_product()
        product_2 = self.create_product(name_fr=None)
        self.assertTrue(isinstance(product, Product))
        self.assertEqual(product.name_fr, 'Some french name')
        self.assertEqual(str(product), product.name_fr)

        self.assertTrue('object' in str(product_2))
        

    def test_productcard(self):
        fp = self.create_productcard()
        self.assertTrue(isinstance(fp, ProductCard))
        self.assertEqual(fp.product.name_fr, 'Some french name')

    def create_productcard(self):
        product = self.create_product()
        return ProductCard.objects.create(product=product)

    def create_product(self, desc_fr= 'Some french description', desc_en = 'Some english description',
                        desc_ru = 'Some russian description', desc_tm = 'Some turkmen description', 
                        name_fr = 'Some french name', name_en = 'Some english name', name_ru = 'Some russian name',
                        name_tm = 'Some turkmen name'):
        return Product.objects.create(desc_fr=desc_fr,
                desc_ru=desc_ru, desc_tm=desc_tm, desc_en=desc_en, 
                name_en = name_en, name_ru=name_ru, name_tm=name_tm,
                name_fr=name_fr)
