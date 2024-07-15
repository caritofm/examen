from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cliente, Producto

class CustomerUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=200, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Cliente.objects.create(
                user=user,
                name=self.cleaned_data['name'],
                Email=self.cleaned_data['email']
            )
        return user
    
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['name', 'precio', 'digital', 'image']