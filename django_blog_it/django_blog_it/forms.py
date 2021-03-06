from django import forms
from .models import Post, Category, Page, Menu, ContactUsSettings
from django.template.defaultfilters import slugify
# for authentication
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'is_active')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if self.instance:
            if User.objects.filter(email=email, username=username).exclude(id=self.instance.id).count():
                raise forms.ValidationError(u'Email addresses must be unique.')
        else:
            if User.objects.filter(email=email).exclude(username=username).count():
                raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        for field in iter(self.fields):
            if max(enumerate(iter(self.fields)))[0] != field:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control',
                    "placeholder": "Please enter your " + field.capitalize()
                })

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

class AdminLoginForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Incorrect Login Details")

        return self.cleaned_data


class BlogPostForm(forms.ModelForm):
    tags = forms.CharField(label="Tags", max_length=300, required=False)

    class Meta:
        model = Post
        exclude = ('slug', 'user', 'tags')

    def __init__(self, *args, **kwargs):
        self.is_superuser = kwargs.pop('is_superuser', None)
        self.user_role = kwargs.pop('user_role', None)
        super(BlogPostForm, self).__init__(*args, **kwargs)
        if self.is_superuser or self.user_role != 'Author':
            pass
        else:
            del self.fields['status']
        for field in iter(self.fields):

            if field == 'tags':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control myTags', "placeholder": "Please enter your Blog " + field.capitalize()
                })

            else:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control', "placeholder": "Please enter your Blog " + field.capitalize()
                })


class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ('slug',)

    def clean_name(self):
        if not self.instance.id:
            if Category.objects.filter(slug=slugify(self.cleaned_data['name'])).exists():
                raise forms.ValidationError('Category with this Name already exists.')
        else:
            if Category.objects.filter(name__icontains=self.cleaned_data['name']).exclude(id=self.instance.id):
                raise forms.ValidationError('Category with this Name already exists.')

        return self.cleaned_data['name']

    def __init__(self, *args, **kwargs):
        super(BlogCategoryForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            if max(enumerate(iter(self.fields)))[0] != field:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control', "placeholder": "Please enter your Category " + field.capitalize()
                })


class UserRoleForm(forms.Form):
    role = forms.CharField(max_length=10)


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        exclude = ('slug',)

    def __init__(self, *args, **kwargs):
        super(PageForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            if max(enumerate(iter(self.fields)))[0] != field:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control', "placeholder": "Please enter your Page " + field.capitalize()
                })


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        exclude = ('lvl',)

    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)

        for field in iter(self.fields):
            if max(enumerate(iter(self.fields)))[0] != field:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control', "placeholder": "Please enter your Menu " + field.capitalize()
                })

class ContactUsSettingsForm(forms.ModelForm):

    class Meta:
        model = ContactUsSettings
        exclude = ()
