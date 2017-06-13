from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, Http404
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
    args = dict()
    # items = list(Issue.objects.values('title', 'date_raised', 'id'))
    # [x.update(type='Issue') for x in items]
    # items += list(Task.objects.values('title', 'date_raised', 'id', 'type'))
    # items = sorted(items, key=itemgetter('date_raised'))
    # args['items'] = items
    # print(args['items'])
    return render(req, 'items/index.html', args)

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




