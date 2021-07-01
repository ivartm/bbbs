from django import forms
from django.core.exceptions import ValidationError


class MainAdminForm(forms.ModelForm):
    def clean_questions(self):
        if self.cleaned_data["questions"].count() > 3:
            raise ValidationError("Выбрать можно только 3 вопроса.")
        return self.cleaned_data["questions"]

    def clean_articles(self):
        if self.cleaned_data["articles"].count() > 2:
            raise ValidationError("Выбрать можно только 2 статьи.")
        return self.cleaned_data["articles"]
