import pusher
from random import choice

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse

from bjj.poll.models import *
from bjj.poll.forms import ChoiceFormSet, PollForm 

pusher.app_id = '7655'
pusher.key = 'e95995471c244ab894c4'
pusher.secret = '598a0cea53c3cb66eb64'

p = pusher.Pusher()

def poll_index(request):
    polls = Poll.objects.all()
    return direct_to_template(request, 'poll/index.html', {'polls':polls, 'title':'Polls'})
    
@login_required
def add_poll(request):
    if request.method == "POST":
        poll_form = PollForm(request.POST)
        choice_formset = ChoiceFormSet(request.POST, prefix='choice')
        if poll_form.is_valid() and choice_formset.is_valid():
            poll = poll_form.save()
            for form in choice_formset:
                choice = form.save(commit=False)
                choice.poll = poll
                choice.save()
            request.user.message_set.create(message = 'Successfully created poll.')
            return HttpResponseRedirect(reverse('poll_index'))
    else:
        poll_form = PollForm()
        choice_formset = ChoiceFormSet(prefix='choice')
    return direct_to_template(request, 'poll/add_poll.html', {'poll_form':poll_form, 'choice_formset':choice_formset})

def get_random(request):
    count = Poll.objects.all().count()
    pk = choice(range(1,count+1))
    poll = Poll.objects.get(pk=pk)
    choices = poll.choice_set.all()
    return direct_to_template(request, 'poll/output.html', {'poll':poll, 'choices':choices})

def get_poll_widget(request, pk):
    poll = Poll.objects.get(pk=pk)
    choices = poll.choice_set.all()
    return direct_to_template(request, 'poll/output.html', {'poll':poll, 'choices':choices})

def get_poll_single(request, pk):
    poll = Poll.objects.get(pk=pk)
    choices = poll.choice_set.all()
    return direct_to_template(request, 'poll/single_poll.html', {'poll':poll, 'choices':choices, 'title':'Poll: %s' % poll.question})

@csrf_exempt
def upvote_choice(request, pk):
    if request.method == "POST":
        choice = Choice.objects.get(pk=pk)
        ip = request.META['REMOTE_ADDR']  
        votes = Vote.objects.filter(ip=ip, poll=choice.poll)  
        if votes:
            return HttpResponse('2') # 2 means already voted
        v = Vote.objects.create(ip=ip, poll=choice.poll)
        choice.votes += 1
        choice.save()
        p[pk].trigger('upvote', {})
        return HttpResponse()
    raise Http404              
