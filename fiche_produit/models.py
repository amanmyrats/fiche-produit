import re
from django.db import models
from django.contrib.auth.models import User
from django.db.models import constraints
from django.db.models.constraints import UniqueConstraint



class Product(models.Model):
    name_en = models.CharField(max_length=200, blank=True, null=True)
    name_fr = models.CharField(max_length=200, blank=True, null=True)
    name_ru = models.CharField(max_length=200, blank=True, null=True)
    name_tm = models.CharField(max_length=200, blank=True, null=True)
    desc_en = models.TextField(max_length=1000, blank=True, null=True)
    desc_fr = models.TextField(max_length=1000, blank=True, null=True)
    desc_ru  = models.TextField(max_length=1000, blank=True, null=True)
    desc_tm  = models.TextField(max_length=1000, blank=True, null=True)
    image = models.ImageField(upload_to='product_image/',blank=True, null=True)
    technical_detail = models.FileField(upload_to='technical_detail/', blank=True, null=True)
    created_by = models.ForeignKey('Employee', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        if self.name_fr:
            return self.name_fr
        else:
            return super().__str__()
    
    
class Lot(models.Model):
    number = models.CharField(max_length=5, blank=True, null=True)
    name_en = models.CharField(max_length=200, blank=True, null=True)
    name_fr = models.CharField(max_length=200, blank=True, null=True)
    name_ru = models.CharField(max_length=200, blank=True, null=True)
    name_tm = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.number) + ' - ' + str(self.name_fr)

class Unit(models.Model):
    name_en = models.CharField(max_length=10, blank=True, null=True)
    name_fr = models.CharField(max_length=10, blank=True, null=True)
    name_ru = models.CharField(max_length=10, blank=True, null=True)
    name_tm = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name_fr

class Currency(models.Model):
    short_name_en = models.CharField(max_length=3, blank=True, null=True)
    short_name_fr = models.CharField(max_length=3, blank=True, null=True)
    short_name_ru = models.CharField(max_length=3, blank=True, null=True)
    short_name_tm = models.CharField(max_length=3, blank=True, null=True)
    name_en = models.CharField(max_length=10, blank=True, null=True)
    name_fr = models.CharField(max_length=10, blank=True, null=True)
    name_ru = models.CharField(max_length=10, blank=True, null=True)
    name_tm = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.short_name_fr

class PackageType(models.Model):
    name_en = models.CharField(max_length=10, blank=True, null=True)
    name_fr = models.CharField(max_length=10, blank=True, null=True)
    name_ru = models.CharField(max_length=10, blank=True, null=True)
    name_tm = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name_fr

class Project(models.Model):
    code = models.CharField(max_length=3, blank=True, null=True)
    name_en = models.CharField(max_length=200, blank=True, null=True)
    name_fr = models.CharField(max_length=200, blank=True, null=True)
    name_ru = models.CharField(max_length=200, blank=True, null=True)
    name_tm = models.CharField(max_length=200, blank=True, null=True)
    director = models.ForeignKey('Employee', on_delete=models.SET_NULL, blank=True, null=True)
    contract_total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.code
    
    @property
    def total_sum(self):
        annexe_list = list(self.annexe5_set.all())
        total_sum=0
        for annexe in annexe_list:
            total_sum += annexe.total_price
            print(total_sum)
        print(total_sum)
        return total_sum

