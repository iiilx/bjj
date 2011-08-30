from bjj.custom_threadedcomments.models import CustomThreadedComment
from bjj.custom_threadedcomments.forms import CustomThreadedCommentForm

def get_model():
    return CustomThreadedComment

def get_form():
    return CustomThreadedCommentForm
