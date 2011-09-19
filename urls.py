from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings

from sitemap import SitemapForum, SitemapTopic
from forms import RegistrationFormUtfUsername
from djangobb_forum import settings as forum_settings

# HACK for add default_params with RegistrationFormUtfUsername and backend to registration urlpattern
# Must be changed after django-authopenid #50 (signup-page-does-not-work-whih-django-registration)
# will be fixed
from django_authopenid.urls import urlpatterns as authopenid_urlpatterns

for i, rurl in enumerate(authopenid_urlpatterns):
    if rurl.name == 'registration_register':
        authopenid_urlpatterns[i].default_args.update({'form_class': RegistrationFormUtfUsername})

from registration.views import register
admin.autodiscover()

from app.models import profile_callback
from app.forms import RegForm

urlpatterns = patterns('',
    url(r'^account/', include(authopenid_urlpatterns)),
    url(r'^forum', include('djangobb_forum.urls', namespace='djangobb')),
    url(r'^accounts/', include('socialauth.urls')),
    url(r'^accts/', include('registration.urls')),
    url(r'^accts/register/$', register, {'form_class':RegForm, 'profile_callback':profile_callback}, name='registration_register'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^search/', include('haystack.urls')),
    #url(r'^sentry/', include('sentry.web.urls')),
)


urlpatterns += patterns('bjj.app.views',
    url(r'^$', 'home', name = 'home'),
    url(r'^add-post2$', 'add_post2', name='add_post2'),
    url(r'^add-post$', 'add_post', name='add_post'),
    url(r'^category/(?P<cat_id>\d+)/', 'category', name='category'),
    url(r'^edit-profile$', 'edit_profile', name='edit_profile'),
    url(r'^latest$', 'latest', name='latest'),
    url(r'^login$', 'login', name='login'),
    url(r'^logout$', 'logout', name='logout'),
    url(r'^post/(?P<post_id>\d+)/', 'single_post', name='single_post'),
    url(r'^post/upvote$', 'upvote', name = 'upvote'),
    url(r'^profile/(?P<user_name>.+)$', 'view_profile', name='view_profile'),
    url(r'^set-handle$', 'set_handle', name='set_handle'),
    url(r'^site-message$', 'site_message', name='site_message'),
    url(r'^top-contributers$', 'top_contributers', name='top_contributers'),
)

urlpatterns += patterns('bjj.poll.views',
    url(r'^poll/random/$', 'get_random', name='get_random'),
    url(r'^poll/(?P<pk>\d+)/widget$', 'get_poll_widget', name='get_poll_widget'),
    url(r'^poll/(?P<pk>\d+)/', 'get_poll_single', name='get_poll_single'),
    url(r'^poll/choice/(?P<pk>\d+)/upvote$', 'upvote_choice', name='upvote_choice'),
    url(r'^poll/$', 'poll_index', name='poll_index'),
    url(r'^poll/add$', 'add_poll', name='add_poll'),
)
# PM Extension
if (forum_settings.PM_SUPPORT):
    urlpatterns += patterns('',
        (r'^pm/', include('messages.urls')),
   )

if (settings.DEBUG):
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'),
            'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

