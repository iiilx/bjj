import sys
import cjson
import cPickle

from urllib import urlencode
from random import choice
from datetime import datetime

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as login_user, logout as logout_user
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context, Template, RequestContext
from django.utils.http import urlquote 
from django.views.generic.simple import direct_to_template

from app.forms import *
from app.models import *
from app.messaging import send_increment_upvotes

def login(request):
    if request.method == 'POST': # If the form has been submitted...
        form = AuthenticationForm(data=request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
             login_user(request, form.get_user())
             return HttpResponseRedirect(reverse('home'))# Redirect after POST
    else:
        form = AuthenticationForm()
    return direct_to_template(request, 'login.html', {'form': form})

def logout(request):
    logout_user(request)
    return HttpResponseRedirect(reverse('home'))

def paginate(request, all_posts):
    paginator = Paginator(all_posts, 25)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        posts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        posts = paginator.page(paginator.num_pages)
    return posts

LIMIT = 5000
PPP = 25
MAX_PAGES = LIMIT/PPP

def paginate_(page, max):
    if page == 1:
        previous = None
    else:
        previous = page - 1
    if page == max:
        next = None
    else:
        next = page + 1 
    return previous, next

def get_page(request):
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    return page

def home(request):
    page = get_page(request)
    last_p = cache.get('top-ct')
    try:
        last_p = int(last_p)
    except:
        py, prev_p , next_p = None, None, None 
    else:
        if page > last_p:
            page = 1
        serialized = cache.get('top-%s' % page) 
        if not serialized: #XXX fail safe here?
            return HttpResponse('Something is wrong.')
        py = cPickle.loads(serialized)
        prev_p, next_p = paginate_(page, last_p)
    handle_form = None
    posts = Post.objects.filter(id__in=py) if py else None
    if request.user.is_authenticated():
        try:
            profile = request.user.get_profile()
        except:
            UserProfile.objects.create(user=request.user, handle=request.user.username)
            handle_form = HandleForm() 
    return direct_to_template(request, 'generic_posts.html', {
                'page':page, 'prev_p':prev_p, 
                'next_p':next_p, 'title':'Top',  
                'next':settings.LOGIN_REDIRECT_URL, 
                'handle_form':handle_form, 'posts':posts})

def latest(request):
    page = get_page(request)
    last_p = cache.get('latest-ct')
    if not last_p or page > last_p:
        serialized = 0 
    else:
        serialized = cache.get('latest-%s' % page)
    prev_p, next_p = paginate_(page, last_p)
    py = cPickle.loads(serialized) if serialized else None
    posts = Post.objects.filter(id__in=py) if py else None
    return direct_to_template(request, 'generic_posts.html',{
                'page':page, 'prev_p':prev_p, 'next_p':next_p, 
                'posts':posts,
                'title':'Latest'})

@login_required
def add_post2(request):
    def handle_sucess():
        profile = request.user.get_profile()
        profile.points += 1
        profile.save()
        request.user.message_set.create(message = 'Successfully posted.')
        return HttpResponseRedirect(reverse('single_post', args=(post.id,)))
    if request.method == "POST":
        post = Post(author=request.user)
        if request.POST.get("post_url"):
            form1 = AddLinkPostForm(request.POST, instance=post)
            if form1.is_valid():
                post = form1.save()
                handle_success()
        else:
            form2 = AddTextPostForm(request.POST, instance=post)
            if form2.is_valid():
                post = form2.save()
                handle_success()
    else:
        form1 = AddLinkPostForm()
        form2 = AddTextPostForm()
    return direct_to_template(request, 'add_post2.html', {'form1':form1, 'form2':form2, 'title':'Add Post'})

@login_required
def add_post(request):
    if request.method == "POST":
        post = Post(author=request.user)
        form = AddPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            profile = request.user.get_profile()
            profile.points += 1
            profile.save()
            request.user.message_set.create(message = 'Successfully posted.')
            return HttpResponseRedirect(reverse('single_post', args=(post.id,)))
    else:
        form = AddPostForm()
    return direct_to_template(request, 'add_post.html', {'form':form, 'title':'Add Post'})

def single_post(request, post_id):
    try:
        post=Post.objects.get(pk=post_id)
    except:
        raise Http404
    return direct_to_template(request, 'single_post.html', {'post':post, 'cat' : post.category, 'title':post.title })

def site_message(request):
    return direct_to_template(request, 'site_message.html', {})

def set_handle(request):
    if request.method == "POST":
        profile = UserProfile.objects.get(user=request.user)
        form = HandleForm(request.POST, instance = profile)
        if form.is_valid():
            user = request.user
            user.username = form.cleaned_data['handle']
            user.save()
            form.save()
        else:
            request.user.message_set.create(message = 'Invalid Handle!')
        return HttpResponseRedirect(reverse('home'))
    else:
        raise Http404

def top_contributers(request):
    profiles =  UserProfile.objects.all().order_by('-points')[0:10] 
    return direct_to_template(request, 'top_contributers.html', {'profiles':profiles, 'title':'Top Contributers'})

def view_profile(request, user_name):
    profile = UserProfile.objects.get(handle=user_name)
    return direct_to_template(request, 'view_profile.html', {'profile':profile, 'title':"%s's Profile" % profile.handle})

@login_required
def edit_profile(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except:
        raise Http404
    if request.method == "POST":
        form = ProfileForm(request.POST, instance = profile) 
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('home')
    else:
        form = ProfileForm(instance = profile)
    return direct_to_template(request, 'edit_profile.html', {'form':form, 'title':'Edit Profile'})

@login_required
def upvote(request):
    if request.method == "POST":
        try:
            post_id = request.POST.get('post_id')        
            #post = Post.objects.get(pk=int(post_id))
        except:
            raise Http404
        else:
            try:
                p = Post.objects.get(pk=post_id)
            except:
                raise Http404
            #curent user didnt vote on it already , doesnt have this post id in his profilesupvotes.
            profile = request.user.get_profile()
            if p.author.id != request.user.id and not profile.upvoted.filter(pk=post_id):
                p.upvotes += 1
                p.save()
                profile.upvoted.add(p)
                profile.save()
                auth_profile = p.author.get_profile()
                auth_profile.points += 1
                auth_profile.save()
                return HttpResponse()
            else:
                return HttpResponse('2')
    else:
        raise Http404

@login_required
def upvote_async(request):
    if request.method == "POST":
        try:
            post_id = request.POST.get('post_id')        
            #post = Post.objects.get(pk=int(post_id))
        except:
            raise Http404
        else:
            send_increment_upvotes(post_id)
            return HttpResponse()
    else:
        raise Http404

def category(request, cat_id):
    try:
        cat = Category.objects.get(pk=cat_id)
    except:
        raise Http404
    page = get_page(request)
    last_p = cache.get('cat-ct-%s' % cat.id)
    if not last_p or page > last_p:
        serialized = 0 
    else:
        serialized = cache.get('cat-%s-%s' % (cat.id, page))
    prev_p, next_p = paginate_(page, last_p)
    py = cPickle.loads(serialized) if serialized else None
    posts = Post.objects.filter(id__in=py) if py else None
    title = cat.name
    if cat.seo_name:
        title=cat.seo_name
    return direct_to_template(request, 'generic_posts.html', {'title': title, 'page':page,'prev_p':prev_p, 'next_p':next_p, 'posts':posts})

