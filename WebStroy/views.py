import codecs
from django.shortcuts import render, redirect
from .forms import *
from django.core.signing import Signer
from django.http import HttpResponse
import csv
import psycopg2
from django.contrib import messages
import datetime
# Create your views here.

o = 0
login = ''
password = ''
idid = 0
Name = ''
Last_name = ''
Middel_name = ''
IsCreate = False
cklad = ''
adress = ''
pay = ''
NumberCard = ''
Crok = ''
Cvc = ''


def write_logger_user(me):  # логирование пользователей
    singer=Signer()
    # Подключение к БД
    conn = psycopg2.connect("dbname='WriteLogger' user='postgres' host='127.0.0.1' password='123'")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO public.logger_user(surname, name, midellname, login, password, message, date_and_time) VALUES ('{singer.sign_object(Last_name)}', '{singer.sign_object(Name)}', '{singer.sign_object(Middel_name)}', '{singer.sign_object(login)}', '{singer.sign_object(password)}', '{singer.sign_object(me)}', '{datetime.datetime.now()}');")
    conn.commit()
    conn.close()


def Main(request):  # главная страница пользователя
    materials=BuildingMaterials.objects.all()
    if o == 0:
        return render(request, 'User/Main.html', {'auth': 'Вы не авторизованы поэтому вы "Гость"',
                                             'materials': materials})
    if o == 1:
        search = request.POST.get('search')
        if search != None:
            materials = BuildingMaterials.objects.filter(name__icontains=search)
        global IsCreate
        if IsCreate==False:
            user=Users.objects.filter(pk=idid)
            try:
                Cart.objects.filter(fk_users=idid)
            except Cart.DoesNotExist:
                Cart.objects.create(fk_users=user)
            IsCreate=True
        if request.method == "POST":
            formCart = CartForm(request.POST)
            if formCart.is_valid():
                new_cart=Cart.objects.create(fk_users=idid)
                car = formCart.save(commit=False)
                car.fk_cart = new_cart
                car.fk_building_materials = materials
                car.save()
                return redirect('Main')
        else:
            formCart = CartForm(initial={'fk_users':idid, 'fk_building_materials':materials})
        return render(request, 'User/Main.html', {'auth': f'Вы авторизованы под логином - {login}',
                                             'materials': materials, 'formCart': formCart})

def MainAdmin(request):
    materials=BuildingMaterials.objects.all()
    return render(request, 'SysAdmin/AdminMain.html', {'auth': 'Вы авторизовались под Админестратора',
                                             'materials': materials})

def ViewUsers(request):
    return render(request, 'SysAdmin/ViewUsers.html', {'Users':Users.objects.all()})

def AddUser(request):
    singer = Signer()
    if request.POST:
        formNEWPASSPORTDATA = AddNewPassportData(request.POST)
        formNEWUSERS = AddNewUsersForms(request.POST)
        if formNEWPASSPORTDATA.is_valid() and formNEWUSERS.is_valid():
            nar = formNEWUSERS.save(commit=False)
            nar.surname = singer.sign_object(nar.surname)
            nar.name = singer.sign_object(nar.name)
            nar.midellname = singer.sign_object(nar.midellname)
            nar.number_phone = singer.sign_object(nar.number_phone)
            nar.login = singer.sign_object(nar.login)
            nar.password = singer.sign_object(nar.password)
            formNEWPASSPORTDATA.save()
            nar.fk_pasport_data = PasportData.objects.latest('pk')
            nar.save()
            return redirect('ViewUsers')
    else:
        formNEWUSERS = AddNewUsersForms()
        formNEWPASSPORTDATA = AddNewPassportData()
    return render(request, 'SysAdmin/AddUsers.html', {'formUsers':formNEWUSERS, 'formPassport': formNEWPASSPORTDATA})

def ViewDataAdmin(request):
    Data = "Нажмите на кнопку, чтобы вывелись данные, из конкретной таблицы"
    view = request.POST.get('view')
    if view == "Отделы":
        Data = Departaments.objects.all()
    elif view == "Производители":
        Data = Manufacturer.objects.all()
    elif view == "Заказы":
        Data = Orders.objects.all()
    elif view == "Роли":
        Data = Role.objects.all()
    elif view == "Склады":
        Data = Warehouse.objects.all()
    elif view == "Типы материала":
        Data = TypeMaterial.objects.all()
    return render(request, 'SysAdmin/ViewDataAdmin.html', { 'Data':Data, 'view':view })

