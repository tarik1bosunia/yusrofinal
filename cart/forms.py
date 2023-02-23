from django import forms
from cart.models import Order, Division, City, Area

DELIVERY_TYPE_CHOICES = [
    (1, 'Standard'),
    (2, 'Express'),
    (3, 'Next day'),
    (4, 'Scheduled'),
]


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, label='First Name*', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter first name', 'required': True}))
    last_name = forms.CharField(max_length=50, label='Last Name*', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter last name', 'required': True}))
    email = forms.EmailField(label='Email*', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter email', 'required': True}))
    phone = forms.CharField(max_length=20, label='Phone Number*', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter phone number', 'required': True}))
    division = forms.ModelChoiceField(
        queryset=Division.objects.all(),
        empty_label=("Choose Division", {"disabled": 'disabled', "selected": "selected"}),
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'get_cities_by_division();'}),
    )

    city = forms.ModelChoiceField(
        queryset=City.objects.none(),
        empty_label='Select City',
        widget=forms.Select(attrs={'class': 'form-control', 'onchange': 'get_areas_by_city();'}))
    area = forms.ModelChoiceField(
        queryset=Area.objects.none(),
        empty_label='Select Area',
        widget=forms.Select(attrs={'class': 'form-control'}))

    delivery_type = forms.ChoiceField(choices=DELIVERY_TYPE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'division', 'city', 'area', 'delivery_type', 'address_1', 'address_2', 'note']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        self.fields['division'].empty_label = "Choose Division"
        self.fields['city'].empty_label = "Choose City"
        self.fields['area'].empty_label = "Choose Area"

        if 'division' in self.data:
            try:
                division_id = int(self.data.get('division'))
                self.fields['city'].queryset = City.objects.filter(division_id=division_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.division.city_set.order_by('name')

        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['area'].queryset = Area.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['area'].queryset = self.instance.city.area_set.order_by('name')



    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if 'initial' in kwargs:
    #         division_id = kwargs['initial']['division'].id
    #         self.fields['city'].queryset = City.objects.filter(division_id=division_id)
    #         self.fields['area'].queryset = Area.objects.none()
    #
    #     if self.instance.pk:
    #         self.fields['city'].queryset = City.objects.filter(division=self.instance.division)
    #         self.fields['area'].queryset = Area.objects.filter(city=self.instance.city)

    # first_name = forms.CharField(max_length=50, label='First Name*', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name', 'required': True}))
    # last_name = forms.CharField(max_length=50, label='Last Name*', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name', 'required': True}))
    # email = forms.EmailField(label='Email*', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email', 'required': True}))
    # phone = forms.CharField(max_length=20, label='Phone Number*', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number', 'required': True}))
    # division = forms.ChoiceField(choices=[('default', 'Choose Your Division'), ('1', 'Dhaka'), ('2', 'Barisal'), ('3', 'Chittagong'), ('4', 'Khulna'), ('5', 'Mymensingh'), ('6', 'Rajshahi'), ('7', 'Rangpur'), ('8', 'Sylhet')], label='Division', widget=forms.Select(attrs={'class': 'form-select bg-gray-200'}))
    # city = forms.ChoiceField(choices=[('default', 'Choose Your City')], label='City', widget=forms.Select(attrs={'class': 'form-select bg-gray-200'}))
    # area = forms.ChoiceField(choices=[('default', 'Choose Your Area')], label='Area', widget=forms.Select(attrs={'class': 'form-select bg-gray-200'}))
    # delivery_type = forms.ChoiceField(choices=[('default', 'Choose Your Delivery Type'), ('6', 'Free Delivery [Applicable For Fully Paid]'), ('8', 'Outside Rajshahi | Sundarban (48hrs to 72hrs) | 1% COD')], label='Delivery Type*', widget=forms.Select(attrs={'class': 'form-select bg-gray-200', 'required': True}))
    # address_1 = forms.CharField(max_length=100, label='Address 1*', widget=forms.TextInput(attrs={'class': 'form-control bg-gray-200', 'required': True}))
    # address_2 = forms.CharField(max_length=100, label='Address 2', widget=forms.TextInput(attrs={'class': 'form-control bg-gray-200'}))
    # note = forms.CharField(max_length=500, label='Note (Optional)', widget=forms.Textarea(attrs={'class': 'form-control my-2 bg-white text-black', 'placeholder': 'Write any note here (Optional)'}))