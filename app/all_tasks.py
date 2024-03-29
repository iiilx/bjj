import sys
import os

PROJECT_DIR = os.path.abspath(os.path.join(__file__, '../..'))
STAGING_DIR = os.path.abspath(os.path.join(__file__, '../../..'))
sys.path.append(PROJECT_DIR)
sys.path.append(STAGING_DIR)

from django.core.management import setup_environ
from bjj import settings
setup_environ(settings)
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache

import logging
import cPickle

from datetime import datetime, timedelta 
from math import ceil
from app.messaging import process_upvotes
from app.models import Post, Category
from custom_threadedcomments.models import CustomThreadedComment
from poll.models import Poll

logger = logging.getLogger()
LIMIT = 5000
PPP = 25
MAX_PAGES = LIMIT/PPP
TABLE_TEMPLATE = 'generic_table.html'
CATS_TEMPLATE = 'cached_cats.html'
post_ctype = ContentType.objects.get(name="post")

def get_top_polls():
    n=3
    polls = Poll.objects.all()
    poll_count = Poll.objects.all().count()
    n = poll_count if poll_count < n else n
    poll_list = []
    for poll in polls:
        count = 0
        for choice in poll.choice_set.all(): 
            count += choice.votes
        poll_list.append((poll, count))
    poll_list.sort(key=lambda tup: tup[1], reverse=True)
    i = 0
    top_polls=[]
    while i < n:
        top_polls.append(poll_list[i][0].pk)
        i +=1
    cache.set('top_polls', cPickle.dumps(top_polls))

def get_comment_count(post_pk):
    return CustomThreadedComment.objects.filter(content_type=post_ctype, object_pk=post_pk).count()

def get_most_discussed():
    posts = Post.objects.all()
    posts_and_counts = [(post, get_comment_count(post.pk)) for post in posts]
    posts_and_counts.sort(key = lambda tup: tup[1], reverse=True)
    top3 = [(tup[0].pk, tup[0].title) for tup in posts_and_counts[0:3]]
    cache.set('top3', cPickle.dumps(top3))

def calculate_score(votes, item_hour_age, gravity=1.8):
    return votes / pow((item_hour_age + 2), gravity)

def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def update_uncat_count():
    num_uncat = Post.objects.filter(category=None).count()
    cache.set('uncat_count', str(num_uncat))

def update_latest2():
    all_posts = Post.objects.all().order_by('-pk')[:LIMIT]
    count = Post.objects.all().order_by('-pk')[:LIMIT].count()
    chunked = chunks(all_posts, PPP)
    for i, chunk in enumerate(chunked):
        pks = [post.id for post in chunk]
        cache.set('latest-%s' % (i+1), cPickle.dumps(pks))
    cache.set('latest-ct', get_max_pages(count))

def update_top_cats2():
    cats = Category.objects.all()
    for cat in cats:
        all_posts = Post.objects.filter(category = cat).order_by('-pk')[:LIMIT]
        count = Post.objects.filter(category = cat).order_by('-pk')[:LIMIT].count()
        chunked = create_chunked(all_posts)
        for i, chunk in enumerate(chunked): #a chunk is 25 post objects
            pks = [post.id for post in chunk]
            cache.set('cat-%s-%s' % (cat.id, (i+1)), cPickle.dumps(pks))
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

def update_top2():
    all_posts = Post.objects.all().order_by('-pk')[:LIMIT]
    count = Post.objects.all().order_by('-pk')[:LIMIT].count()
    chunked = create_chunked(all_posts)        
    for i, chunk in enumerate(chunked):  # a chunk is a list of 25 post objects 
        pks = [post.id for post in chunk]
        cache.set('top-%s' % (i+1), cPickle.dumps(pks))
    max_pages = get_max_pages(count)
    cache.set('top-ct', max_pages)        

def update_all():
    update_top_cats2()
    update_latest2()
    get_most_discussed()
    update_top2() 
    get_top_polls()

if __name__ == '__main__':
    update_all() 
