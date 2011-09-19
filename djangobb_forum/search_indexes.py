from haystack import indexes
#from haystack import site
#from haystack.indexes import *

#import djangobb_forum.models as models
from djangobb_forum.models import Post

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='user')
    created = indexes.DateTimeField(model_attr='created')
    topic = indexes.CharField(model_attr='topic')
    category = indexes.CharField(model_attr='topic__forum__category__name')
    forum = indexes.IntegerField(model_attr='topic__forum__pk')

    def get_model(self):
        return Post
#site.register(models.Post, PostIndex)
