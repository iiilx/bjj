from django.core.cache import cache

from app.models import Category
import cPickle
from urllib import urlencode
import settings 
from poll.models import Poll

request_variables = {
    'client_id': settings.FACEBOOK_APP_ID,
    'redirect_uri': 'http://%s/accounts/facebook_login/done/' % settings.DOMAIN,
}

urlencoded_request_variables = urlencode(request_variables)
FB_REDIRECT_URL = "https://graph.facebook.com/oauth/authorize?%s" % urlencoded_request_variables

def domain(request):
    return {'DOMAIN' : settings.DOMAIN}

def fbook_url(request):
    if request.method == "GET":
        return {'FB_LOGIN_URL' : FB_REDIRECT_URL} 
    else:
        return {}   

def categories(request):
    if request.method == "GET":
        cats = Category.objects.all().order_by('name') 
        return {'cats':cats}
    else:
        return {}

def top_polls_processor(request):
    s = cache.get('top_polls')
    py = cPickle.loads(s) if s else None
    polls = Poll.objects.filter(id__in=py)
    return {'top_polls':polls}

def most_discussed_processor(request):
    posts = cache.get('top3')
    posts = cPickle.loads(posts) if posts else None
    return {'most_discussed':posts}
 
