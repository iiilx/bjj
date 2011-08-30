from app.models import Category
import memcache
import cPickle
import cjson
from urllib import urlencode
import settings, socialauth_settings
from poll.models import Poll

cache = memcache.Client(['127.0.0.1:11211'])

request_variables = {
    'client_id': socialauth_settings.FACEBOOK_APP_ID,
    'redirect_uri': 'http://bjjlinks.com/accounts/facebook_login/done/',
}

urlencoded_request_variables = urlencode(request_variables)
FB_REDIRECT_URL = "https://graph.facebook.com/oauth/authorize?%s" % urlencoded_request_variables

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
    all_polls = Poll.objects.all()
    return {'top_polls':all_polls}

def most_discussed_processor(request):
    posts = cache.get('%s-top3' % settings.PREFIX)
    posts = cPickle.loads(posts) if posts else None
    return {'most_discussed':posts}
 
def categories_old(request):
    if request.method == "GET":
        json = cache.get('%s-all-cats' % settings.PREFIX)
        cats = cjson.decode(json)
        return {'cats':cats}
    else:
        return {}