def auth(request):
    global idid
    global login
    global password
    global Name
    global Middel_name
    global Last_name
    singer = Signer()
    log = request.POST.get('log')
    pas = request.POST.get('pass')
    print(log)
    print(pas)

    if request.method == "POST":
        for i in Users.objects.all():
            print(singer.unsign_object(i.login))
            print(singer.unsign_object(i.password))
            if singer.unsign_object(i.login) == log and singer.unsign_object(i.password) == pas and i.fk_role.name=='Head of Warehouses':
                idid = i.pk
                login = singer.unsign_object(i.login)
                password = singer.unsign_object(i.password)
                idid = i.pk
                Name = singer.unsign_object(i.name)
                Middel_name = singer.unsign_object(i.midellname)
                Last_name = singer.unsign_object(i.surname)
                write_logger_user('Авторизовался в системе')
                return redirect('MainWarehouse')
            if singer.unsign_object(i.login) == log and singer.unsign_object(i.password) == pas and i.fk_role.name=='Admin':
                idid = i.pk
                login = singer.unsign_object(i.login)
                password = singer.unsign_object(i.password)
                idid = i.pk
                Name = singer.unsign_object(i.name)
                Middel_name = singer.unsign_object(i.midellname)
                Last_name = singer.unsign_object(i.surname)
                write_logger_user('Авторизовался в системе')
                return redirect('MainAdmin')
            if singer.unsign_object(i.login) == log and singer.unsign_object(i.password) == pas and i.fk_role.name=='User':
                global o
                o = 1
                login = singer.unsign_object(i.login)
                password = singer.unsign_object(i.password)
                idid = i.pk
                Name = singer.unsign_object(i.name)
                Middel_name = singer.unsign_object(i.midellname)
                Last_name = singer.unsign_object(i.surname)
                print(idid)
                print(i.fk_role.name)
                write_logger_user("Авторизовался в системе")
                return redirect('Main')
    return render(request, 'User/auth.html')


def regis(request):
    singer = Signer()
    role = Role.objects.get(name='User')
    if request.method == "POST":
        formUsers = UsersForm(request.POST)
        if formUsers.is_valid():
            nar = formUsers.save(commit=False)
            nar.fk_role = role
            nar.surname = singer.sign_object(nar.surname)
            nar.name = singer.sign_object(nar.name)
            nar.midellname = singer.sign_object(nar.midellname)
            nar.number_phone = singer.sign_object(nar.number_phone)
            nar.login = singer.sign_object(nar.login)
            nar.password = singer.sign_object(nar.password)
            global login
            login = singer.unsign_object(nar.login)
            global password
            password = singer.unsign_object(nar.password)
            global idid
            idid = nar.pk
            formUsers.save()
            global o
            o=1
            return redirect('Main')
    else:
        formUsers = UsersForm(initial={'fk_role': role.id})
    return render(request, 'User/regis.html', {'formUsers': formUsers})


def Ord(request):
    materials = ItemCart.objects.filter(fk_cart__fk_users_id=idid)
    orders = Orders.objects.filter(fk_cart__fk_users_id=idid)
    return render(request, 'User/Orders.html', {'Orders':orders, 'Materials':materials})

def Add_cart(request, pk):
    clothers=BuildingMaterials.objects.get(pk=pk)
    user = Users.objects.get(pk=idid)
    if request.method == "POST":
        form = CartForm(request.POST)
        if form.is_valid():
            nar = form.save(commit=False)
            nar.fk_cart = Cart.objects.get(fk_users=user)
            nar.fk_build_material = clothers
            nar.save()
            write_logger_user("Добавил строительный материал в корзину")
            return redirect('Main')
    else:
        form=CartForm(initial={'fk_cart': Cart.objects.get(fk_users=user), 'fk_build_material': clothers.id})
    return render(request, 'User/add_card.html', {'form': form, 'material':clothers})


def cart(request):
    cart = ItemCart.objects.filter(fk_cart__fk_users=idid)
    return render(request, 'User/cart.html', {'car':cart})