class Provider(models.Model):
    code = models.CharField(max_length=20, blank=True, null=True)
    name_en = models.CharField(max_length=200, blank=True, null=True)
    name_fr = models.CharField(max_length=200, blank=True, null=True)
    name_ru = models.CharField(max_length=200, blank=True, null=True)
    name_tm = models.CharField(max_length=200, blank=True, null=True)
    country = models.ForeignKey('Country',on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name_fr

class Country(models.Model):
    code = models.CharField(max_length=2, blank=True, null=True)
    name_en = models.CharField(max_length=200, blank=True, null=True)
    name_fr = models.CharField(max_length=200, blank=True, null=True)
    name_ru = models.CharField(max_length=200, blank=True, null=True)
    name_tm = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name_fr

class Room(models.Model):
    project = models.ForeignKey(Project,on_delete=models.SET_NULL, blank=True, null=True)
    no = models.CharField(max_length=20, blank=True, null=True)
    level = models.CharField(max_length=10, blank=True, null=True)
    zone = models.CharField(max_length=20, blank=True, null=True)
    name_en = models.CharField(max_length=200, blank=True, null=True)
    name_fr = models.CharField(max_length=200, blank=True, null=True)
    name_ru = models.CharField(max_length=200, blank=True, null=True)
    name_tm = models.CharField(max_length=200, blank=True, null=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    plan = models.ImageField(upload_to = 'room_plan/', blank=True, null = True)

    def __str__(self):
        return self.no + ' - ' + self.name_fr

class Client(models.Model):
    name_en = models.CharField(max_length=200, blank=True, null=True)
    name_fr = models.CharField(max_length=200, blank=True, null=True)
    name_ru = models.CharField(max_length=200, blank=True, null=True)
    name_tm = models.CharField(max_length=200, blank=True, null=True)
    project = models.ForeignKey(Project,on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name_fr

class Employee(models.Model):
    name_en = models.CharField(max_length=200, blank=True, null=True)
    name_fr = models.CharField(max_length=200, blank=True, null=True)
    name_ru = models.CharField(max_length=200, blank=True, null=True)
    name_tm = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name_fr

class Phase(models.Model):
    name = models.CharField(max_length=3, blank=True, null=True)

    def __str__ (self):
        return self.name

class Trade(models.Model):
    name_en = models.CharField(max_length=200, blank=True, null=True)
    name_fr = models.CharField(max_length=200, blank=True, null=True)
    name_ru = models.CharField(max_length=200, blank=True, null=True)
    name_tm = models.CharField(max_length=200, blank=True, null=True)

    def __str__ (self):
        return self.name_fr
    
class Department(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)

    def __str__ (self):
        return self.name


class OrderItem(models.Model):
    no = models.CharField(max_length=20, blank=True, null=True)
    order = models.ForeignKey('Order', related_name = 'orderorderitems', on_delete=models.SET_NULL, blank=True, null=True)
    product_card = models.ForeignKey('ProductCard', related_name='productcardorderitems', on_delete=models.SET_NULL, blank=True, null=True)
    desc_fr = models.TextField(max_length=500, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    unit  = models.ForeignKey(Unit,on_delete=models.SET_NULL, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    currency =  models.ForeignKey(Currency,on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        try:
            return str(str(self.order.number) + ' - ' + str(self.no) + ' - ' + str(self.desc_fr))
        except:
            return 'Empty item (should be deleted)'

    def save(self, *args, **kwargs):
        try:
            self.total_price = self.quantity * self.price
        except:
            self.total_price = 0
        super(OrderItem, self).save(*args, **kwargs)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['order', 'no'], name='order-item-no')]
        ordering = ['no']


class FactureItem(models.Model):
    facture = models.ForeignKey('Facture',related_name='factureitems', on_delete=models.SET_NULL, blank=True, null=True)
    no = models.CharField(max_length=20, blank=True, null=True)
    package_type = models.ForeignKey(PackageType,on_delete=models.SET_NULL, blank=True, null=True)
    hs_code  = models.CharField(max_length = 10, blank=True, null=True)
    order_item = models.ForeignKey(OrderItem, on_delete=models.SET_NULL, blank=True, null=True)
    currency = models.ForeignKey(Currency,on_delete=models.SET_NULL, blank=True, null=True)
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    unit  = models.ForeignKey(Unit,on_delete=models.SET_NULL, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['facture', 'no'], name='facture-item-no')]

    def __str__(self):
        try:
            return str(self.facture.number) + ' - ' + str(self.no) + ' - ' + str(self.order_item.product_card.product.name_fr) + ' - ' + str(self.order_item.desc_fr)
        except:
            return str(self.no)
    
    def save(self, *args, **kwargs):
        try:
            self.total_price = self.quantity * self.price
        except:
            self.total_price = 0
        super(FactureItem, self).save(*args, **kwargs)


class SpecificationItem(models.Model):
    specification =models.ForeignKey('Specification',related_name='specifications', on_delete=models.SET_NULL, blank=True, null=True)
    no = models.CharField(max_length=20, blank=True, null=True)
    facture_item = models.ForeignKey(FactureItem,related_name='specificationfactures', on_delete=models.SET_NULL, unique=True, blank=True, null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['specification', 'no'], name='specification-item-no')]

    def __str__(self):
        if not self.facture_item.order_item.desc_fr:
            return self.facture_item.order_item.desc_fr
        else:
            return self.specification.number


class TdsItem(models.Model):
    tds =models.ForeignKey('Tds', related_name='tdsitems', on_delete=models.SET_NULL, blank=True, null=True)
    no = models.CharField(max_length=20, blank=True, null=True)
    facture_item = models.ForeignKey(FactureItem,related_name='tdsfactures', on_delete=models.SET_NULL, unique=True, blank=True, null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['tds', 'no'], name='tds-item-no')]

    def __str__(self):
        try:
            return self.facture_item.order_item.desc_fr
        except:
            return super().__str__()


class FPType(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class ProductCard(models.Model):
    number = models.CharField(max_length=10, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, blank=True, null=True)
    origin = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, related_name='origin_country')
    manufactured_in = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, related_name='manufactured_country')
    project = models.ForeignKey(Project,on_delete=models.SET_NULL, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=True, null=True)
    location = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True)
    trade = models.ForeignKey(Trade, on_delete=models.SET_NULL, blank=True, null=True)
    lot = models.ForeignKey(Lot, on_delete=models.SET_NULL, blank=True, null=True)
    fp_type =  models.ForeignKey(FPType, on_delete=models.SET_NULL, blank=True, null=True)
    phase = models.ForeignKey(Phase, on_delete=models.SET_NULL, blank=True, null=True)
    index = models.CharField(max_length=2, blank=True, null=True)
    protocol = models.TextField(max_length=500, blank=True, null=True)
    observation =models.TextField(max_length=500, blank=True, null=True)

    annexe5 = models.ForeignKey('Annexe5', on_delete=models.SET_NULL, blank=True, null=True)
    
    sign_contractor1 = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True, related_name='sign_emetteur')
    sign_contractor2 = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True, related_name='sign_director')
    sign_tehnadzor = models.CharField(max_length=200, blank=True, null=True)
    sign_client = models.ForeignKey(Client,on_delete=models.SET_NULL, blank=True, null=True)
    
    date_contractor = models.DateTimeField(auto_now=True, blank=True, null=True)
    date_tehnadzor = models.DateTimeField(auto_now=True, blank=True, null=True)
    date_client = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True, related_name='created')
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    note_for_achat = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        try:
            return str(self.project) + ' - ' + str(self.number) + ' - ' + str(self.product.name_fr)
        except:
            return super().__str__()
    
    @property
    def product_name(self):
        try:
            return self.product.name_fr
        except:
            return ''
    
    @property
    def product_name_fr(self):
        try:
            return self.product.name_fr
        except:
            return ''
    
    @property
    def product_name_ru(self):
        try:
            return self.product.name_ru
        except:
            return ''

    @property
    def product_desc_fr(self):
        try:
            return self.product.desc_fr
        except:
            return ''

    @property
    def product_desc_ru(self):
        try:
            return self.product.desc_ru
        except:
            return ''

    @property
    def image_url(self):
        try:
            return self.product.image.url
        except:
            return 'no image'
    
    @property
    def order_numbers(self):
        order_items = OrderItem.objects.filter(product_card = self.pk)
        orders = []
        for item in order_items:
            orders.append(item.order.number)
        return orders

    @property
    def facture_numbers(self):
        order_items = OrderItem.objects.filter(product_card = self.pk)
        facture_items = FactureItem.objects.filter(order_item__in = order_items)
        factures = []
        for item in facture_items:
            factures.append(item.facture.number)
        return factures

    @property
    def specification_numbers(self):
        order_items = OrderItem.objects.filter(product_card = self.pk)
        facture_items = FactureItem.objects.filter(order_item__in = order_items)
        specification_items = SpecificationItem.objects.filter(facture_item__in = facture_items)
        specifications = []
        for item in specification_items:
            specifications.append(item.specification.number)
        return specifications
    
    @property
    def tds_numbers(self):
        order_items = OrderItem.objects.filter(product_card = self.pk)
        facture_items = FactureItem.objects.filter(order_item__in = order_items)
        # specification_items = SpecificationItem.objects.filter(facture_item__in = facture_items)
        tds_items = TdsItem.objects.filter(facture_item__in = facture_items)
        tdss = []
        for item in tds_items:
            tdss.append(item.tds.number)
        return tdss
    
    @property
    def declaration_numbers(self):
        order_items = OrderItem.objects.filter(product_card = self.pk)
        facture_items = FactureItem.objects.filter(order_item__in = order_items)
        # specification_items = SpecificationItem.objects.filter(facture_item__in = facture_items)
        # tds_items = TdsItem.objects.filter(facture_item__in = specification_items)
        declaration_items = DeclarationItem.objects.filter(facture_item__in  = facture_items)
        declarations = []
        for item in declaration_items:
            declarations.append(item.declaration.number)
        return declarations
    
    @property
    def coo_numbers(self):
        order_items = OrderItem.objects.filter(product_card = self.pk)
        facture_items = FactureItem.objects.filter(order_item__in = order_items)
        coo_factures = CooFacture.objects.filter(facture_item__in = facture_items)
        coos = []
        for item in coo_factures:
            coos.append(item.coo.number)
        return coos
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=['project','number'], name = 'project-fp-number')]


