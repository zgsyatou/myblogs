from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from .models import OAuthRelationship

class LoginForm(forms.Form):
    username_or_email = forms.CharField(label= '用户名或邮箱',
                                        widget=forms.TextInput( 
                                        attrs={'class':'from-control', 'placeholder':'请输入用户名或邮箱'}))
    password = forms.CharField(label= '密码', 
                               widget= forms.PasswordInput(
                               attrs={'class':'from-control', ' placeholder':'请输入密码'}))

    # 定义一个检查用户名与密码的方法
    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email= username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if not user is None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('用户名或者密码不正确')
        else:
            self.cleaned_data['user'] = user  # 返回所获取的清洗过的use，并将其返回到views文件中
        return self.cleaned_data

# 注册
class RegisterForm(forms.Form):
    username = forms.CharField(label= '用户名', 
                               max_length=30,
                               min_length=6,
                               widget=forms.TextInput( 
                               attrs={'class':'from-control', 'placeholder':'请输入3-30位用户名'}))
    email = forms.EmailField(label= '邮箱', 
                             widget=forms.EmailInput( 
                             attrs={'class':'from-control', 'placeholder':'请输入邮箱'}))
    verification_code =forms.CharField(label= '验证码',
                                       required=False, widget=forms.TextInput( 
                                       attrs={'class':'from-control', 'placeholder':'请输入验证码'}))
    password = forms.CharField(label= '密码',
                               min_length=6, 
                               widget= forms.PasswordInput(
                               attrs={'class':'from-control', ' placeholder':'请输入密码,最少6位'}))
    password_agin = forms.CharField(label= '密码',
                                    min_length=6,
                                    widget= forms.PasswordInput(
                                    attrs={'class':'from-control', ' placeholder':'请再输入一次密码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(RegisterForm, self).__init__(*args, **kwargs)

    # 判断验证码
    def cleaned_code(self):
        code = self.request.session.get('bind_email', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return self.cleaned_data
    
    # 定义验证注册的验证输入的数据
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username= username).exists():
            raise forms.ValidationError('用户名已存在')
        return username 

    def clean_Email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email= email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    # 验证两次输入的密码是否一致
    def password_ge_password_agin(self):
        password = self.cleaned_data['password']
        password_agin = self.cleaned_data['password_agin']
        if password != password_agin:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_agin

    # 判断验证码是否为空
    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code

# 昵称表单
class NicknameChangeForm(forms.Form):
    nickname_new = forms.CharField(label= '新昵称', max_length='20', widget=forms.TextInput(
                               attrs={'class':'from-control', 'placeholder':'请输入昵称'})
    )


    # 创建user对象
    def __init__(self, *args, **kwargs ):
        if 'user' in  kwargs:
            self.user = kwargs.pop('user')
        super(NicknameChangeForm, self).__init__(*args, **kwargs)

    # 定义岁评论对象进行鉴别
    def clean(self):
        # 判断用户是否登录
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')
        return self.cleaned_data

    # 定义对输入的nicename进行检查
    def clean_nickname_new(self):
        # 获取表单输入的昵称，去空格
        nickname_new = self.cleaned_data.get('nickname_new', '').strip()
        if nickname_new == '':
            raise forms.ValidationError('新的昵称不能为空，请重新输入！')
        else:
            return nickname_new

# 绑定邮箱
class BindEmailForm(forms.Form):
    email = forms.EmailField(label= '邮箱', 
                             widget=forms.EmailInput( 
                             attrs={'class':'from-control', 'placeholder':'请输入邮箱'}))
    verification_code =forms.CharField(label= '验证码',
                                       required=False, widget=forms.TextInput( 
                                       attrs={'class':'from-control', 'placeholder':'请输入验证码'}))
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登录')

        # 判断用户是否已绑定邮箱
        if self.request.user.email != '':
            raise forms.ValidationError('你已经绑定邮箱')

        # 判断验证码
        code = self.request.session.get('bind_email', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return self.cleaned_data

    # 判断邮箱是否已经绑定
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已经被绑定')
        return email

    # 判断验证码是否为空
    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code

# 修改密码
class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label= '旧密码', 
                               widget= forms.PasswordInput(
                               attrs={'class':'from-control', 'placeholder':'请输入旧密码'}))
    new_password = forms.CharField(label= '新密码', 
                               widget= forms.PasswordInput(
                               attrs={'class':'from-control', 'placeholder':'请输入新密码'}))
    new_password_again = forms.CharField(label= '新密码', 
                               widget= forms.PasswordInput(
                               attrs={'class':'from-control', 'placeholder':'请再次输入新密码'}))

    def __init__(self, *args, **kwargs):
        if 'user' in  kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    # 验证新密码
    def clean(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_again = self.cleaned_data.get('new_password_again', '')
        if new_password != new_password_again or new_password == '':
            raise forms.ValidationError('两次输入密码不一致，请重新输入！')
        return self.cleaned_data

    # 验证旧密码
    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password','')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('旧密码错误，请重新输入！')
        return old_password

# 忘记密码。进行邮箱修改
class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(label= '邮箱', 
                             widget=forms.EmailInput( 
                             attrs={'class':'from-control', 'placeholder':'请输入邮箱'}))
    verification_code =forms.CharField(label= '验证码',
                                       required=False, widget=forms.TextInput( 
                                       attrs={'class':'from-control', 'placeholder':'请输入验证码'}))

    new_password = forms.CharField(label= '密码',
                                   min_length=6, 
                                   widget= forms.PasswordInput(
                                   attrs={'class':'from-control', ' placeholder':'请输入新密码,最少6位'}))
    
    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgetPasswordForm, self).__init__(*args, **kwargs)

    # 验证用户名是否存在
    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email= email).exists():
            raise forms.ValidationError('邮箱不存在，请重新输入！')
        return email

    def clean_verification_code(self):
        # 判断验证码是否为空
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')

        # 判断验证码
        code = self.request.session.get('bind_email', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return verification_code

# 绑定QQ
class BindQQFrom(forms.Form):
    username_or_email = forms.CharField(label= '用户名或邮箱',
                                        widget=forms.TextInput( 
                                        attrs={'class':'from-control', 'placeholder':'请输入用户名或邮箱'}))
    password = forms.CharField(label= '密码', 
                               widget= forms.PasswordInput(
                               attrs={'class':'from-control', ' placeholder':'请输入密码'}))

    # 定义一个检查用户名与密码的方法
    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email= username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if not user is None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('用户名或者密码不正确')
        else:
            self.cleaned_data['user'] = user  # 返回所获取的清洗过的use，并将其返回到views文件中

        # 验证用户丙丁QQ情况
        if OAuthRelationship.objects.filter(user=user, oauth_type=0).exists():
            raise forms.ValidationError('该用户已经绑定QQ账号！')
        return self.cleaned_data