def Update_cart(request, id):
    user = Users.objects.get(pk=idid)
    update=ItemCart.objects.get(pk=id)
    if request.method == "POST":
        form = ItemCartForm(request.POST, instance=update)
        if form.is_valid():
            nar = form.save(commit=False)
            nar.fk_cart = Cart.objects.get(fk_users=user)
            nar.save()
            write_logger_user("Изменил корзину")
            return redirect('cart')
    else:
        form = ItemCartForm(initial={'fk_cart':Cart.objects.get(fk_users=user)})
    return render(request, 'User/item_cart.html', {'form':form})

def upOrdownCountCart(request, id, min_or_plus):
    update = ItemCart.objects.get(pk=id)
    if min_or_plus == '+':
        update.count_build_material+=1
    if min_or_plus == '-':
        update.count_build_material-=1
    if update.count_build_material>=1:
        update.save()
    return redirect('cart')

def deletecart(request, id):
    delcart = ItemCart.objects.get(id=id)
    delcart.delete()
    write_logger_user("Удалил корзину")
    return redirect('cart')

# выбор способа оплаты и написание данных о банковской карты
def choose_pay(request):
    global pay
    pay = request.POST.get('oplati')
    Cvc = request.POST.get('CVC')
    Crok = request.POST.get('Crok')
    NumberCard = request.POST.get('NumberCard')
    if Cvc != None and NumberCard != None and Crok != None:
        pay = 'Банковская карта'
        return redirect('dilivery')
    if pay == 'Наличными':
        return redirect('dilivery')
    if pay == None:
        return render(request, 'User/choose_method_oplati.html', {'opla': Orders.objects.all()})
    if pay == 'Банковская карта':
        return render(request, 'User/write_BankCard.html')
    

# выбор способа доставки, написание адресса и выбора склада
def choose_dilivery(request):
    global adress, cklad
    adress = request.POST.get('adress')
    if adress != None:
        return redirect('Add_order')
    cklad = request.POST.get('diliveri')
    if cklad == None:
        return render(request, 'User/choose_method_diliveri.html')
    if cklad == 'Забрать со склада':
        return render(request, 'User/choose_cklad.html', {'Cklads':Warehouse.objects.all()})
    if cklad == 'Заказать доставку':
        return render(request, 'User/write_adress.html')
    
def add_Order(request):
    user = Users.objects.get(pk=idid)
    pre=0
    global cklad, pay
    if cklad == 'Забрать со склада':
        cklad=Orders.CKLAD
    if cklad == 'Заказать доставку':
        cklad=Orders.COURIER
    if pay == 'Банковская карта':
        pay=Orders.BANCCARD
    if pay == 'Наличными':
        pay=Orders.MONEY

    for i in ItemCart.objects.filter(fk_cart__fk_users=idid):
        pre = (i.count_build_material*i.fk_build_material.price) + pre
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            nar = form.save(commit=False)
            nar.fk_cart = Cart.objects.get(fk_users=user)
            nar.fk_users = Users.objects.get(pk=idid)
            nar.price = pre
            nar.delivery_address = adress
            nar.payment_method = pay
            nar.the_method_of_obtaining = cklad
            nar.status_order = 'Принят на обработку'
            nar.save()
            write_logger_user("Добавил заказ")
            return redirect('order')
    else:
        form = OrderForm(initial={'fk_cart':Cart.objects.get(fk_users=user),
                                  'fk_users':Users.objects.get(pk=idid),
                                  'price':pre,
                                  'delivery_address':adress,
                                  'payment_method':pay,
                                  'the_method_of_obtaining':cklad,
                                  'status_order':'Принят на обработку'})
    return render(request, 'User/add_order.html', {'form':form})

def update_Order(request, id):
    user = Users.objects.get(pk=idid)
    update = Orders.objects.get(pk=id)
    print(update.payment_method)
    print(update.the_method_of_obtaining)
    pre=0
    for i in ItemCart.objects.filter(fk_cart__fk_users=idid):
        pre = (i.count_build_material*i.fk_build_material.price) + pre
    if request.method == "POST":
        form = OrderUpdateForm(request.POST, instance=update)
        if form.is_valid():
            nar = form.save(commit=False)
            nar.fk_cart = Cart.objects.get(fk_users=user)
            nar.fk_users = Users.objects.get(pk=idid)
            nar.price = pre
            nar.payment_method = update.payment_method
            nar.the_method_of_obtaining = update.the_method_of_obtaining
            nar.status_order = update.status_order
            nar.save()
            write_logger_user("Изменил заказ")
            return redirect('order')
    else:
        form = OrderUpdateForm(initial={'fk_cart':Cart.objects.get(fk_users=user),
                                  'fk_users':Users.objects.get(pk=idid),
                                  'price':pre, 
                                  'payment_method':update.payment_method,
                                  'the_method_of_obtaining': update.the_method_of_obtaining,
                                  'status_order':update.status_order})
    return render(request, 'User/update_order.html', {'form':form})
        
