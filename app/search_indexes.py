from haystack import indexes
from bjj.app.models import Post

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='author')

    def get_model(self):
        return Post
    def index_queryset(self):
        return self.get_model().objects.all()
