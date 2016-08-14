from django import forms

class loginForm(forms.Form):
    usernameField = forms.CharField(label='usrname', max_length=30)
    passwordField = forms.CharField(label='pssword', max_length=100)

class signupForm(forms.Form):
    usernameField = forms.CharField(label='usrname', max_length=30)
    emailField = forms.CharField(label='email', max_length=30)
    firstNameField = forms.CharField(label='firstName', max_length=30)
    passwordField = forms.CharField(label='pssword', max_length=100)
    imageField = forms.ImageField()

class settingsForm(forms.Form):
    emailField = forms.CharField(label='email', max_length=30)
    firstNameField = forms.CharField(label='firstName', max_length=30)
    imageField = forms.ImageField()


class questionForm(forms.Form):
    titleField = forms.CharField(label='title', max_length=200)
    questionTextField = forms.CharField(label='questionText', widget = forms.Textarea)
    tagsField = forms.CharField(label='tags', max_length=300)

class answerForm(forms.Form):
    answerTextField = forms.CharField(label='answerText', widget=forms.Textarea)