def deletOrder(request, id):
    delorder = Orders.objects.get(id=id)
    delorder.delete()
    write_logger_user("Удалил заказ")
    return redirect('order')

def deleteUser(request, id):
    deluser = Users.objects.get(id=id)
    deluser.delete()
    write_logger_user("Удалил пользователя")
    return redirect('ViewUsers')

def Add_new_role(request):
    if request.POST:
        formRole=AddNewRole(request.POST)
        if formRole.is_valid():
            formRole.save()
            write_logger_user("Добавил новую роль")
        return redirect('ViewData')
    formRole=AddNewRole()
    return render(request, 'SysAdmin/Add_Role.html', {'formRole':formRole})

def Update_role(request, id):
    role=Role.objects.get(id=id)
    if request.POST:
        formRole=AddNewRole(request.POST, instance=role)
        if formRole.is_valid():
            formRole.save()
            write_logger_user("Изменил роль")
            return redirect ('ViewData')
    formRole=AddNewRole()
    return render(request, 'SysAdmin/Update_Role.html', {'formRole':formRole})

def Delete_role(request, id):
    delrole = Role.objects.get(id=id)
    delrole.delete()
    write_logger_user("Удалил роль")
    return redirect('ViewData')

################################Начальник склада
def MainWarehouse(request):
    materials=BuildingMaterials.objects.all()
    return render(request, 'Warehouse/WarehouseMain.html', {'auth': 'Вы авторизовались под Начальником склада',
                                             'materials': materials})

def ViewDataWarehouse(request):
    Data = "Нажмите на кнопку, чтобы начать работу с данными, из конкретной таблицы"
    view = request.POST.get('view')
    if view == "Отделы":
        Data = Departaments.objects.all()
    elif view == "Производители":
        Data = Manufacturer.objects.all()
    elif view == "Заказы":
        Data = Orders.objects.all()
    elif view == "Склады":
        Data = Warehouse.objects.all()
    elif view == "Типы материала":
        Data = TypeMaterial.objects.all()
    elif view == "Строительные материалы":
        Data = BuildingMaterials.objects.all()
    return render(request, 'Warehouse/ViewDataWarehouse.html', {'Data':Data, 'view':view})

#Тип материала
###########################################################################################
def AddNewTypeMaterial(request): # Добавление типа метериала
    if request.POST:
        formTypeMaterial=AddNewTypeMaterials(request.POST)
        if formTypeMaterial.is_valid():
            formTypeMaterial.save()
            write_logger_user("Добавил новый тип материала")
        return redirect('ViewDataWarehouse')
    formTypeMaterial=AddNewTypeMaterials()
    return render(request, 'Warehouse/AddTypeMaterial.html', {'formTypeMaterial':formTypeMaterial})

def Update_TypeMaterial(request, id): # Изменение типа материала
    typeMaterial=TypeMaterial.objects.get(id=id)
    if request.POST:
        formtypeMaterial=AddNewTypeMaterials(request.POST, instance=typeMaterial)
        if formtypeMaterial.is_valid():
            formtypeMaterial.save()
            write_logger_user("Изменил тип материала")
            return redirect ('ViewDataWarehouse')
    formtypeMaterial=AddNewTypeMaterials()
    return render(request, 'Warehouse/UpdateTypeMaterial.html', {'formtypeMaterial':formtypeMaterial})


def Delete_TypeMaterial(request, id): # Удаление типа материала
    delTypeMaterial = TypeMaterial.objects.get(id=id)
    delTypeMaterial.delete()
    write_logger_user("Удалил тип материала")
    return redirect('ViewDataWarehouse')

