# home/forms.py

from django import forms

class ManualPricingForm(forms.Form):
    width_drawer = forms.FloatField(label="عرض الادر (A)")
    height_side = forms.FloatField(label="ارتفاع الجانب (B)")
    thickness_side = forms.FloatField(label="تخانة الجانب (C)")
    thickness_drawer = forms.FloatField(label="تخانة الدرج (D)")
