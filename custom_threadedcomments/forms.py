import datetime

from django.conf import settings
from django.contrib.comments.forms import CommentDetailsForm
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.utils.encoding import force_unicode
from threadedcomments.forms import ThreadedCommentForm

from bjj.custom_threadedcomments.models import CustomThreadedComment

class CustomThreadedCommentForm(CommentDetailsForm):
    parent = forms.IntegerField(required=False, widget=forms.HiddenInput)

    def __init__(self, target_object, parent=None, data=None, initial=None):
        self.parent = parent
        if initial is None:
            initial = {}
        initial.update({'parent': self.parent})
        super(CustomThreadedCommentForm, self).__init__(target_object, data=data,
            initial=initial)
        del self.fields['url']        
        del self.fields['name']
        del self.fields['email']

    def get_comment_model(self):
        return CustomThreadedComment

    def get_comment_create_data(self):
        return dict(
            content_type = ContentType.objects.get_for_model(self.target_object),
            object_pk    = force_unicode(self.target_object._get_pk_val()),
            comment      = self.cleaned_data["comment"],
            submit_date  = datetime.datetime.now(),
            site_id      = settings.SITE_ID,
            is_public    = True,
            is_removed   = False,
            parent_id    = self.cleaned_data['parent']
        )
