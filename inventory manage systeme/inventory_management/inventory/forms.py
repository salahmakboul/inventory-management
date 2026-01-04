from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import InventoryItem

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField(required=False)
    class Meta :
        model = User
        fields =['username','email','password1','password2']
        

class InventoryItemForm(forms.ModelForm):
     class Meta:
        model = InventoryItem
        fields = ['sujet', 'date_arv','numero'] 
        widgets = {
            'date_arv': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'sujet': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le sujet du message'
            }),
        }
        labels = {
            'sujet': 'Sujet du Message*',
            'date_arv': "Date d'Arrivée*",
        }
        def clean_numero(self):
            numero = self.cleaned_data.get('numero')
            if InventoryItem.objects.filter(numero=numero).exists():
                if self.instance and self.instance.numero == numero:
                    return numero
                raise forms.ValidationError("Ce numéro existe déjà. Veuillez en choisir un autre.")
            return numero