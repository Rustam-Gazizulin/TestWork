from django.db import models


class Location(models.Model):
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    build = models.CharField(max_length=10)


class Info(models.Model):
    email = models.EmailField()
    address = models.ForeignKey(Location, on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    model = models.CharField(max_length=30, verbose_name='Модель')
    release_date = models.DateField(auto_now_add=True, verbose_name='Дата релиза')


class StatusHierarchy(models.IntegerChoices):
    factory = 0, 'Завод'
    distributor = 1, 'Дистрибьютор'
    dealer_center = 2, 'Дилерский центр'
    retail_network = 3, 'Розничная сеть'
    entrepreneur = 4, 'Индивидуальный предприниматель'


class Factory(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    contacts = models.ForeignKey(Info, on_delete=models.CASCADE, verbose_name='Контактная информация')
    produce = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукция')
    staff = models.PositiveBigIntegerField(verbose_name='Сотрудники')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.PositiveSmallIntegerField(
        verbose_name='Статус в иерархии поставок',
        choices=StatusHierarchy.choices,
        default=StatusHierarchy.factory
    )


class Distributor(models.Model):
    name = models.CharField(max_length=20)
    contacts = models.ForeignKey(Info, on_delete=models.CASCADE, verbose_name='Контактная информация')
    produce = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукция')
    supplier = models.ForeignKey(Factory, on_delete=models.CASCADE, verbose_name='Поставщик')
    staff = models.PositiveBigIntegerField(verbose_name='Сотрудники')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.PositiveSmallIntegerField(
        verbose_name='Статус в иерархии поставок',
        choices=StatusHierarchy.choices,
        default=StatusHierarchy.distributor
    )


class DealerCenter(models.Model):
    name = models.CharField(max_length=20)
    contacts = models.ForeignKey(Info, on_delete=models.CASCADE, verbose_name='Контактная информация')
    produce = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукция')
    supplier = models.ForeignKey(Distributor, on_delete=models.CASCADE, verbose_name='Поставщик')
    staff = models.PositiveBigIntegerField(verbose_name='Сотрудники')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.PositiveSmallIntegerField(
        verbose_name='Статус в иерархии поставок',
        choices=StatusHierarchy.choices,
        default=StatusHierarchy.dealer_center
    )


class RetailNetwork(models.Model):
    name = models.CharField(max_length=20)
    contacts = models.ForeignKey(Info, on_delete=models.CASCADE, verbose_name='Контактная информация')
    produce = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукция')
    supplier = models.ForeignKey(DealerCenter, on_delete=models.CASCADE, verbose_name='Поставщик')
    staff = models.PositiveBigIntegerField(verbose_name='Сотрудники')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.PositiveSmallIntegerField(
        verbose_name='Статус в иерархии поставок',
        choices=StatusHierarchy.choices,
        default=StatusHierarchy.retail_network
    )


class Entrepreneur(models.Model):
    name = models.CharField(max_length=20)
    contacts = models.ForeignKey(Info, on_delete=models.CASCADE, verbose_name='Контактная информация')
    produce = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукция')
    supplier = models.ForeignKey(RetailNetwork, on_delete=models.CASCADE, verbose_name='Поставщик')
    staff = models.PositiveBigIntegerField(verbose_name='Сотрудники')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    status = models.PositiveSmallIntegerField(
        verbose_name='Статус в иерархии поставок',
        choices=StatusHierarchy.choices,
        default=StatusHierarchy.entrepreneur
    )