def export_TypeMaterial_to_csv(request): #Экспорт CSV тип материалов
    data = TypeMaterial.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=TypeMaterials.csv'

    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response)
    writer.writerow(['Название типа',])

    for BuildMaterial in data:
        writer.writerow([
            BuildMaterial.name_type,
        ])
    write_logger_user("Осуществил экспорт данных об типов материалов в формате CSV")
    return response

def export_TypeMaterial_to_sql(request): #Экспорт SQL тип материалов
    response = HttpResponse(content_type='test/sql')
    response['Content-Disposition'] = 'attachment; filename="TypeMaterials.sql"'
    sql_commands=[]
    data = TypeMaterial.objects.all()
    for item in data:
        sql = f"INSERT INTO type_material (name_type) VALUES ('{item.name_type}');\n"
        sql_commands.append(sql)
    response.content = ''.join(sql_commands)
    write_logger_user("Осуществил экспорт данных об типов материалов в формате SQL")
    return response

def import_csvTypeMaterial(request): #Импорт CSV тип материалов
    if request.method == 'POST':
        form = ImportFormCSV(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file'].read().decode('utf-8-sig').splitlines()
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader:
                print(row.keys())
                TypeMaterial.objects.create(
                    name_type=row['Название типа'],
                )
            write_logger_user("Осуществил импорт данных об типов материалов в формате CSV")
            return redirect('ViewDataWarehouse')
    else:
        form = ImportFormCSV()
    return render(request, 'Warehouse/import_csv.html', {'form':form})


###################################################################################################

#Производители
##################################################################################################
def AddNewManufactire(request):# Добавление производителя
    if request.POST:
        formManufactire=AddNewManufactires(request.POST)
        if formManufactire.is_valid():
            formManufactire.save()
            write_logger_user("Добавил нового производителя")
        return redirect('ViewDataWarehouse')
    formManufactire=AddNewManufactires()
    return render(request, 'Warehouse/AddManifacture.html', {'formManufactire':formManufactire})

def Update_Manufactire(request, id): # Изменение производителя
    Manifacture=Manufacturer.objects.get(id=id)
    if request.POST:
        formManifacture=AddNewManufactires(request.POST, instance=Manifacture)
        if formManifacture.is_valid():
            formManifacture.save()
            write_logger_user("Изменил производителя")
            return redirect ('ViewDataWarehouse')
    formManifacture=AddNewManufactires()
    return render(request, 'Warehouse/UpdateManifacture.html', {'formManifacture':formManifacture})


def Delete_Manufactire(request, id): # Удаление производителя
    delManufactire = Manufacturer.objects.get(id=id)
    delManufactire.delete()
    write_logger_user("Удалил производителя")
    return redirect('ViewDataWarehouse')

def export_Manufactire_to_csv(request): #Экспорт CSV производителей
    data = Manufacturer.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Manufacturers.csv'

    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response)
    writer.writerow(['Название производителя', 'Страна',])

    for BuildMaterial in data:
        writer.writerow([
            BuildMaterial.name_manufacturer,
            BuildMaterial.country,
        ])
    write_logger_user("Осуществил экспорт данных об производителях в формате CSV")
    return response

def export_Manufactire_to_sql(request): #Экспорт SQL производителей
    response = HttpResponse(content_type='test/sql')
    response['Content-Disposition'] = 'attachment; filename="Manufactire.sql"'
    sql_commands=[]
    data = Manufacturer.objects.all()
    for item in data:
        sql = f"INSERT INTO Manufacturer (name_manufacturer, country) VALUES ('{item.name_manufacturer}', '{item.country}');\n"
        sql_commands.append(sql)
    response.content = ''.join(sql_commands)
    write_logger_user("Осуществил экспорт данных об производителях в формате SQL")
    return response

