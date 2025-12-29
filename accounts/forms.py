from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # 👈 AuthenticationForm رو اضافه کن
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    # اینجا فیلدها رو فارسی و خوشگل می‌کنیم
    username = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
        help_text='' # این خط اون متن‌های اضافی زیر نام کاربری رو حذف میکنه
    )
    
    email = forms.EmailField(
        label='ایمیل (اختیاری)',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'})
    )

    class Meta:
        model = User
        fields = ['username', 'email'] # فیلدهایی که نشون داده میشن

    # این تابع برای خوشگل کردن فیلدهای پسورده
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # فارسی کردن لیبل پسوردها
        self.fields['password1'].label = "رمز عبور"
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'حداقل ۸ کاراکتر'
        })
        # متن راهنمای زشت انگلیسی رو با این جمله کوتاه عوض میکنیم:
        self.fields['password1'].help_text = "رمز عبور باید حداقل ۸ کاراکتر و ترکیبی از حروف و اعداد باشد."

        self.fields['password2'].label = "تکرار رمز عبور"
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'رمز را مجدد وارد کنید'
        })
        self.fields['password2'].help_text = ""

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری خود را وارد کنید'})
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'رمز عبور خود را وارد کنید'})
    )