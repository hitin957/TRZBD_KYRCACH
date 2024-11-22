from django.contrib import admin
from  .models import *
# Register your models here.


@admin.register(Role)
class AdminRole(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Manufacturer)
class AdminManufacturer(admin.ModelAdmin):
    list_display = ('name_manufacturer', 'country',)


@admin.register(PasportData)
class AdminPasportData(admin.ModelAdmin):
    list_display = ('seria_passport', 'number_passport', 'date_give', 'code_podrazdelenia',)


@admin.register(TypeMaterial)
class AdminTypeMaterial(admin.ModelAdmin):
    list_display = ('name_type',)


@admin.register(Warehouse)
class AdminWarehouse(admin.ModelAdmin):
    list_display = ('name_warehouse', 'adress_warehouse',)


@admin.register(Users)
class AdminUsers(admin.ModelAdmin):
    list_display = ('surname', 'name', 'midellname',
                    'date_birth', 'number_phone',
                    'login', 'password',
                    'fk_pasport_data', 'fk_role',)


@admin.register(BuildingMaterials)
class AdminBuildingMaterials(admin.ModelAdmin):
    list_display = ('name', 'description', 'price',
                    'fk_manufacturer', 'fk_type_material',)


@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = ('fk_users',)


@admin.register(Departaments)
class AdminDepartaments(admin.ModelAdmin):
    list_display = ('counts', 'fk_warehouse', 'fk_building_materials')

@admin.register(ItemCart)
class AdminItemCart(admin.ModelAdmin):
    list_display=('count_build_material', 'fk_build_material', 'fk_cart')


@admin.register(Orders)
class AdminOrders(admin.ModelAdmin):
    list_display = ('price', 'payment_method', 'the_method_of_obtaining', 'status_order', 'delivery_address', 'fk_cart', 'fk_users')