def import_csvManufactire(request): #Импорт CSV производителей
    if request.method == 'POST':
        form = ImportFormCSV(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file'].read().decode('utf-8-sig').splitlines()
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader:
                print(row.keys())
                Manufacturer.objects.create(
                    name_manufacturer=row['Название производителя'],
                    country = row['Страна'],
                )
            write_logger_user("Осуществил импорт данных об производителях в формате CSV")
            return redirect('ViewDataWarehouse')
    else:
        form = ImportFormCSV()
    return render(request, 'Warehouse/import_csv.html', {'form':form})


##########################################################################################

#Склад
##########################################################################################
def AddNewWarehouse(request):# Добавление Склада
    if request.POST:
        formWarehouse=AddNewWarehouses(request.POST)
        if formWarehouse.is_valid():
            formWarehouse.save()
            write_logger_user("Добавил новый склад")
        return redirect('ViewDataWarehouse')
    formWarehouse=AddNewWarehouses()
    return render(request, 'Warehouse/AddWarehouse.html', {'formWarehouse':formWarehouse})

def Update_Warehouse(request, id): # Изменение склада
    warehouse=Warehouse.objects.get(id=id)
    if request.POST:
        formwarehouse=AddNewWarehouses(request.POST, instance=warehouse)
        if formwarehouse.is_valid():
            formwarehouse.save()
            write_logger_user("Изменил склад")
            return redirect ('ViewDataWarehouse')
    formwarehouse=AddNewWarehouses()
    return render(request, 'Warehouse/UpdateWarehouse.html', {'formwarehouse':formwarehouse})


def Delete_Warehouse(request, id): # Удаление склада
    delWarehouse = Warehouse.objects.get(id=id)
    delWarehouse.delete()
    write_logger_user("Удалил склад")
    return redirect('ViewDataWarehouse')

def export_Warehouse_to_csv(request): #Экспорт CSV склада
    data = Warehouse.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Warehouses.csv'
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response)
    writer.writerow(['Название склада', 'Адресс склада',])
    for BuildMaterial in data:
        writer.writerow([
            BuildMaterial.name_warehouse,
            BuildMaterial.adress_warehouse,
        ])
    write_logger_user("Осуществил экспорт данных об складах в формате CSV")
    return response

def export_Warehouse_to_sql(request): #Экспорт SQL склада
    response = HttpResponse(content_type='test/sql')
    response['Content-Disposition'] = 'attachment; filename="Warehouses.sql"'
    sql_commands=[]
    data = Warehouse.objects.all()
    for item in data:
        sql = f"INSERT INTO Warehouse (name_warehouse, adress_warehouse) VALUES ('{item.name_warehouse}', '{item.adress_warehouse}');\n"
        sql_commands.append(sql)
    response.content = ''.join(sql_commands)
    write_logger_user("Осуществил экспорт данных об складах в формате SQL")
    return response

def import_csvWarehouse(request): #Импорт CSV склада
    if request.method == 'POST':
        form = ImportFormCSV(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file'].read().decode('utf-8-sig').splitlines()
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader:
                if Warehouse.objects.filter(name_warehouse=row['Название склада'], adress_warehouse=row['Адресс склада']):
                    print('Данные уже находяться в БД')
                else:
                    print(row.keys())
                    Warehouse.objects.create(
                        name_warehouse=row['Название склада'],
                        adress_warehouse=row['Адресс склада'],
                    )
            write_logger_user("Осуществил импорт данных об складах в формате CSV")
            return redirect('ViewDataWarehouse')
    else:
        form = ImportFormCSV()
    return render(request, 'Warehouse/import_csv.html', {'form':form})


#Строительные материалы
########################################################################################

def add_Buildmaterials(request):#добавление строительного материала
    if request.POST:
        formBuildMaterial = AddNewBuildMaterial(request.POST)
        if formBuildMaterial.is_valid():
            formBuildMaterial.save()
            write_logger_user("Добавление нового строительного материала")
            return redirect('ViewDataWarehouse')
    formBuildMaterial=AddNewBuildMaterial()
    return render(request, 'Warehouse/AddBuildMaterial.html', {'formBuildMaterial':formBuildMaterial})

def update_Buildmaterials(request, id):# Изменение строительного материала
    BuildingMaterial = BuildingMaterials.objects.get(id=id)
    if request.POST:
        formBuildMaterial = AddNewBuildMaterial(request.POST, instance=BuildingMaterial)
        if formBuildMaterial.is_valid():
            formBuildMaterial.save()
            write_logger_user("Изменение строительного материала")
            return redirect('ViewDataWarehouse')
    formBuildMaterial=AddNewBuildMaterial()
    return render(request, 'Warehouse/UpdateBuildMaterial.html', {'formBuildMaterial':formBuildMaterial})

def delete_Buildmaterials(request, id):#удаление строительного материала
    delBuildmaterials = BuildingMaterials.objects.get(id=id)
    delBuildmaterials.delete()
    write_logger_user("Удаление строительного материала")
    return redirect('ViewDataWarehouse')

def export_buildmaterials_to_csv(request): #Экспорт CSV Строительных материалов
    data = BuildingMaterials.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=BuildingMaterials.csv'

    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response)
    writer.writerow(['name', 'description', 'price', 'Manufacturer', 'Type_material'])

    for BuildMaterial in data:
        writer.writerow([
            BuildMaterial.name, BuildMaterial.description, BuildMaterial.price,
            BuildMaterial.fk_manufacturer, BuildMaterial.fk_type_material
        ])
    write_logger_user("Осуществил экспорт данных об строительных материалов в формате CSV")
    return response

