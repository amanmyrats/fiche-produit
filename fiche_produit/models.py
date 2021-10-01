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
    technical_detail = models.FileField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    created_by = models.ForeignKey('Employee', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name_fr
    
class Lot(models.Model):
    no = models.CharField(max_length=5, blank=True, null=True)
    name_en = models.CharField(max_length=200, blank=True, null=True)
    name_fr = models.CharField(max_length=200, blank=True, null=True)
    name_ru = models.CharField(max_length=200, blank=True, null=True)
    name_tm = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name_fr

class Project(models.Model):
    code = models.CharField(max_length=3, blank=True, null=True)
    name_en = models.CharField(max_length=200, blank=True, null=True)
    name_fr = models.CharField(max_length=200, blank=True, null=True)
    name_ru = models.CharField(max_length=200, blank=True, null=True)
    name_tm = models.CharField(max_length=200, blank=True, null=True)
    director = models.ForeignKey('Employee', on_delete=models.SET_NULL, blank=True, null=True)
    # client = models.ForeignKey('Client',on_delete=models.SET_NULL, blank=True, null=True)
    contract_total = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.code

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

    def __str__(self):
        return self.name_fr + ' - ' + self.name_fr

class Client(models.Model):
    name_en = models.CharField(max_length=200, blank=True, null=True)
    name_fr = models.CharField(max_length=200, blank=True, null=True)
    name_ru = models.CharField(max_length=200, blank=True, null=True)
    name_tm = models.CharField(max_length=200, blank=True, null=True)
    project = models.ForeignKey(Project,on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name_fr

class Employee(models.Model):
    # project = models.ForeignKey(Project,on_delete=models.SET_NULL, blank=True, null=True)
    name_en = models.CharField(max_length=200, blank=True, null=True)
    name_fr = models.CharField(max_length=200, blank=True, null=True)
    name_ru = models.CharField(max_length=200, blank=True, null=True)
    name_tm = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name_fr

class ProductCard(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    lot = models.ForeignKey(Lot, on_delete=models.SET_NULL, blank=True, null=True)
    project = models.ForeignKey(Project,on_delete=models.SET_NULL, blank=True, null=True)
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, blank=True, null=True)
    origin = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, related_name='origin_country')
    manufactured_in = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, related_name='manufactured_country')
    location = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True)
    protocol = models.CharField(max_length=300, blank=True, null=True)
    observation =models.CharField(max_length=300, blank=True, null=True)
    sign_contractor1 = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True, related_name='sign_emetteur')
    sign_contractor2 = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True, related_name='sign_director')
    sign_tehnadzor = models.CharField(max_length=200, blank=True, null=True)
    sign_client = models.ForeignKey(Client,on_delete=models.SET_NULL, blank=True, null=True)
    date_contractor = models.DateTimeField(auto_now=True, blank=True, null=True)
    date_tehnadzor = models.DateTimeField(auto_now=True, blank=True, null=True)
    date_client = models.DateTimeField(auto_now=True, blank=True, null=True)
    phase = models.CharField(max_length=10,choices=[('1','APD'), ('2','PEO'), ('3', 'DOE'),], blank=True, null=True)
    fp_type = models.CharField(max_length=10,choices=[(1,'FP')], blank=True, null=True)
    no = models.CharField(max_length=10, blank=True, null=True)
    index = models.CharField(max_length=2, blank=True, null=True)
    trade = models.CharField(max_length=10,choices=[('1','CEA'), ('2','MEC'), ('3', 'ELE'),], blank=True, null=True)
    department = models.CharField(max_length=10,choices=[('1','CEA'), ('2','MEC'), ('3', 'ELE'),], blank=True, null=True)
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True, related_name='created')
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    note_for_achat = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.project) + ' - ' + str(self.no)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['project','no'], name = 'project-fp-no')]

class Annexe5(models.Model):
    units = [(1,'un'),(2,'mt'), (3,'pc'),(4, 'm2'),(5,'m3'), (6,'set'), (7,'ls'),]
    currencies = [(1,'Manat'),(2,'Euro'),(3, 'USD'),]

    project = models.ForeignKey(Project,on_delete=models.SET_NULL, blank=True, null=True)
    lot = models.ForeignKey(Lot,on_delete=models.SET_NULL, blank=True, null=True)
    no = models.CharField(max_length=10, blank=True, null=True)
    name_en = models.CharField(max_length=200, blank=True, null=True)
    name_fr = models.CharField(max_length=200, blank=True, null=True)
    name_ru = models.CharField(max_length=200, blank=True, null=True)
    name_tm = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    unit  = models.CharField(max_length=10,choices=units, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10,choices=currencies, blank=True, null=True)
    country = models.ForeignKey('Country',on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return str(self.no) + str(self.name_fr)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['project','no'], name = 'project-annexe-no')]

