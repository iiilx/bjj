from django.forms import ModelForm
from django.forms.widgets import CheckboxSelectMultiple
from django import forms
from django.contrib.auth.models import User
from bjj.app.models import *
from django.utils.html import strip_tags
from registration.forms import RegistrationForm

class HandleForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('handle',)
    
    def clean_handle(self):
        handle = self.cleaned_data['handle']
        try:
            User.objects.get(username=handle)
            return forms.ValidationError("That username already exists")
        except User.DoesNotExist:
            return self.cleaned_data['handle']


class RegForm(RegistrationForm):
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        user = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if user:
            raise forms.ValidationError('This username is already taken. Please choose another.')
        profile = UserProfile.objects.filter(handle=self.cleaned_data['username'])
        if profile:
            raise forms.ValidationError('This username is already taken. Please choose another.')
        return self.cleaned_data['username']

class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('email', 'belt', 'bio')

class AddPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category','post_url', 'text')

    def clean_title(self):
        return strip_tags(self.cleaned_data['title'])

    def clean_text(self):
        return strip_tags(self.cleaned_data['text'])

    def clean(self):
        post_url = self.cleaned_data['post_url']
        text = self.cleaned_data['text']
        if post_url == '' and text == '':
            raise forms.ValidationError("You must submit either a link or some text")
        return self.cleaned_data

class AddLinkPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'post_url', 'text')
    
    def clean(self):
        if self.cleaned_data['post_url'][0:7] != 'http://':
            raise forms.ValidationError("Submit a valid link starting with http://")
        return self.cleaned_data

class AddTextPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'text')

    def clean_text(self):
        if self.cleaned_data['text'] == '':
            raise forms.ValidationError("You must enter some text")

class PostCatForm(ModelForm):
    def __init__(self, *pa, **ka):
        super(PostCatForm, self).__init__(*pa, **ka)
        self.fields['related_cats'].help_text= ''
    
    class Meta:
        model = Post
        fields = ('category',)

    def clean_category(self):
        if self.cleaned_data['category'] is None:
            raise forms.ValidationError("You must set a primary category.")
        return self.cleaned_data['category']
        
