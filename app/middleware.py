from django.http import Http404, HttpResponse
import whitelist 

class WhiteList(object):
    def process_request(self, request):
        ip = request.META['REMOTE_ADDR']
        if ip not in whitelist.WHITE_LIST:
            return HttpResponse('sorry, we are working on the website now.') # raise Http404
        else:
            return None


