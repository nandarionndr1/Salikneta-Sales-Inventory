from django.db import models


# Create your models here.

class Branch(models.Model):
    idBranch = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)


class Manager(models.Model):
    idManager = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    idBranch = models.ForeignKey(Branch, on_delete=models.CASCADE)


class Cashier(models.Model):
    idCashier = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    idBranch = models.ForeignKey(Branch, on_delete=models.CASCADE)


class Supplier(models.Model):
    idSupplier = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    contactNumber = models.CharField(max_length=45)
    emailAddress = models.CharField(max_length=45)
    website = models.CharField(max_length=45)
    address1 = models.CharField(max_length=45)
    address2 = models.CharField(max_length=45)
    city = models.CharField(max_length=45)
    province = models.CharField(max_length=45)
    country = models.CharField(max_length=45)
    postal = models.CharField(max_length=45)


class Category(models.Model):
    idCategory = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)


class Product(models.Model):
    idProduct = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    description = models.CharField(max_length=45)
    suggestedUnitPrice = models.FloatField()
    unitsInStock = models.IntegerField()
    reorderLevel = models.IntegerField()
    unitOfMeasure = models.CharField(max_length=45)
    SKU = models.IntegerField()
    barcode = models.CharField(max_length=45)
    img_path = models.ImageField(upload_to="prod_img/")
    idCategory = models.ForeignKey(Category, on_delete=models.CASCADE,db_column='idCategory_id')

    class Meta:
        managed = False
        db_table = 'salikneta_product'
    @property
    def get_product_code(self):
        return self.idProduct + 1000

    @property
    def get_num_incoming(self):
        incoming = 0;
        objs = OrderLines.objects.filter(idProduct_id=self.idProduct)
        for o in objs:
           incoming += o.qty - o.get_delivered_products_num
        return incoming
    @staticmethod
    def get_num_lowstock_items():
        ct = 0
        for p in Product.objects.all():
            if p.unitsInStock < p.reorderLevel:
                ct+=1
        return ct
class PurchaseOrder(models.Model):
    idPurchaseOrder = models.AutoField(primary_key=True)
    idCashier = models.ForeignKey(Cashier, on_delete=models.CASCADE)
    idSupplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    orderDate = models.DateField()
    expectedDate = models.DateField()
    status = models.CharField(max_length=45)
    @property
    def get_delivery(self):
        return Delivery.objects.get(idPurchaseOrder=self.idPurchaseOrder)
    @property
    def get_orderLines(self):
        return OrderLines.objects.filter(idPurchaseOrder_id=self.pk).select_related('idProduct')


class OrderLines(models.Model):
    idOrderLines = models.AutoField(primary_key=True)
    idPurchaseOrder = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    idProduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.FloatField()

    @property
    def get_delivered_products_num(self):
        qty = 0
        for d in DeliveredProducts.objects.filter(idOrderLines=self.idOrderLines):
            qty += d.qty
        return qty

class Delivery(models.Model):
    idDelivery = models.AutoField(primary_key=True)
    deliveryDate = models.DateField()
    idPurchaseOrder = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)


class DeliveredProducts(models.Model):
    idDeliveredProducts = models.AutoField(primary_key=True)
    idOrderLines = models.ForeignKey(OrderLines, on_delete=models.CASCADE)
    idDelivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    qty = models.FloatField()


class SalesInvoice(models.Model):
    idSales = models.AutoField(primary_key=True)
    idCashier = models.ForeignKey(Cashier, on_delete=models.CASCADE)
    invoiceDate = models.DateTimeField(db_column='invoiceDate')
    customer = models.CharField(max_length=45)

    @staticmethod
    def get_latest_invoice_num():
        try:
            si = SalesInvoice.objects.all().order_by("-idSales")[0]
            return si.idSales + 100000
        except:
            return 100000

    @staticmethod
    def get_latest_invoice_id():
        try:
            si = SalesInvoice.objects.all().order_by("-idSales")[0]
            return si.idSales + 1
        except:
            return 1
    @property
    def get_invoice_id(self):
        return 100000 + self.idSales
    @property
    def get_invoicelines(self):
        return InvoiceLines.objects.filter(idSales=self.idSales)
    @property
    def get_invoice_qty(self):
        invoices = InvoiceLines.objects.filter(idSales=self.idSales)
        qty = 0
        for i in invoices:
            qty += i.qty
        return qty
    @property
    def get_gross_invoice_amount(self):
        invoices = InvoiceLines.objects.filter(idSales=self.idSales)
        amt = 0
        for i in invoices:
            amt += i.qty * i.unitPrice
        return amt
    @property
    def get_net_invoice_amount(self):
        invoices = InvoiceLines.objects.filter(idSales=self.idSales)
        amt = 0
        for i in invoices:
            amt += i.get_net_price
        return amt

class InvoiceLines(models.Model):
    idInvoiceLines = models.AutoField(db_column='idInvoiceLines', primary_key=True)  # Field name made lowercase.
    idProduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    unitPrice = models.FloatField()
    qty = models.FloatField()
    idSales = models.ForeignKey(SalesInvoice, models.DO_NOTHING, db_column='idSales')  # Field name made lowercase.
    disc = models.FloatField(blank=True, null=True)

    @property
    def get_net_price(self):
        g_amt = (self.qty * self.unitPrice)
        return g_amt - (g_amt * (self.disc / 100))


class BackLoad(models.Model):
    idBackload = models.AutoField(primary_key=True)
    idCashier = models.ForeignKey(Cashier, on_delete=models.CASCADE)
    backloadDate = models.DateField()
    @property
    def get_backload_lines(self):
        return BackloadLines.objects.filter(idBackload=self.pk)



class BackloadLines(models.Model):
    idBackloadLines = models.AutoField(primary_key=True)
    idProduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    idBackload = models.ForeignKey(BackLoad, models.DO_NOTHING, db_column='idBackload')
    qty = models.FloatField()
    reason = models.CharField(max_length=45)
   
class TransferOrder(models.Model):
    idTransferOrder = models.AutoField(primary_key=True)
    idCashier = models.ForeignKey(Cashier, on_delete=models.CASCADE)
    transferDate = models.DateField()
    expectedDate = models.DateField()


class TransferLines(models.Model):
    idTransferOrder = models.AutoField(primary_key=True)
    idProduct = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.FloatField()


