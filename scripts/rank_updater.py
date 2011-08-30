import sys
sys.path.append('/srv/www')
sys.path.append('/srv/www/hntagged')

import logging
import memcache
import cPickle
import cjson
from datetime import datetime 
from math import ceil

from django.template import Context, Template, loader, RequestContext
from django.core.management import setup_environ
from hntagged import settings
setup_environ(settings)

from hn.models import Post, Category
from hntagged.hn.messaging import process_upvotes

logger = logging.getLogger()
cache = memcache.Client(['127.0.0.1:11211'])
LIMIT = 5000
PPP = 25
MAX_PAGES = LIMIT/PPP
TABLE_TEMPLATE = 'generic_table.html'
CATS_TEMPLATE = 'cached_cats.html'

def calculate_score(votes, item_hour_age, gravity=1.8):
    return votes / pow((item_hour_age + 2), gravity)

def get_html(objects, template):
    return loader.render_to_string(template, {'objects':objects, 'MEDIA_URL':settings.MEDIA_URL})

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def update_uncat_count():
    num_uncat = Post.objects.filter(category=None).count()
    cache.set('uncat_count', str(num_uncat))

def update_latest():
    all_posts = Post.objects.all().order_by('-pk')[:LIMIT]
    count = Post.objects.all().order_by('-pk')[:LIMIT].count()
    chunked = chunks(all_posts, PPP)
    for i, chunk in enumerate(chunked):
        lot = [(post.id, post.post_url, post.title, post.comments_url, post.upvotes, post.author.get_profile().handle if post.author else 0) for post in chunk]
        json = cjson.encode(lot)
        cache.set('latest-%s' % (i+1), json)
    cache.set('latest-ct', get_max_pages(count))

def update_top_cats():
    cats = Category.objects.all()
    for cat in cats:
        all_posts = Post.objects.filter(category = cat).order_by('-pk')[:LIMIT]
        count = Post.objects.filter(category = cat).order_by('-pk')[:LIMIT].count()
        chunked = create_chunked(all_posts)
        for i, chunk in enumerate(chunked): #a chunk is 25 post objects
            lot = [(post.id, post.post_url, post.title, post.comments_url, post.upvotes, post.author.get_profile().handle if post.author else 0) for post in chunk]
            json = cjson.encode(lot)
            cache.set('cat-%s-%s' % (cat.id, (i+1)), json)
        cache.set('cat-ct-%s' % cat.id, get_max_pages(count))

def get_max_pages(count):
    return  int(ceil(count / float(PPP)))

def create_chunked(all_posts):
    posts = []
    now = datetime.now()
    for i, post in enumerate(all_posts):
        delta = now - post.datetime
        hours = delta.seconds / 3600
        score = calculate_score(post.upvotes, hours)
        posts.append((i, score))
    posts.sort(key=lambda tup: tup[1], reverse=True)
    posts_sorted = [all_posts[post[0]] for post in posts]
    chunked = chunks(posts_sorted, PPP)        
    return chunked 

def update_top():
    all_posts = Post.objects.all().order_by('-pk')[:LIMIT]
    count = Post.objects.all().order_by('-pk')[:LIMIT].count()
    chunked = create_chunked(all_posts)        
    for i, chunk in enumerate(chunked):  # a chunk is a list of 25 post objects 
        lot = [(post.id, post.post_url, post.title, post.comments_url, post.upvotes, post.author.get_profile().handle if post.author else 0) for post in chunk]
        json = cjson.encode(lot)
        cache.set('top-%s' % (i+1), json)
    cache.set('top-ct', get_max_pages(count))        

def get_uncat():
    uncat = Post.objects.filter(category=None)
    py = [post.id for post in uncat]
    json = cjson.encode(py)
    cache.set('uncat', json)

def all_cats():
    cats = Category.objects.all()
    lot = [(cat.name, cat.url_name, cat.id) for cat in cats]
    json = cjson.encode(lot)
    cache.set('all-cats', json)

def update_all():
    process_upvotes()
    update_uncat_count()
    update_top_cats()
    update_latest()
    get_uncat()
    update_top() 
    all_cats() 

if __name__ == '__main__':
    update_all() 
