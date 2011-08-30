import sys
sys.path.append('/srv/www')
sys.path.append('/srv/www/hntagged')
sys.path.append('/srv/envs/hnenv/lib/python2.6/site-packages')

from django.core.management import setup_environ
from hntagged import settings
setup_environ(settings)

from hn.models import Post, Category
import nltk

posts = Post.objects.filter(category__isnull = False)

documents = []
every_word = []
for post in posts:
    words = post.title.split(' ')
    documents.append((words,post.category.name))
    every_word += words
all_words = nltk.FreqDist([w.lower() for w in every_word])
word_features = all_words.keys()[:2000]

def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    print 'got features'
    return features

featuresets = [(document_features(d), c) for (d,c) in documents]
print 'got featuresets'
train_set, test_set = featuresets[100:], featuresets[:100]
print 'getting classifier.'

classifier = nltk.NaiveBayesClassifier.train(train_set)
print 'got classifier'
print nltk.classify.accuracy(classifier, test_set)
#post=Post.objects.get(pk=2005)
#print document_features(post.title.split(' '))
