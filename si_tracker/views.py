from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from si_tracker.models import *

def general(req):
    return HttpResponse("Hello")

def items(req):
    args = dict()
    args['items'] = Issue.objects.all()
    return render_to_response('items/index.html', args)

def issue(req, item=None):
    args = dict()
    issue = Issue.objects.get(id=item)
    args['item'] = issue
    args['tasks'] = issue.related_tasks.all()
    return render_to_response('issue/index.html', args)

def task(req, item=None):
    args = dict()
    task = Task.objects.get(id=item)
    args['item'] = task
    args['issue'] = task.issue.all()[0]
    return render_to_response('task/index.html', args)


