import sys
sys.path.append('/srv/www')
sys.path.append('/srv/www/bjj')

from django.core.management import setup_environ
from bjj import settings
setup_environ(settings)
from django.contrib.contenttypes.models import ContentType

import logging
import memcache
import cjson
import cPickle

from datetime import datetime, timedelta 
from math import ceil
from bjj.app.messaging import process_upvotes
from bjj.app.models import Post, Category
from bjj.custom_threadedcomments.models import CustomThreadedComment
from poll.models import Poll

logger = logging.getLogger()
cache = memcache.Client(['127.0.0.1:11211'])
LIMIT = 5000
PPP = 25
MAX_PAGES = LIMIT/PPP
TABLE_TEMPLATE = 'generic_table.html'
CATS_TEMPLATE = 'cached_cats.html'
PREFIX = settings.PREFIX
post_ctype = ContentType.objects.get(name="post")

def get_top_polls():
    polls = Poll.objects.all()
    poll_list = []
    for poll in polls:
        count = 0
        for choice in poll.choice_set.all(): 
            count += choice.votes
        poll_list.append((poll, count))
    poll_list.sort(key=lambda tup: tup[1], reverse=True)
    top_polls_by_id = [tup[0].pk for tup in poll_list]

def get_comment_count(post_pk):
    return CustomThreadedComment.objects.filter(content_type=post_ctype, object_pk=post_pk).count()

def get_most_discussed():
    posts = Post.objects.all()
    posts_and_counts = [(post, get_comment_count(post.pk)) for post in posts]
    posts_and_counts.sort(key = lambda tup: tup[1], reverse=True)
    top3 = [(tup[0].pk, tup[0].title) for tup in posts_and_counts[0:3]]
    cache.set('%s-top3' % PREFIX, cPickle.dumps(top3))

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
    cache.set('%s-uncat_count' % PREFIX, str(num_uncat))

def update_latest2():
    all_posts = Post.objects.all().order_by('-pk')[:LIMIT]
    count = Post.objects.all().order_by('-pk')[:LIMIT].count()
    chunked = chunks(all_posts, PPP)
    for i, chunk in enumerate(chunked):
        lot = [(post.id, post.post_url, post.title, post.upvotes, post.author.get_profile().handle if post.author else 0, get_comment_count(post.pk), post.is_youtube) for post in chunk]
        path = '/srv/www/bjj/latest-%s.txt' % i
        cache.set('%s-latest-%s' % (PREFIX, (i+1)), cPickle.dumps(lot))
    cache.set('%s-latest-ct' % PREFIX, get_max_pages(count))

def update_top_cats2():
    cats = Category.objects.all()
    for cat in cats:
        all_posts = Post.objects.filter(category = cat).order_by('-pk')[:LIMIT]
        count = Post.objects.filter(category = cat).order_by('-pk')[:LIMIT].count()
        chunked = create_chunked(all_posts)
        for i, chunk in enumerate(chunked): #a chunk is 25 post objects
            lot = [(post.id, post.post_url, post.title, post.upvotes, post.author.get_profile().handle if post.author else 0, get_comment_count(post.pk), post.is_youtube) for post in chunk]
            cache.set('%s-cat-%s-%s' % (PREFIX, cat.id, (i+1)), cPickle.dumps(lot))
            #print str == cache.get('%s-top-%s' % (PREFIX, (i+1))) 
            #print repr(cPickle.loads(str))
        cache.set('%s-cat-ct-%s' % (PREFIX, cat.id), get_max_pages(count))

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

def update_top2():
    all_posts = Post.objects.all().order_by('-pk')[:LIMIT]
    count = Post.objects.all().order_by('-pk')[:LIMIT].count()
    chunked = create_chunked(all_posts)        
    for i, chunk in enumerate(chunked):  # a chunk is a list of 25 post objects 
        lot = [(post.id, post.post_url, post.title, post.upvotes, post.author.get_profile().handle if post.author else 0, get_comment_count(post.pk), post.is_youtube) for post in chunk]
        cache.set('%s-top-%s' % (PREFIX, (i+1)), cPickle.dumps(lot))
    max_pages = get_max_pages(count)
    #print 'max pages: %s' % max_pages
    cache.set('%s-top-ct' % PREFIX, max_pages)        
    #print max_pages
    #print cache.get('bjj-top-ct')

def get_uncat():
    uncat = Post.objects.filter(category=None)
    py = [post.id for post in uncat]
    json = cjson.encode(py)
    cache.set('%s-uncat' % PREFIX, json)

def all_cats():
    cats = Category.objects.all()
    lot = [(cat.name, cat.url_name, cat.id) for cat in cats]
    json = cjson.encode(lot)
    cache.set('%s-all-cats' % PREFIX, json)

def update_all():
    #update_uncat_count()
    update_top_cats2()
    update_latest2()
    get_most_discussed()
    #get_uncat()
    update_top2() 
    get_top_polls()
    #all_cats() 
    #process_upvotes()

if __name__ == '__main__':
    update_all() 
