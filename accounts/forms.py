from django import forms
from .models import Account

class registrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs=
                                                          {'placeholder':'Enter Password',
                                                           'class':'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs=
                                                                  {'placeholder':'Confirm Password'}))
    class Meta:
        model = Account
        fields = ['first_name','last_name', 'phone_number', 'email', 'password']

    def __init__(self,*args, **kwargs):
        super(registrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder']= "Enter first name"
        self.fields['last_name'].widget.attrs['placeholder']= "Enter last name"
        self.fields['phone_number'].widget.attrs['placeholder']= "Enter phone number"
        self.fields['email'].widget.attrs['placeholder']= "Enter Email address"
        for field in self.fields:
            self.fields[field].widget.attrs['class']= "form-control"

    def clean(self):
        cleand_data = super(registrationForm, self).clean()
        password = cleand_data.get('password')
        confirm_password = cleand_data.get('confirm_password')

        if password != confirm_password :
            raise forms.ValidationError('Passwords does not match')