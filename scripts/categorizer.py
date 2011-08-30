import sys
sys.path.append('/srv/www')
sys.path.append('/srv/www/hntagged')

import logging
import memcache
import cjson
from datetime import datetime 
from math import ceil

from django.template import Context, Template, loader, RequestContext
from django.core.management import setup_environ
from hntagged import settings
setup_environ(settings)

from hn.models import Post, Category, Tag

logger = logging.getLogger()
cache = memcache.Client(['127.0.0.1:11211'])

ALL_CATS = cjson.decode(cache.get('all-cats'))

def check_common(link):
    text=link.split(' ')
    #print 'checking %s' % text
    cats=[]
    for cat in ALL_CATS:
        #print 'cat[0] = %s' % cat[0]
        cat_name = cat[0].lower()
        #print 'catname is %s' % cat_name
        l=len(cat_name.split(' '))
        if l == 1 and cat_name in text:
            #print 'got category from category name: %s' % cat[0]
            cats.append((Category.objects.get(pk=cat[2]), text.index(cat_name)))
        elif l > 1 and cat_name in link:
            #print 'got category from category name: %s' % cat[0]
            cats.append((Category.objects.get(pk=cat[2]), 0 ))
        else:
            pass
    return cats 

def check_common_orig(link):
    text=link.split(' ')
    #print 'checking %s' % text
    cats=[]
    for cat in ALL_CATS:
        #print 'cat[0] = %s' % cat[0]
        cat_name = cat[0].lower()
        #print 'catname is %s' % cat_name
        if cat_name in text:
            #print 'got category from category name: %s' % cat[0]
            cats.append((Category.objects.get(pk=cat[2]), text.index(cat_name)))
    return cats 

def checkEqual3(lst):
    return lst[1:] == lst[:-1]

def choose_best(cats):
    #which category occurs first in sentence
    cats.sort(key=lambda tup: tup[1])
    #print cats 
    if checkEqual3([t[0].id for t in cats]): # all same
        return cats[0][0]
    #if that category is in another category's text, use the latter. 
    skip = False
    for tup in cats:
        l=[t[0].name.lower() for t in cats]
        l.remove(tup[0].name.lower())
        #print 'l is ' + repr(l)
        for name in l:
            if tup[0].name.lower() in name:
                skip = True
                break
        if skip:
            #print 'skipping to next cat'
            continue
        return tup[0] 
    return None
 
def check_tags(link):
    #print 'checking tags'
    text=link.split(' ')
    cats=[]
    for tag in Tag.objects.all():
        tag_name = tag.name.lower()
        #print 'checking tag: %s' % tag_name
        if tag_name in text:
            #print 'got category from tag: %s' % tag_name
            cats.append((tag.category, text.index(tag_name)))
    return cats

def categorize(post):
    link = post.title.replace(':','').replace('(','').replace(')','').replace('/',' ').lower()
    url = post.post_url
    cats = False 
    cats = check_common(link)
    cat = None
    if cats:
        cat = choose_best(cats)
    else:
        cats = check_tags(link)
        if cats:
            cat = choose_best(cats)
    if cat is not None:        
        #print 'chose cat %s' % cat
        p=Post.objects.get(pk=post.id)
        p.category = cat
        p.save()
        #print 'saved'
    else:
        pass

def categorize_all():
    uncat = Post.objects.filter(category = None) 
    for i, post in enumerate(uncat):
        #if not 'firefox' in post.title.lower():
        #    print 'no firefox'
        #    continue 
        #else:
        #    print 'firefox!'
        #print 'categorizing post %r...' % post.title 
        categorize(post)
        #if i == 100:
        #    break

if __name__ == '__main__':
    categorize_all() 