def export_buildmaterials_to_sql(request): #Экспорт SQL Строительных материалов
    response = HttpResponse(content_type='test/sql')
    response['Content-Disposition'] = 'attachment; filename="BuildingMaterials.sql"'
    sql_commands=[]
    data = BuildingMaterials.objects.all()
    for item in data:
        sql = f"INSERT INTO building_materials (name, description, price, fk_manufacturer, fk_type_material) VALUES ('{item.name}', '{item.description}', {item.price}, {item.fk_manufacturer.pk}, {item.fk_type_material.pk});\n"
        sql_commands.append(sql)
    response.content = ''.join(sql_commands)
    write_logger_user("Осуществил экспорт данных об строительных материалов в формате SQL")
    return response

def import_csvBuildingMaterials(request): #Импорт CSV Строительных материалов
    if request.method == 'POST':
        form = ImportFormCSV(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file'].read().decode('utf-8-sig').splitlines()
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader:
                print(row.keys())
                BuildingMaterials.objects.create(
                    name=row['name'],
                    description=row['description'],
                    price=row['price'],
                    fk_manufacturer=Manufacturer.objects.get(pk = row['Manufacturer']),
                    fk_type_material=TypeMaterial.objects.get(pk = row['Type_material'])
                )
            write_logger_user("Осуществил импорт данных об строительных материалах в формате CSV")
            return redirect('ViewDataWarehouse')
    else:
        form = ImportFormCSV()
    return render(request, 'Warehouse/import_csv.html', {'form':form})

############################################################################################################

#Отделы
############################################################################################################
def add_Departments(request):#Добавление отдела
    if request.POST:
        formDepartment = AddNewDepartments(request.POST)
        if formDepartment.is_valid():
            formDepartment.save()
            write_logger_user("Добавление нового отдела")
            return redirect('ViewDataWarehouse')
    formDepartment=AddNewDepartments()
    return render(request, 'Warehouse/AddDepartments.html', {'formDepartment':formDepartment})

def update_Departments(request, id):# Изменение отдела
    departaments = Departaments.objects.get(id=id)
    if request.POST:
        formDepartment = AddNewDepartments(request.POST, instance=departaments)
        if formDepartment.is_valid():
            formDepartment.save()
            write_logger_user("Изменение отдела")
            return redirect('ViewDataWarehouse')
    formDepartment=AddNewDepartments()
    return render(request, 'Warehouse/UpdateDepartment.html', {'formDepartment':formDepartment})


def delete_Departments(request, id):#Удаление отдела
    delDepartments = Departaments.objects.get(id=id)
    delDepartments.delete()
    write_logger_user("Удаление отдела")
    return redirect('ViewDataWarehouse')

def export_Departments_to_csv(request): #Экспорт CSV Отделов
    data = Departaments.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Departaments.csv'

    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response)
    writer.writerow(['Колличество', 'Склад', 'Строительный материал'])

    for BuildMaterial in data:
        writer.writerow([
            BuildMaterial.counts,
            BuildMaterial.fk_warehouse,
            BuildMaterial.fk_building_materials])
    write_logger_user("Осуществил экспорт данных об отделов в формате CSV")
    return response

def export_Departments_to_sql(request): #Экспорт SQL Отделов
    response = HttpResponse(content_type='test/sql')
    response['Content-Disposition'] = 'attachment; filename="Departaments.sql"'
    sql_commands=[]
    data = Departaments.objects.all()
    for item in data:
        sql = f"INSERT INTO Departaments (counts, fk_warehouse, fk_building_materials) VALUES ('{item.counts}', {item.fk_warehouse.pk}, {item.fk_building_materials.pk});\n"
        sql_commands.append(sql)
    response.content = ''.join(sql_commands)
    write_logger_user("Осуществил экспорт данных об отделов в формате SQL")
    return response