class Annexe5(models.Model):
    project = models.ForeignKey(Project,on_delete=models.SET_NULL, blank=True, null=True)
    lot = models.ForeignKey(Lot,on_delete=models.SET_NULL, blank=True, null=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    name_en = models.CharField(max_length=200, blank=True, null=True)
    name_fr = models.CharField(max_length=200, blank=True, null=True)
    name_ru = models.CharField(max_length=200, blank=True, null=True)
    name_tm = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    unit  = models.ForeignKey(Unit,on_delete=models.SET_NULL, blank=True, null=True)
    material_unit_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    material_total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    fabrication_unit_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    fabrication_total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    transport_unit_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    transport_total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    currency =  models.ForeignKey(Currency,on_delete=models.SET_NULL, blank=True, null=True)
    country = models.ForeignKey('Country',on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.code) + ' - ' + str(self.name_fr)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['project','code'], name = 'project-annexe-code')]

class Order(models.Model):
    number = models.CharField(max_length=20,unique=True, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True)
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        try:
            return str(self.number)
        except:
            return 'Without order number.'
    @property
    def total_sum(self):
        orderitems = self.orderorderitems.all()
        total_sum = 0
        for item in orderitems:
            try:
                total_sum += item.total_price
            except:
                pass
        
        return total_sum

    @property
    def facture_numbers(self):
        facture_items = FactureItem.objects.filter(order_item = self.pk)
        factures = []
        for item in facture_items:
            factures.append(item.facture.number)
        return factures

    @property
    def specification_numbers(self):
        facture_items = FactureItem.objects.filter(order_item = self.pk)
        specification_items = SpecificationItem.objects.filter(facture_item__in = facture_items)
        specifications = []
        for item in specification_items:
            specifications.append(item.specification.number)
        return specifications
    
    @property
    def tds_numbers(self):
        facture_items = FactureItem.objects.filter(order_item = self.pk)
        # specification_items = SpecificationItem.objects.filter(facture_item__in = facture_items)
        tds_items = TdsItem.objects.filter(facture_item__in = facture_items)
        tdss = []
        for item in tds_items:
            tdss.append(item.tds.number)
        return tdss
    
    @property
    def declaration_numbers(self):
        facture_items = FactureItem.objects.filter(order_item = self.pk)
        # specification_items = SpecificationItem.objects.filter(facture_item__in = facture_items)
        # tds_items = TdsItem.objects.filter(facture_item__in = specification_items)
        declaration_items = DeclarationItem.objects.filter(facture_item__in  = facture_items)
        declarations = []
        for item in declaration_items:
            declarations.append(item.declaration.number)
        return declarations
    
    @property
    def coo_numbers(self):
        facture_items = FactureItem.objects.filter(order_item = self.pk)
        coo_factures = CooFacture.objects.filter(facture_item__in = facture_items)
        coos = []
        for item in coo_factures:
            coos.append(item.coo.number)
        return coos


