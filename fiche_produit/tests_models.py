from os import name
from django.test import TestCase
from .models import *

class ModelsTest(TestCase):
    def test_product(self):
        product = self.create_product()
        product2 = self.create_product(name_fr=None)
        self.assertTrue(isinstance(product, Product))
        self.assertEqual(product.name_fr, 'Some french name')
        self.assertEqual(str(product), product.name_fr)
        self.assertEqual('No image', product.image_url)
        self.assertEqual('No technical detail', product.technical_detail_url)
        self.assertTrue('object' in str(product2))
 
    def test_productcard(self):
        
        fp = self.create_productcard()
        fp2 = self.create_productcard2()
        self.assertTrue(isinstance(fp, ProductCard))
        self.assertTrue(isinstance(fp2, ProductCard))
        self.assertEqual(fp.product.name_fr, 'Some french name')
        self.assertEqual(fp2.product.name_fr, None)
        self.assertEqual('CRA - 10001 - Some french name',str(fp))
        self.assertTrue('object' in str(fp2))
    

    def test_lot(self):
        lot = self.create_lot()
        lot2 = self.create_lot(name_fr=None)
        lot3 = self.create_lot(number=None, name_fr=None)
        self.assertEqual(str(lot), '02 - Lot name in french')
        self.assertTrue(isinstance(lot, Lot))
        self.assertTrue(isinstance(lot2, Lot))
        self.assertTrue('02' in str(lot2))
        self.assertTrue('object' in str(lot3))

    def test_unit(self):
        unit = self.create_unit()
        unit2 = self.create_unit(name_fr=None)
        self.assertEqual(str(unit), 'ens')
        self.assertTrue(isinstance(unit, Unit))
        self.assertTrue(isinstance(unit2, Unit))
        self.assertTrue('object' in str(unit2))

    def test_currency(self):
        currency = self.create_currency()
        currency2 = self.create_currency(short_name_fr=None)
        self.assertEqual(str(currency), 'USD')
        self.assertTrue(isinstance(currency, Currency))
        self.assertTrue(isinstance(currency2, Currency))
        self.assertTrue('object' in str(currency2))

    def test_package_type(self):
        pt = self.create_package_type()
        pt2 = self.create_package_type(name_fr=None)
        self.assertTrue(isinstance(pt, PackageType))
        self.assertTrue(isinstance(pt2, PackageType))
        self.assertEqual(str(pt), 'pallete')
        self.assertTrue('object' in str(pt2))

    def test_project(self):
        project = self.create_project()
        project2 = self.create_project(code=None, name_fr=None)
        self.assertTrue(isinstance(project, Project))
        self.assertTrue(isinstance(project2, Project))
        self.assertEqual(str(project), 'CRA')
        self.assertTrue('object' in str(project2))
        self.assertEqual(project.total_sum, 0)
    
    def test_provider(self):
        provider = self.create_provider()
        provider2 = self.create_provider(code=None, name_fr=None)
        self.assertTrue(isinstance(provider, Provider))
        self.assertTrue(isinstance(provider2, Provider))
        self.assertEqual('Epoca company', str(provider))
        self.assertTrue('object' in str(provider2))

    def test_country(self):
        country = self.create_country()
        country2 = self.create_country(code=None, name_fr=None)
        self.assertTrue(isinstance(country, Country))
        self.assertTrue(isinstance(country2, Country))
        self.assertEqual('Turkmenistan', str(country))
        self.assertTrue('object' in str(country2))

    def test_room(self):
        room = self.create_room()
        room2 = self.create_room(no=None, name_fr=None)
        self.assertTrue(isinstance(room, Room))
        self.assertTrue(isinstance(room2, Room))
        self.assertEqual('A1.01 - Office', str(room))
        self.assertTrue('object' in str(room2))

    def test_client(self):
        client = self.create_client()
        client2 = self.create_client(name_fr=None)
        self.assertTrue(isinstance(client, Client))
        self.assertTrue(isinstance(client2, Client))
        self.assertEqual('Mammet', str(client))
        self.assertTrue('object' in str(client2))
    
    def test_employee(self):
        employee = self.create_employee()
        employee2 = self.create_employee(name_fr=None)
        self.assertTrue(isinstance(employee, Employee))
        self.assertTrue(isinstance(employee2, Employee))
        self.assertEqual('Aman', str(employee))
        self.assertTrue('object' in str(employee2))

    def test_phase(self):
        phase = self.create_phase()
        phase2 = self.create_phase(name=None)
        self.assertTrue(isinstance(phase, Phase))
        self.assertTrue(isinstance(phase2, Phase))
        self.assertEqual('GO', str(phase))
        self.assertTrue('object' in str(phase2))

    def test_trade(self):
        trade = self.create_trade()
        trade2 = self.create_trade(name_fr=None)
        self.assertTrue(isinstance(trade, Trade))
        self.assertTrue(isinstance(trade2, Trade))
        self.assertEqual('CEA', str(trade))
        self.assertTrue('object' in str(trade2))

    def test_department(self):
        department = self.create_department()
        department2 = self.create_department(name=None)
        self.assertTrue(isinstance(department, Department))
        self.assertTrue(isinstance(department2, Department))
        self.assertEqual('QS', str(department))
        self.assertTrue('object' in str(department2))

    def test_annexe5(self):
        project = self.create_project()
        project2 = self.create_project(code=None, name_fr=None)
        annexe5 = self.create_annexe5(project=project)
        annexe52 = self.create_annexe5(project=project2, code=None, name_fr=None)
        self.assertTrue(isinstance(annexe5, Annexe5))
        self.assertTrue(isinstance(annexe52, Annexe5))
        self.assertEqual('70.311 - Meuble', str(annexe5))
        self.assertTrue('object' in str(annexe52))
        self.assertEqual(50, annexe5.total_price)
        try:
            annexe53 = self.create_annexe5(quantity='', unit_price='')
            self.assertEqual(0, annexe53.total_price)
        except:
            pass
        
    def test_orderitem(self):
        project = self.create_project()
        order=self.create_order(number=3356, project=project)
        product_card = self.create_productcard(number=10002)

        orderitem = self.create_orderitem(no=2, order=order, product_card=product_card, quantity=5, price=10)
        orderitem2 = self.create_orderitem()
        orderitem3 = self.create_orderitem(no=3, order=None, product_card=None)

        self.assertTrue(isinstance(orderitem, OrderItem))
        self.assertTrue(isinstance(orderitem2, OrderItem))
        self.assertTrue(isinstance(orderitem3, OrderItem))
        self.assertEqual('3356 - 2 - None', str(orderitem))
        self.assertTrue('Empty item' in str(orderitem2))
        self.assertTrue('Empty item' in str(orderitem3))
        self.assertEqual(50, orderitem.total_price )
        try:
            orderitem4 = self.create_orderitem(quantity='', price='')
            self.assertEqual(0, orderitem4.total_price)
        except:
            pass
    
    def test_order(self):
        project = self.create_project()
        order = self.create_order(number=3333, project=project)
        order2 = self.create_order()
        product_card=self.create_productcard(number=20001)
        orderitem = self.create_orderitem(no=5, order=order, product_card=product_card)
        self.assertTrue(isinstance(order, Order))
        self.assertTrue(isinstance(order2, Order))
        self.assertEqual('3333', str(order))
        self.assertTrue('Without' in str(order2))
        self.assertEqual(50, order.total_sum)












    def create_productcard(self, number='10001'):
        product = self.create_product()
        project = self.create_project()
        provider = self.create_provider()
        country = self.create_country()
        department = self.create_department()
        room = self.create_room()
        trade = self.create_trade()
        lot = self.create_lot()
        phase = self.create_phase()
        annexe5 = self.create_annexe5(project=project)
        return ProductCard.objects.create(number=number, product=product, project=project, provider=provider, origin=country, 
                                            department=department, location=room, trade=trade, lot=lot, phase=phase, 
                                                annexe5=annexe5)
    
    def create_productcard2(self, number=None):
        product2 = self.create_product(name_fr=None)
        project2 = self.create_project(code=None, name_fr=None)
        provider2 = self.create_provider(code=None, name_fr=None)
        country2 = self.create_country(code=None, name_fr=None)
        department2 = self.create_department(name=None)
        room2 = self.create_room(no=None, name_fr=None)
        trade2 = self.create_trade(name_fr=None)
        lot2 = self.create_lot(name_fr=None)
        phase2 = self.create_phase(name=None)
        annexe52 = self.create_annexe5(project=project2)
        return ProductCard.objects.create(number=number, product=product2, project=project2, provider=provider2, origin=country2, 
                                            department=department2, location=room2, trade=trade2, lot=lot2, phase=phase2, 
                                                annexe5=annexe52)

    def create_product(self, desc_fr= 'Some french description', desc_en = 'Some english description',
                        desc_ru = 'Some russian description', desc_tm = 'Some turkmen description', 
                        name_fr = 'Some french name', name_en = 'Some english name', name_ru = 'Some russian name',
                        name_tm = 'Some turkmen name'):
        return Product.objects.create(desc_fr=desc_fr,
                desc_ru=desc_ru, desc_tm=desc_tm, desc_en=desc_en, 
                name_en = name_en, name_ru=name_ru, name_tm=name_tm,
                name_fr=name_fr, 
                )
            
    def create_product2(self, desc_fr= 'Some french description', desc_en = 'Some english description',
                        desc_ru = 'Some russian description', desc_tm = 'Some turkmen description', 
                        name_fr = 'Some french name', name_en = 'Some english name', name_ru = 'Some russian name',
                        name_tm = 'Some turkmen name'):
        return Product.objects.create( desc_fr=desc_fr,
                desc_ru=desc_ru, desc_tm=desc_tm, desc_en=desc_en, 
                name_en = name_en, name_ru=name_ru, name_tm=name_tm,
                name_fr=name_fr)
    
    def create_lot(self, number='02', name_fr='Lot name in french'):
        return Lot.objects.create(number=number, name_fr=name_fr)

    def create_unit(self, name_fr='ens'):
        return Unit.objects.create(name_fr=name_fr)
    
    def create_currency(self, short_name_fr='USD', name_fr='Dollar'):
        return Currency.objects.create(short_name_fr=short_name_fr, name_fr=name_fr)
    
    def create_package_type(self, name_fr='pallete'):
        return PackageType.objects.create(name_fr=name_fr)
    
    def create_project(self, code='CRA', name_fr='Project CRA'):
        return Project.objects.create(code=code, name_fr=name_fr)
    
    def create_provider(self, code='EPOCA', name_fr='Epoca company'):
        return Provider.objects.create(code=code, name_fr=name_fr)
    
    def create_country(self, code='TKM', name_fr='Turkmenistan'):
        return Country.objects.create(code=code, name_fr=name_fr)
    
    def create_room(self, no='A1.01', name_fr='Office'):
        return Room.objects.create(no=no, name_fr=name_fr)

    def create_client(self, name_fr='Mammet'):
        return Client.objects.create(name_fr=name_fr)
    
    def create_employee(self, name_fr='Aman'):
        return Employee.objects.create(name_fr=name_fr)
    
    def create_phase(self, name='GO'):
        return Phase.objects.create(name=name)
    
    def create_trade(self, name_fr='CEA'):
        return Trade.objects.create(name_fr=name_fr)
    
    def create_department(self, name='QS'):
        return Department.objects.create(name=name)
    
    def create_annexe5(self, project=None, code='70.311', name_fr='Meuble', quantity=5, unit_price=10):
        return Annexe5.objects.create(project=project, code=code, name_fr=name_fr, quantity=quantity, unit_price=unit_price)

    def create_order(self, number=None, project=None):
        return Order.objects.create(number=number, project=project)

    def create_orderitem(self, no=1, order=None, product_card=None, quantity =5, price =10):
        return OrderItem.objects.create(no=no, order=order, product_card=product_card, quantity =quantity , price =price )