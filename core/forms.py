from django import forms

class PagoMatriculaForm(forms.Form):
    id_alumno = forms.IntegerField()
    nombre_padre = forms.CharField(max_length=255)
    email_padre = forms.EmailField()
    monto = forms.DecimalField(max_digits=10, decimal_places=2)
    banco = forms.CharField(max_length=100)
    metodo_pago = forms.ChoiceField(choices=[('tarjeta', 'Tarjeta'), ('transferencia', 'Transferencia')])
