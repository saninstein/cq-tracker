from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from si_tracker.models import *
from si_tracker.forms import *

def user_context(req):
    return {
        'user': req.user
    }

def general(req):
    return HttpResponse("Hello")

def items(req):
    args = dict()
    args['items'] = Issue.objects.all().order_by('-id')
    return render(req, 'items/index.html', args)

def issue(req, item=None):
    args = dict()
    issue = Issue.objects.get(id=item)
    args['item'] = issue
    args['tasks'] = issue.task_set.all()
    return render(req, 'issue/index.html', args)

def task(req, item=None):
    args = dict()
    task = Task.objects.get(id=item)
    args['item'] = task
    args['issue'] = task.issue
    return render(req, 'task/index.html', args)

def issue_create_update(req, item=''):
    args = dict()
    if item:
        issue = get_object_or_404(Issue, id=item)
        args['item'] = issue.id
    else:
        issue = None
        args['item'] = None

    if req.method == 'POST':
        form = IssueForm(req.POST, instance=issue)
        if form.is_valid():
            issue = form.save(commit=False)
            form.save()
            return redirect(issue.get_absolute_url())
        else:
            args['form'] = form

    else:
        args['form'] = IssueForm(instance=issue)

    return render(req, 'issue_update_create/index.html', args)




