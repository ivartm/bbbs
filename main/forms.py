from django.core.exceptions import ValidationError
from django import forms


class MainAdminForm(forms.ModelForm):
    def clean_questions(self):
        if self.cleaned_data["questions"].count() > 3:
            raise ValidationError("Выбрать можно только 3 вопроса.")
        return self.cleaned_data["questions"]