def import_csvDepartments(request): #Импорт CSV Отделов
    if request.method == 'POST':
        form = ImportFormCSV(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file'].read().decode('utf-8-sig').splitlines()
            csv_reader = csv.DictReader(csv_file, delimiter=';')
            for row in csv_reader:
                print(row.keys())
                Departaments.objects.create(
                    counts=row['Колличество'],
                    fk_warehouse = Warehouse.objects.get(name_warehouse=row['Склад']),
                    fk_building_materials= BuildingMaterials.objects.get(name=row['Строительный материал'])
                )
            write_logger_user("Осуществил импорт данных в формате SQL")
            return redirect('ViewDataWarehouse')
    else:
        form = ImportFormCSV()
    return render(request, 'Warehouse/import_csv.html', {'form':form})


#Статус заказов
##############################################################################################

def update_Order_status(request, id):
    update_order = Orders.objects.get(id=id)
    if request.POST:
        formupdatestatus = UpdateOrderStatus(request.POST, instance=update_order)
        if formupdatestatus.is_valid():
            formupdatestatus.save()
            write_logger_user("Изменение статуса заказа")
            return redirect('ViewDataWarehouse')
    formupdatestatus=UpdateOrderStatus()
    return render(request, 'Warehouse/UpdateOrderStatus.html', {'formupdatestatus':formupdatestatus})

def viewdataUserWarehouse(request):
    singer = Signer()
    surname=''
    name=''
    midellname=''
    date_birth=''
    number_phone=''
    login=''
    password=''
    fk_pasport_data=0
    fk_role=0
    for i in Users.objects.filter(pk=idid):
        surname=singer.unsign_object(i.surname)
        name=singer.unsign_object(i.name)
        midellname=singer.unsign_object(i.midellname)
        date_birth=i.date_birth
        number_phone=singer.unsign_object(i.number_phone)
        login=singer.unsign_object(i.login)
        password=singer.unsign_object(i.password)
        fk_pasport_data=i.fk_pasport_data
        fk_role=i.fk_role
    return render(request, 'Warehouse/ViewUserWarehouse.html', {'surname':surname, 'name':name, 'midellname':midellname,
                                                                'date_birth':date_birth, 'number_phone':number_phone,
                                                                'login':login, 'password':password, 
                                                                'fk_pasport_data':fk_pasport_data, 'fk_role':fk_role})


def import_sql(request): # Импорт SQL
    if request.method == 'POST':
        form = ImportFormSQL(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['sql_file']
            try:
                conn = psycopg2.connect("dbname='TRZBDWEBStroY' user='postgres' host='127.0.0.1' password='123'")
                cur = conn.cursor()
                cur.execute(file.read().decode('utf-8'))
                conn.commit()
                conn.close()
                messages.success(request, 'Данные импортированы успешно')
                write_logger_user("Осуществил импорт данных в формате SQL")
                return redirect('ViewDataWarehouse')
            except Exception as e:
                messages.error(request, 'При импорте данных произошла ошибка' + e)
    else:
        form = ImportFormSQL()
    return render(request, 'Warehouse/import_sql.html', {'form':form})

def view_Loging_user(request):
    singer=Signer()
    Logger = []
    conn = psycopg2.connect("dbname='WriteLogger' user='postgres' host='127.0.0.1' password='123'")
    cur = conn.cursor()
    cur.execute(f"SELECT id, surname, name, midellname, login, password, message, date_and_time FROM public.logger_user;")
    for row in cur.fetchall():
        Logger.append({'id': row[0]})
        Logger.append({'surname': singer.unsign_object(row[1])})
        Logger.append({'name': singer.unsign_object(row[2])})
        Logger.append({'midellname': singer.unsign_object(row[3])})
        Logger.append({'login': singer.unsign_object(row[4])})
        Logger.append({'password': singer.unsign_object(row[5])})
        Logger.append({'message': singer.unsign_object(row[6])})
        Logger.append({'date_and_time': row[7]})
    conn.commit()
    conn.close()
    return render(request, 'SysAdmin/ViewLogginUser.html', {'Log': Logger})