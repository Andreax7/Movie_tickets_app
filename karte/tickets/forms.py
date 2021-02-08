from django import forms
from django.forms import ModelForm
from .models import Movies, Ticket, User
from django.contrib.auth.forms import UserCreationForm

class VisitorForm(UserCreationForm):
    username = forms.CharField(label="Your Username")
    password1 = forms.CharField(label="Your Password",widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput,label="Repeat Your Password")
    email = forms.EmailField(label = "Email Address")
    first_name = forms.CharField(label = "First Name")
    last_name = forms.CharField(label = "Last Name")
    class Meta:
        model = User
        fields = ['first_name','last_name', 
        'email', 'username',
         'password1']
    def clean_password(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        forms.errors = None
        if (password1 or password2) and password1 != password2:
           raise forms.ValidationError(
               _("Password Mismatch."),
               code='password_mismatch',)        
        return password1
    def save(self, commit=True):
        user=super(UserCreationForm, self).save(commit=False)
        user.set_password(self.clean_password())
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','is_staff']
    def save(self, commit=True):
        if commit:
            user.save()

class MovieForm(ModelForm):
    class Meta:
        model = Movies
        fields = '__all__'

class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['MovieName','Seat', 'user']
        