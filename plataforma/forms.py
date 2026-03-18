from django import forms
from .models import Staff

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['nombre', 'cargo', 'descripcion', 'categoria', 'imagen', 'descripcion_back']

    def clean_categoria(self):
        categoria = (self.cleaned_data.get('categoria') or '').strip().lower()
        valid = {key for key, _ in Staff.CATEGORIAS}
        if categoria not in valid:
            raise forms.ValidationError(
                'Categoria invalida. Use: ' + ', '.join(sorted(valid))
            )
        return categoria
