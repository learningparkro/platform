from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.utils.translation import ugettext as _

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)

class InstantSearchForm(forms.Form):
    q = forms.CharField(max_length=100)

class SearchOneForm(forms.Form):
    q = forms.CharField(max_length=100)

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text=_('Required. Inform a valid email address.'))

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email
        except MultipleObjectsReturned:
            pass

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError(_('This email address is already in use.'))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
