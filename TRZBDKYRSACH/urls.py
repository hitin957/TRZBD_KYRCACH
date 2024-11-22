"""
URL configuration for TRZBDKYRSACH project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from WebStroy import views as v
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.Main, name='Main'),
    path('regis', v.regis, name='regis'),
    path('auth', v.auth, name='auth'),
    path('orders', v.Ord, name='order'),
    path('cart', v.cart, name='cart'),
    path('delcart/<int:id>/', v.deletecart),
    path('Add_cart/<int:pk>/', v.Add_cart, name='Add_cart'),
    path('UpCount/<int:id>/<str:min_or_plus>', v.upOrdownCountCart),
    path('delorder/<int:id>/', v.deletOrder),
    path('updatecart/<int:id>/', v.Update_cart),
    path('Add_order', v.add_Order, name='Add_order'),
    path('Update_order/<int:id>/', v.update_Order),
    path('choose_method_oplati/', v.choose_pay, name='Pay'),
    path('choose_method_dilivery/', v.choose_dilivery, name='dilivery'),
    path('MainAdmin/', v.MainAdmin, name='MainAdmin'),
    path('MainAdmin/ViewsUsers/', v.ViewUsers, name='ViewUsers'),
    path('MainAdmin/ViewData/', v.ViewDataAdmin, name='ViewData'),
    path('MainAdmin/ViewsUsers/AddNewUsers/', v.AddUser, name='AddUser'),
    path('MainAdmin/ViewsUsers/DeleteUser/<int:id>/', v.deleteUser),
    path('MainAdmin/ViewData/AddNewRole/', v.Add_new_role, name='AddRole'),
    path('MainAdmin/ViewData/UpRole/<int:id>/', v.Update_role),
    path('MainAdmin/ViewData/DelRole/<int:id>/', v.Delete_role),

    #Начальник склада
    path('MainWarehouse/', v.MainWarehouse, name='MainWarehouse'),
    path('MainWarehouse/ViewDataWarehouse/', v.ViewDataWarehouse, name='ViewDataWarehouse'),
    
    #Управление Типами материала
    path('MainWarehouse/ViewDataWarehouse/AddNewTypeMaterials/', v.AddNewTypeMaterial, name='AddNewTypeMaterial'),
    path('MainWarehouse/ViewDataWarehouse/UpdateTypeMaterial/<int:id>/', v.Update_TypeMaterial),
    path('MainWarehouse/ViewDataWarehouse/DeleteTypeMaterials/<int:id>/', v.Delete_TypeMaterial),
    path('MainWarehouse/ViewDataWarehouse/ExportTypeMaterials/CSV', v.export_TypeMaterial_to_csv, name='export_TypeMaterial_to_csv'),
    path('MainWarehouse/ViewDataWarehouse/ExportTypeMaterials/SQL', v.export_TypeMaterial_to_sql, name='export_TypeMaterial_to_sql'),
    path('MainWarehouse/ViewDataWarehouse/ImportTypeMaterials/CSV', v.import_csvTypeMaterial, name='import_csvTypeMaterial'),
    
    #Управление производителя
    path('MainWarehouse/ViewDataWarehouse/AddNewManufactires/', v.AddNewManufactire, name='AddNewManufactire'),
    path('MainWarehouse/ViewDataWarehouse/UpdateManifacture/<int:id>/', v.Update_Manufactire),
    path('MainWarehouse/ViewDataWarehouse/DeleteManufactires/<int:id>/', v.Delete_Manufactire),
    path('MainWarehouse/ViewDataWarehouse/ExportManufactires/CSV', v.export_Manufactire_to_csv, name='export_Manufactire_to_csv'),
    path('MainWarehouse/ViewDataWarehouse/ExportManufactires/SQL', v.export_Manufactire_to_sql, name='export_Manufactire_to_sql'),
    path('MainWarehouse/ViewDataWarehouse/ImportManufactires/CSV', v.import_csvManufactire, name='import_csvManufactire'),

    #Управление складами
    path('MainWarehouse/ViewDataWarehouse/AddNewWarehouse/', v.AddNewWarehouse, name='AddNewWarehouse'),
    path('MainWarehouse/ViewDataWarehouse/UpdateWarehouse/<int:id>/', v.Update_Warehouse),
    path('MainWarehouse/ViewDataWarehouse/DeleteWarehouse/<int:id>/', v.Delete_Warehouse),
    path('MainWarehouse/ViewDataWarehouse/ExportWarehouse/CSV', v.export_Warehouse_to_csv, name='export_Warehouse_to_csv'),
    path('MainWarehouse/ViewDataWarehouse/ExportWarehouse/SQL', v.export_Warehouse_to_sql, name='export_Warehouse_to_sql'),
    path('MainWarehouse/ViewDataWarehouse/ImportWarehouse/CSV', v.import_csvWarehouse, name='import_csvWarehouse'),

    #Управление строительными материалами
    path('MainWarehouse/ViewDataWarehouse/AddBuildMaterial/', v.add_Buildmaterials, name='AddNewBuildMaterial'),
    path('MainWarehouse/ViewDataWarehouse/UpdateBuildMaterials/<int:id>/', v.update_Buildmaterials),
    path('MainWarehouse/ViewDataWarehouse/DeleteBuildMaterials/<int:id>/', v.delete_Buildmaterials),

    #Управление отделами
    path('MainWarehouse/ViewDataWarehouse/AddDepartments/', v.add_Departments, name='AddNewDepartment'),
    path('MainWarehouse/ViewDataWarehouse/UpdateDepartments/<int:id>/', v.update_Departments),
    path('MainWarehouse/ViewDataWarehouse/DeleteDepartments/<int:id>/', v.delete_Departments),
    path('MainWarehouse/ViewDataWarehouse/ExportDepartments/CSV', v.export_Departments_to_csv, name='export_Departments_to_csv'),
    path('MainWarehouse/ViewDataWarehouse/ExportDepartments/SQL', v.export_Departments_to_sql, name='export_Departments_to_sql'),
    path('MainWarehouse/ViewDataWarehouse/ImportDepartments/CSV', v.import_csvDepartments, name='import_csvDepartments'),
        
    #Изменение статуса заказа
    path('MainWarehouse/ViewDataWarehouse/UpdateOrderStatus/<int:id>/', v.update_Order_status),
    path('MainWarehouse/ViewDataWarehouse/ViewUserWarehouse/', v.viewdataUserWarehouse, name='ViewdataUserWarehouse'),

    # Экспорт CSV и SQL
    path('MainWarehouse/ViewDataWarehouse/export-query-to-csv/', v.export_buildmaterials_to_csv, name='export_query_to_csv'),
    path('MainWarehouse/ViewDataWarehouse/export-query-to-sql/', v.export_buildmaterials_to_sql, name='export_query_to_sql'),

    # Импорт CSV и SQL
    path('MainWarehouse/ViewDataWarehouse/import-csv', v.import_csvBuildingMaterials, name='import_csvBuildingMaterials'),
    path('MainWarehouse/ViewDataWarehouse/import-sql', v.import_sql, name='import_sql'),

    path('MainAdmin/ViewsLogData', v.view_Loging_user, name='view_Loging_user'),
]
