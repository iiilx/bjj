from haystack import indexes
from poll.models import Poll

class PollIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Poll 

    def index_queryset(self):
        return self.get_model().objects.all()
