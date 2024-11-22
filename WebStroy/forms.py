from django import forms
from .models import *
from django.core.validators import FileExtensionValidator


class UsersForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UsersForm, self).__init__(*args, **kwargs)
        self.fields['fk_pasport_data'].widget=forms.HiddenInput()
        self.fields['fk_role'].widget=forms.HiddenInput()
        self.fields['surname'].widget=forms.TextInput(
            attrs={
                'placeholder':'Введите Фамилию',
                'required':'True',
                'minlength':'1',
                'maxlength':'20',
                'type':'text',
                'pattern': '[a-zA-Zа-яА-Я]*',
                'title':"Можно вводить только буквы"
            }
        )
        self.fields['name'].widget=forms.TextInput(
            attrs={
                'placeholder':'Введите имя',
                'required':'True',
                'minlength': '3',
                'maxlength': '20',
                'pattern': '[a-zA-Zа-яА-Я]*',
                'title': "Можно вводить только буквы"
            }
        )
        self.fields['midellname'].widget = forms.TextInput(
            attrs={
                'placeholder': 'Введите Отчество',
                'minlength': '5',
                'maxlength': '20',
                'pattern': '[a-zA-Zа-яА-Я]*',
                'title': "Можно вводить только буквы",
            }
        )
        self.fields['date_birth'].widget = forms.DateInput(
            attrs={
                'placeholder': 'Выберите Дату рождения',
                'required': 'True',
                'type':'date',
                'min':"1940-01-01",
                'max':"2006-01-01"
            }
        )
        self.fields['number_phone'].widget = forms.TextInput(
            attrs={
                'placeholder': 'Введите Номер телефона',
                'required': 'True',
                'minlength': '11',
                'maxlength': '11',
                'pattern': '[0-9]*',
                'title': "Можно вводить только цифры"
            }
        )
        self.fields['login'].widget = forms.TextInput(
            attrs={
                'placeholder': 'Придумайте логин',
                'required': 'True',
                'minlength': '5',
                'maxlength': '20',
            }
        )
        self.fields['password'].widget = forms.PasswordInput(
            attrs={
                'placeholder': 'Придумайте Пароль',
                'required': 'True',
                'minlength': '8',
                'maxlength': '20',
            }
        )

    class Meta:
        model = Users
        fields = '__all__'


class CartForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CartForm, self).__init__(*args, **kwargs)
        self.fields['fk_build_material'].widget=forms.HiddenInput()
        self.fields['fk_cart'].widget=forms.HiddenInput()
        self.fields['count_build_material'].widget = forms.NumberInput(
            attrs={
                'placeholder': 'Введите колличество товара',
                'required': 'True',
                'type': 'number',
                'min':"1",
                'max':"100",
                'style':"width: 240px;"
            }
        )
    class Meta:
        model = ItemCart
        fields = '__all__'

class ItemCartForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemCartForm, self).__init__(*args, **kwargs)
        self.fields['fk_cart'].widget=forms.HiddenInput()
        self.fields['count_build_material'].widget = forms.NumberInput(
            attrs={
                'placeholder': 'Введите колличество товара',
                'required': 'True',
                'type': 'number',
                'min':"1",
                'max':"100",
                'style':"width: 240px;"
            }
        )
    class Meta:
        model = ItemCart
        fields = '__all__'

class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['price'].widget = forms.NumberInput(
            attrs={
                'required': 'True',
                'type': 'number',
                'readonly':'True'
            }
        )
        self.fields['the_method_of_obtaining'].widget.attrs['disabled'] = 'disabled'
        self.fields['payment_method'].widget.attrs['disabled'] = 'disabled'
        self.fields['delivery_address'].widget=forms.TextInput(
            attrs={
                'required': 'True',
                'readonly':'True'
            }
        )
        self.fields['fk_cart'].widget=forms.HiddenInput()
        self.fields['fk_users'].widget=forms.HiddenInput()
        self.fields['status_order'].widget=forms.HiddenInput()

    class Meta:
        model = Orders
        fields = '__all__'

class OrderUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderUpdateForm, self).__init__(*args, **kwargs)
        self.fields['price'].widget = forms.NumberInput(
            attrs={
                'required': 'True',
                'type': 'number',
                'readonly':'True'
            }
        )
        self.fields['the_method_of_obtaining'].widget.attrs['disabled'] = 'disabled'
        self.fields['payment_method'].widget.attrs['disabled'] = 'disabled'
        self.fields['delivery_address'].widget=forms.TextInput(
            attrs={
                'required': 'True'
            }
        )
        self.fields['fk_cart'].widget=forms.HiddenInput()
        self.fields['fk_users'].widget=forms.HiddenInput()
        self.fields['status_order'].widget=forms.HiddenInput()

    class Meta:
        model = Orders
        fields = '__all__'


class AddNewUsersForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddNewUsersForms, self).__init__(*args, **kwargs)
        self.fields['fk_pasport_data'].widget=forms.HiddenInput()
        self.fields['surname'].widget=forms.TextInput(
            attrs={
                'placeholder':'Введите Фамилию',
                'required':'True',
                'minlength':'1',
                'maxlength':'20',
                'type':'text',
                'pattern': '[a-zA-Zа-яА-Я]*',
                'title':"Можно вводить только буквы"
            }
        )
        self.fields['name'].widget=forms.TextInput(
            attrs={
                'placeholder':'Введите имя',
                'required':'True',
                'minlength': '3',
                'maxlength': '20',
                'pattern': '[a-zA-Zа-яА-Я]*',
                'title': "Можно вводить только буквы"
            }
        )
        self.fields['midellname'].widget = forms.TextInput(
            attrs={
                'placeholder': 'Введите Отчество',
                'minlength': '5',
                'maxlength': '20',
                'pattern': '[a-zA-Zа-яА-Я]*',
                'title': "Можно вводить только буквы",
            }
        )
        self.fields['date_birth'].widget = forms.DateInput(
            attrs={
                'placeholder': 'Выберите Дату рождения',
                'required': 'True',
                'type':'date',
                'min':"1940-01-01",
                'max':"2006-01-01"
            }
        )
        self.fields['number_phone'].widget = forms.TextInput(
            attrs={
                'placeholder': 'Введите Номер телефона',
                'required': 'True',
                'minlength': '11',
                'maxlength': '11',
                'pattern': '[0-9]*',
                'title': "Можно вводить только цифры"
            }
        )
        self.fields['login'].widget = forms.TextInput(
            attrs={
                'placeholder': 'Придумайте логин',
                'required': 'True',
                'minlength': '5',
                'maxlength': '20',
            }
        )
        self.fields['password'].widget = forms.PasswordInput(
            attrs={
                'placeholder': 'Придумайте Пароль',
                'required': 'True',
                'minlength': '8',
                'maxlength': '20',
            }
        )

    class Meta:
        model = Users
        fields = '__all__'

class AddNewPassportData(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddNewPassportData, self).__init__(*args, **kwargs)
        self.fields['seria_passport'].widget = forms.TextInput(
            attrs={
                'placeholder': 'Введите серию паспорта',
                'required': 'True',
                'minlength': '4',
                'maxlength': '4',
                'pattern': '[0-9]*',
                'title': "Можно вводить только цифры"
            }
        )
        self.fields['number_passport'].widget = forms.TextInput(
            attrs={
                'placeholder': 'Введите номер паспорта',
                'required': 'True',
                'minlength': '6',
                'maxlength': '6',
                'pattern': '[0-9]*',
                'title': "Можно вводить только цифры"
            }
        )
        self.fields['date_give'].widget=forms.DateInput(
            attrs={
                'placeholder': 'Выберите Дату выдачи',
                'required': 'True',
                'type':'date',
                'min':"1940-01-01",
                'max':"2006-01-01"
            }
        )
        self.fields['code_podrazdelenia'].widget=forms.TextInput(
            attrs={
                'placeholder': 'Введите код подразделения',
                'required': 'True',
                'minlength': '6',
                'maxlength': '6',
                'pattern': '[0-9]*',
                'title': "Можно вводить только цифры"
            }
        )
    class Meta:
        model = PasportData
        fields = '__all__'

class AddNewRole(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddNewRole, self).__init__(*args, **kwargs)
    class Meta:
        model = Role
        fields = '__all__'

class AddNewTypeMaterials(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddNewTypeMaterials, self).__init__(*args, **kwargs)
    class Meta:
        model = TypeMaterial
        fields='__all__'

class AddNewManufactires(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddNewManufactires, self).__init__(*args, **kwargs)
    class Meta:
        model=Manufacturer
        fields='__all__'

class AddNewWarehouses(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddNewWarehouses, self).__init__(*args, **kwargs)
    class Meta:
        model=Warehouse
        fields='__all__'

class AddNewBuildMaterial(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddNewBuildMaterial, self).__init__(*args, **kwargs)
    class Meta:
        model = BuildingMaterials
        fields='__all__'

class AddNewDepartments(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddNewDepartments, self).__init__(*args, **kwargs)
    class Meta:
        model = Departaments
        fields='__all__'

class UpdateOrderStatus(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateOrderStatus, self).__init__(*args, **kwargs)
        self.fields['status_order'].widget=forms.TextInput(
            attrs={
                'placeholder': 'Введите статус',
                'required': 'True',
                'minlength': '5',
                'maxlength': '50',
            }
        )
    class Meta:
        model=Orders
        fields=['status_order']

# импрорт CSV и SQL
class ImportFormCSV(forms.Form):
    csv_file = forms.FileField(label="Файл",
                            validators=[FileExtensionValidator(allowed_extensions=["csv"])])
    
class ImportFormSQL(forms.Form):
    sql_file = forms.FileField(label="Файл",
                            validators=[FileExtensionValidator(allowed_extensions=["sql"])])