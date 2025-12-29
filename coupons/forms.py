from django import forms

class CouponApplyForm(forms.Form):
    code = forms.CharField(label='کد تخفیف', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'کد تخفیف را وارد کنید'
    }))