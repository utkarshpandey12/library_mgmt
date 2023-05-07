from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', max_length=20)


user_role_type_choices =(
    ("Member", "Member"),
    ("Librarian", "Librarian"),
)
class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(label='Password', max_length=20)
    user_type = forms.ChoiceField(label='User Role Type',choices = user_role_type_choices)

