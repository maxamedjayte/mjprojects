from darulxadith_system.models import Mustawaha
from django import forms
from django.forms import fields, models
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime

# class MustawaForm(forms.ModelForm):
#     class Meta:
#         model=Mustawaha
#         fields=('magacaMustawaha','sanadDugsiyeedka','maadoyinka')
#         widgets={
#             'magacaMustawaha':forms.TextInput(attrs={'class':'form-control'}),
#             'sanadDugsiyeedka':forms.Select(attrs={'class':'form-control'}),
#             'maadoyinka':forms.TextInput(attrs={'class':'form-control'})
#         }
