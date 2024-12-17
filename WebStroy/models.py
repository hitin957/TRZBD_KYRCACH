# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BuildingMaterials(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название')
    description = models.CharField(max_length=225, verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')
    fk_manufacturer = models.ForeignKey('Manufacturer', models.DO_NOTHING, db_column='fk_manufacturer', verbose_name='Производитель')
    fk_type_material = models.ForeignKey('TypeMaterial', models.DO_NOTHING, db_column='fk_type_material', verbose_name='Тип строительного материала')

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'building_materials'


class Cart(models.Model):
    fk_users = models.ForeignKey('Users', models.DO_NOTHING, db_column='fk_users', verbose_name='Пользователь')

    class Meta:
        managed = False
        db_table = 'cart'


class Departaments(models.Model):
    counts = models.IntegerField(verbose_name='Колличество')
    fk_warehouse = models.ForeignKey('Warehouse', models.DO_NOTHING, db_column='fk_warehouse',verbose_name='Склад')
    fk_building_materials = models.ForeignKey(BuildingMaterials, models.DO_NOTHING, db_column='fk_building_materials', verbose_name='Строительный материал')

    class Meta:
        managed = False
        db_table = 'departaments'


class ItemCart(models.Model):
    count_build_material = models.IntegerField(blank=True, null=True, verbose_name='Колличество материала')
    fk_build_material = models.ForeignKey(BuildingMaterials, models.DO_NOTHING, db_column='fk_build_material', verbose_name='Строительный материал')
    fk_cart = models.ForeignKey(Cart, models.DO_NOTHING, db_column='fk_cart', verbose_name='Корзина')

    class Meta:
        managed = False
        db_table = 'item_cart'


class Manufacturer(models.Model):
    name_manufacturer = models.CharField(max_length=20, verbose_name='Название производителя')
    country = models.CharField(max_length=25, verbose_name='Страна')

    def __str__(self):
        return self.name_manufacturer

    class Meta:
        managed = False
        db_table = 'manufacturer'


class Orders(models.Model):
    price = models.IntegerField(verbose_name='Цена')
    
    BANCCARD = 'Банковская карта'
    MONEY = 'Наличными'
    PAYMENT_METHOD = [
        (BANCCARD,'Банковская карта'),
        (MONEY, 'Наличными')
    ]
    payment_method = models.CharField(max_length=30, blank=True, null=True, choices=PAYMENT_METHOD, verbose_name='Способ оплаты')

    CKLAD='Забрать со склада'
    COURIER='Заказать доставку'
    TYPE_DELIVERY = [
        (CKLAD, 'Забрать со склада'),
        (COURIER, 'Заказать доставку')
    ]
    the_method_of_obtaining = models.CharField(max_length=30, blank=True, null=True, choices=TYPE_DELIVERY, verbose_name='Способ получения')
    status_order = models.CharField(max_length=30, blank=True, null=True, verbose_name='Статус заказа')
    delivery_address = models.CharField(max_length=80, blank=True, null=True, verbose_name='Адрес доставки')
    fk_cart = models.ForeignKey(Cart, models.DO_NOTHING, db_column='fk_cart', verbose_name='Корзина')
    fk_users = models.ForeignKey('Users', models.DO_NOTHING, db_column='fk_users', verbose_name='Пользователь')

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        managed = False
        db_table = 'orders'


class PasportData(models.Model):
    seria_passport = models.IntegerField(verbose_name='Серия паспорта')
    number_passport = models.IntegerField(verbose_name='Номер паспорта')
    date_give = models.DateField(verbose_name='Дата выдачи')
    code_podrazdelenia = models.IntegerField(verbose_name='Код подраздиления')

    def __str__(self):
        return f'Серия: {self.seria_passport}, Номер: {self.number_passport}'

    class Meta:
        managed = False
        db_table = 'pasport_data'


class Role(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название роли')

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'role'


class TypeMaterial(models.Model):
    name_type = models.CharField(max_length=20, verbose_name='Название типа')

    def __str__(self):
        return self.name_type

    class Meta:
        managed = False
        db_table = 'type_material'


class Users(models.Model):
    surname = models.TextField(verbose_name='Фамилия')
    name = models.TextField(verbose_name='Имя')
    midellname = models.TextField(verbose_name='Отчество')
    date_birth = models.DateField(verbose_name='Дата рождения')
    number_phone = models.TextField(verbose_name='Номер телефона')
    login = models.TextField(verbose_name='Логин')
    password = models.TextField(verbose_name='Пароль')
    fk_pasport_data = models.ForeignKey(PasportData, models.DO_NOTHING, db_column='fk_pasport_data', blank=True, null=True, verbose_name='Паспортные данные')
    fk_role = models.ForeignKey(Role, models.DO_NOTHING, db_column='fk_role', verbose_name='Роль')

    def __str__(self):
        return f'{self.surname} {self.name} {self.midellname}'

    class Meta:
        managed = False
        db_table = 'users'


class Warehouse(models.Model):
    name_warehouse = models.CharField(max_length=30, verbose_name='Название склада')
    adress_warehouse = models.CharField(max_length=50, verbose_name='Адресс склада')

    def __str__(self):
        return self.name_warehouse

    class Meta:
        managed = False
        db_table = 'warehouse'
