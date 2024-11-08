from django import forms
from django.core.exceptions import ValidationError

class VagaForm(forms.Form):
    titulo = forms.CharField(max_length=150 , required=True)
    empresa = forms.CharField(max_length=150, required=True)
    telefone = forms.CharField(max_length=20, required=True)
    descritivo = forms.CharField(max_length=255, required=True )
    email = forms.EmailField(required=True)

    def clean_titulo(self):
        nome = self.cleaned_data['titulo']
        return nome.upper()

    def clean_empresa(self):
        empresa = self.cleaned_data['empresa']
        if len(empresa) < 2:
            raise ValidationError('Empresa precisa ter ao menos dois caracteres')
        return empresa.capitalize()
    
    def clean_email(self):
        email = self.cleaned_data['email']
        return email

    def clean_telefone(self):
        telefone = self.cleaned_data['telefone']
        if telefone.startswith('19'):
            return telefone
        raise ValidationError('DDD válido somente o 19')
    

    def clean_descritivo(self):
        descritivo = self.cleaned_data['descritivo'] 
        if len(descritivo) < 10:
            raise ValidationError('Precisa ter 10')
        return descritivo

    