class Order(models.Model):
    no = models.CharField(max_length=20,unique=True, blank=True, null=True)
    project = models.ForeignKey(Project,on_delete=models.SET_NULL, blank=True, null=True)
    created_by = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.no)

class OrderItem(models.Model):
    units = [(1,'un'),(2,'mt'), (3,'pc'),(4, 'm2'),(5,'m3'), (6,'set'), (7,'ls'),]
    currencies = [(1,'Manat'),(2,'Euro'),(3, 'USD'),]

    no = models.CharField(max_length=20,unique=True, blank=True, null=True)
    product_card = models.ForeignKey(ProductCard, on_delete=models.SET_NULL, blank=True, null=True)
    desc_fr = models.TextField(max_length=500, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    unit  = models.CharField(max_length=10,choices=units, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10,choices=currencies, blank=True, null=True)
    annexe5 = models.ForeignKey(Annexe5, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.desc_fr

class Routage(models.Model):
    no = models.CharField(max_length = 20,unique=True, blank=True, null=True)
    date = models.DateTimeField( blank=True, null=True)

    def __str__(self):
        return self.no

class Facture(models.Model):
    currencies = [(1,'Manat'),(2,'Euro'),(3, 'USD')]


    no = models.CharField(max_length=20,unique=True, blank=True, null=True)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField( blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    routage = models.ForeignKey(Routage, on_delete=models.SET_NULL, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10,choices=currencies, blank=True, null=True)

    def __str__(self):
        return self.no

class FactureItem(models.Model):
    currencies = [(1,'Manat'),(2,'Euro'),(3, 'USD'),]
    units = [(1,'un'),(2,'mt'), (3,'pc'),(4, 'm2'),(5,'m3'), (6,'set'), (7,'ls'),]
    package_types = [(1,'Palette'),(2, 'Package'), (3, 'Some other type'),]

    package_type = models.CharField(max_length=20,choices=package_types, blank=True, null=True)
    hs_code  = models.CharField(max_length = 10,unique=True, blank=True, null=True)
    item = models.ForeignKey(OrderItem, on_delete=models.SET_NULL, blank=True, null=True)
    currency = models.CharField(max_length=10,choices=currencies, blank=True, null=True)
    provider = models.ForeignKey(Provider, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    unit  = models.CharField(max_length=10,choices=units, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.item.desc_fr

class Specification(models.Model):
    no = models.CharField(max_length=20,unique=True, blank=True, null=True)
    date = models.DateTimeField( blank=True, null=True)
    
    def __str__(self):
        return self.no

class SpecificationItem(models.Model):
    specification =models.ForeignKey(Specification, on_delete=models.SET_NULL, blank=True, null=True)
    no = models.CharField(max_length=20,unique=True, blank=True, null=True)
    facture_item = models.ForeignKey(FactureItem, on_delete=models.SET_NULL, unique=True, blank=True, null=True)

    def __str__(self):
        return self.facture_item.item.desc_fr

class Tds(models.Model):
    no = models.CharField(max_length=20,unique=True, blank=True, null=True)
    date = models.DateTimeField( blank=True, null=True)

    def __str__(self):
        return self.no

class TdsItem(models.Model):
    tds =models.ForeignKey(Tds, on_delete=models.SET_NULL, blank=True, null=True)
    no = models.CharField(max_length=20,unique=True, blank=True, null=True)
    facture_item = models.ForeignKey(FactureItem, on_delete=models.SET_NULL, unique=True, blank=True, null=True)

    def __str__(self):
        return self.facture_item.item.desc_fr

class Declaration(models.Model):
    no = models.CharField(max_length=20,unique=True, blank=True, null=True)
    date = models.DateTimeField( blank=True, null=True)

    def __str__(self):
        return self.no

class DeclarationItem(models.Model):
    declaration =models.ForeignKey(Declaration, on_delete=models.SET_NULL, blank=True, null=True)
    no = models.CharField(max_length=20,unique=True, blank=True, null=True)
    facture_item = models.ForeignKey(FactureItem, on_delete=models.SET_NULL, unique=True, blank=True, null=True)

    def __str__(self):
        return self.facture_item.item.desc_fr

class Coo(models.Model):
    no = models.CharField(max_length=20,unique=True, blank=True, null=True)
    date = models.DateTimeField( blank=True, null=True)

    def __str__(self):
        return self.no

class CooFacture(models.Model):
    coo =models.ForeignKey(Coo, on_delete=models.SET_NULL, blank=True, null=True)
    facture_item = models.ForeignKey(FactureItem, on_delete=models.SET_NULL, unique=True, blank=True, null=True)

    def __str__(self):
        return self.facture_item.item.desc_fr
