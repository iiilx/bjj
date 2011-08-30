from django.http import Http404, HttpResponse
import local_settings

class WhiteList(object):
    def process_request(self, request):
        ip = request.META['REMOTE_ADDR']
        if ip not in local_settings.WHITE_LIST:
            return HttpResponse('sorry, we are working on the website now.') # raise Http404
        else:
            return None


