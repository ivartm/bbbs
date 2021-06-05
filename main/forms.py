from django.core.exceptions import ValidationError
from django import forms


class MainAdminForm(forms.ModelForm):
    def clean_questions(self):
        if self.cleaned_data["questions"].count() > 4:
            raise ValidationError("Выбрать можно только 4 вопроса.")
        return self.cleaned_data["questions"]
