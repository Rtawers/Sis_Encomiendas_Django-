# envios/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Encomienda
from clientes.models import Cliente
from rutas.models import Ruta


class EncomiendaForm(forms.ModelForm):
    """
    Formulario para registrar o editar una encomienda.
    """
    class Meta:
        model = Encomienda
        
        # ✅ SOLO estos campos (SIN codigo, SIN costo_envio, SIN empleado_registro)
        fields = [
            'descripcion',
            'peso_kg',
            'volumen_cm3',
            'remitente',
            'destinatario',
            'ruta',
            'fecha_entrega_est',
            'observaciones',
        ]
        
        # Widgets con Bootstrap
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'peso_kg': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'volumen_cm3': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'remitente': forms.Select(attrs={'class': 'form-select'}),
            'destinatario': forms.Select(attrs={'class': 'form-select'}),
            'ruta': forms.Select(attrs={'class': 'form-select'}),
            'fecha_entrega_est': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
        
        # Labels
        labels = {
            'descripcion': 'Descripción',
            'peso_kg': 'Peso (kg)',
            'volumen_cm3': 'Volumen (cm³)',
            'remitente': 'Remitente',
            'destinatario': 'Destinatario',
            'ruta': 'Ruta',
            'fecha_entrega_est': 'Fecha estimada de entrega',
            'observaciones': 'Observaciones',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar solo clientes activos
        self.fields['remitente'].queryset = Cliente.objects.activos()
        self.fields['destinatario'].queryset = Cliente.objects.activos()
        self.fields['ruta'].queryset = Ruta.objects.filter(estado=1)

    def clean(self):
        """
        Validaciones cruzadas.
        """
        cleaned_data = super().clean()
        remitente = cleaned_data.get('remitente')
        destinatario = cleaned_data.get('destinatario')
        fecha_entrega_est = cleaned_data.get('fecha_entrega_est')

        # Regla 1: Remitente y destinatario no pueden ser la misma persona
        if remitente and destinatario and remitente == destinatario:
            self.add_error(
                'destinatario',
                ValidationError('El remitente y el destinatario no pueden ser la misma persona.')
            )

        # Regla 2: La fecha de entrega estimada no puede ser en el pasado
        if fecha_entrega_est and fecha_entrega_est < timezone.now().date():
            self.add_error(
                'fecha_entrega_est',
                ValidationError('La fecha de entrega estimada no puede ser en el pasado.')
            )

        return cleaned_data