class Routage(models.Model):
    number = models.CharField(max_length = 20,unique=True, blank=True, null=True)
    date = models.DateTimeField( blank=True, null=True)

    def __str__(self):
        try:
            return str(self.number)
        except:
            return 'Without Routage Number'


class RoutageItem(models.Model):
    routage = models.ForeignKey(Routage, related_name='routagetoroutageitem', on_delete=models.SET_NULL, blank=True, null=True)
    facture = models.ForeignKey('Facture', related_name='facturetoroutageitem', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['routage', 'facture'], name='routage-facture-number')]

    def __str__(self):
        try:
            return str(self.routage) + ' - ' + str(self.facture)
        except:
            try:
                return str(self.facture)
            except:
                return 'There is no assigned facture.'

class Facture(models.Model):
    number = models.CharField(max_length=20,unique=True, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField( blank=True, null=True)

    @property
    def total_sum(self):
        factureitems = self.factureitems.all()
        total = 0
        for item in factureitems:
            try:
                total += item.total_price
            except:
                pass
        return total

    def __str__(self):
        try:
            return str(self.number)
        except:
            return 'Without facture number.'

    @property
    def facture_numbers(self):
        facture_items = FactureItem.objects.filter(order_item = self.pk)
        factures = []
        for item in facture_items:
            factures.append(item.facture.number)
        return factures


class Specification(models.Model):
    number = models.CharField(max_length=20,unique=True, blank=True, null=True)
    date = models.DateTimeField( blank=True, null=True)
    
    def __str__(self):
        try:
            return str(self.number)
        except:
            return 'Without specification number.'

class Tds(models.Model):
    number = models.CharField(max_length=20,unique=True, blank=True, null=True)
    date = models.DateTimeField( blank=True, null=True)

    def __str__(self):
        try:
            return str(self.number)
        except:
            return 'Without TDS number.'

class Declaration(models.Model):
    number = models.CharField(max_length=20,unique=True, blank=True, null=True)
    date = models.DateTimeField( blank=True, null=True)

    def __str__(self):
        try:
            return str(self.number)
        except:
            return 'Without declaration number.'

class DeclarationItem(models.Model):
    declaration =models.ForeignKey(Declaration,related_name='declarationitems', on_delete=models.SET_NULL, blank=True, null=True)
    no = models.CharField(max_length=20,unique=True, blank=True, null=True)
    facture_item = models.ForeignKey(FactureItem, related_name='declarationfactures', on_delete=models.SET_NULL, unique=True, blank=True, null=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['declaration', 'no'], name='declaration-item-no')]

    def __str__(self):
        try:
            return self.facture_item.order_item.desc_fr
        except:
            return 'Declaration item is empty.'

class Coo(models.Model):
    number = models.CharField(max_length=20,unique=True, blank=True, null=True)
    date = models.DateTimeField( blank=True, null=True)

    def __str__(self):
        try:
            return str(self.number)
        except:
            return 'Without COO number.'

class CooFacture(models.Model):
    coo =models.ForeignKey(Coo,related_name='cootofacture', on_delete=models.SET_NULL, blank=True, null=True)
    facture_item = models.ForeignKey(FactureItem,related_name='facturetocoo', on_delete=models.SET_NULL, unique=True, blank=True, null=True)

    def __str__(self):
        try:
            return str(self.coo) + ' - ' + str(self.facture_item.facture)
        except:
            try:
                return str(self.facture_item.facture)
            except:
                return 'There is no assigned facture.'
