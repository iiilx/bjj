from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from registration.views import register
admin.autodiscover()

from bjj.app.models import profile_callback
from bjj.app.forms import RegForm

urlpatterns = patterns('',
    # Examples:
    url(r'^accounts/', include('socialauth.urls')),
    url(r'^accts/', include('registration.urls')),
    url(r'^accts/register/$', register, {'form_class':RegForm, 'profile_callback':profile_callback}, name='registration_register'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^sentry/', include('sentry.web.urls')),
)


urlpatterns += patterns('bjj.app.views',
    url(r'^$', 'home', name = 'home'),
    url(r'^home2$', 'home2', name = 'home2'),
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

