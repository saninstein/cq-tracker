from django.shortcuts import render, render_to_response, get_object_or_404, redirect, reverse
from django.contrib.auth.forms import AuthenticationForm
from  django.contrib import auth
from django.http import HttpResponse, Http404, JsonResponse
from si_tracker.models import *
from si_tracker.forms import *
from operator import itemgetter

def user_context(req):
    return {
        'user': req.user
    }

def general(req):
    return render(req, 'items/index.html')

def items(req):
    issues = Issue.objects.all()
    issue_items = list(issues.values('id', 'title', 'date_raised', 'status', 'raised_by'))
    [x.update(type='Issue', url=reverse('tracker:item', args=['issue', x.get('id')])) for x in issue_items]

    tasks = Task.objects.all()
    task_items = list(tasks.values('id', 'type', 'title', 'date_raised', 'status', 'raised_by'))
    [x.update(url=reverse('tracker:item', args=['task', x.get('id')])) for x in task_items]

    items = sorted(task_items + issue_items, key=itemgetter('date_raised'), reverse=True)
    return JsonResponse({'results': items, 'user': req.user.id})

def get_issue(args, issue):
    args['tasks'] = issue.task_set.all()

def get_task(args, task):
    args['issue'] = task.issue

def item(req, type='', item=''):
    args = dict()
    if type.lower() == 'issue':
        template = 'issue/index.html'
        Item = Issue
        get_item = get_issue
    elif type.lower() == 'task' or type.lower() == 'idea':
        template = 'task/index.html'
        Item = Task
        get_item = get_task

    _item = get_object_or_404(Item, id=item)
    args['item'] = _item
    get_item(args, _item)
    return render(req, template, args)


def item_create_update(req, type='', item=''):
    args = dict()
    args['type'] = type
    if type == 'issue':
        Item = Issue
        Form = IssueForm
    elif type == 'task':
        Item = Task
        Form = TaskForm
    else:
        return Http404()

    if item:
        _item = get_object_or_404(Item, id=item)
        args['item'] = _item.id
    else:
        _item = None
        args['item'] = None

    if req.method == 'POST':
        form = Form(req.POST, instance=_item)
        if form.is_valid():
            _item = form.save(commit=False)
            form.save()
            return redirect(_item.get_absolute_url())
        else:
            args['form'] = form

    else:
        args['form'] = Form(instance=_item)

    return render(req, 'item_form/index.html', args)

def login(req):
    args = dict()
    if req.method == 'POST':
        form = AuthenticationForm(req, req.POST)
        if form.is_valid():
            auth.login(req, form.get_user())
            return redirect(reverse('tracker:general'))
        else:
            args['form'] = form

    else:
        args['form'] = AuthenticationForm()

    return render(req, 'login/index.html', args)

def logout(req):
    auth.logout(req)
    return redirect(reverse('tracker:general'))









