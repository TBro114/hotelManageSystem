# forms.py
from django import forms
from publicModels.models import User

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=255, label="用户名")
    password = forms.CharField(widget=forms.PasswordInput(), label="密码")

class UserRegisterForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(), label="确认密码")

    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'secret_key']
        labels = {
            'username': '用户名',
            'password': '密码',
            'role': '身份',
            'secret_key': '秘钥',
        }
        widgets = {
            'password': forms.PasswordInput(),
            'password2': forms.PasswordInput(),
        }

    def clean_secret_key(self):
        role = self.cleaned_data.get('role')
        secret_key = self.cleaned_data.get('secret_key')
        # 只有在角色为特定值时才验证秘钥
        if role in ['front_desk', 'ac_manager', 'hotel_manager']:
            if not secret_key:
                raise forms.ValidationError('秘钥不能为空')

            # 针对每个角色检查秘钥
            if role == 'front_desk' and secret_key != '123':
                raise forms.ValidationError('秘钥错误，前台秘钥应为 123')
            elif role == 'ac_manager' and secret_key != '456':
                raise forms.ValidationError('秘钥错误，空调管理员秘钥应为 456')
            elif role == 'hotel_manager' and secret_key != '789':
                raise forms.ValidationError('秘钥错误，经理秘钥应为 789')

        return secret_key
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        
        if password and password2:
            if password != password2:
                raise forms.ValidationError('两次输入的密码不一致')
        
        return cleaned_data
