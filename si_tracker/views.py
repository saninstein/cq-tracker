from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib import auth
from django.http import HttpResponse, Http404, JsonResponse
from django.db.models import Q
from si_tracker.models import *
from si_tracker.forms import *
from operator import itemgetter

def user_context(req):
    return {
        'user': req.user
    }

@user_passes_test(lambda user: user.is_authenticated, login_url=reverse_lazy('tracker:login'), redirect_field_name='')
def general(req):
    return render(req, 'items/index.html')

@user_passes_test(lambda user: user.is_authenticated, login_url=reverse_lazy('tracker:login'), redirect_field_name='')
def items(req):
    if req.user.is_staff:
        issues = Issue.objects.all()
        tasks = Task.objects.all()
    else:
        issues = Issue.objects.filter(Q(visible='Public') | Q(raised_by=req.user))
        tasks = Task.objects.filter(Q(visible='Public') | Q(raised_by=req.user))

    issue_items = list(issues.values('id', 'title', 'date_raised', 'status', 'raised_by'))
    [x.update(type='Issue', url=reverse('tracker:item', args=['issue', x.get('id')])) for x in issue_items]


    task_items = list(tasks.values('id', 'type', 'title', 'date_raised', 'status', 'raised_by'))
    [x.update(url=reverse('tracker:item', args=['task', x.get('id')])) for x in task_items]

    items = sorted(task_items + issue_items, key=itemgetter('date_raised'), reverse=True)
    return JsonResponse({'results': items, 'user': req.user.id})

def get_issue(args, issue):
    args['tasks'] = issue.task_set.all()

def get_task(args, task):
    args['issue'] = task.issue

@user_passes_test(lambda user: user.is_authenticated, login_url=reverse_lazy('tracker:login'), redirect_field_name='')
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

@user_passes_test(lambda user: user.is_authenticated, login_url=reverse_lazy('tracker:login'), redirect_field_name='')
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
        if _item.status.startswith('Closed') and not req.user.is_staff:
            return redirect(_item.get_absolute_url())
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
        inital = {'raised_by': req.user.id, 'assigned_to': req.user.id} if _item is None else None
        form = Form(instance=_item, initial=inital)

        if not req.user.is_staff:
            if req.user.id != _item.raised_by.id:
                print("Yes")
                form.fields['visible'].disabled = True
            if isinstance(form, TaskForm):
                form.fields['issue'].queryset = Issue.objects.filter(Q(visible='Public') | Q(raised_by=req.user.id))

        args['form'] = form

    return render(req, 'item_form/index.html', args)

@user_passes_test(lambda user: user.is_staff, login_url=reverse_lazy('tracker:general'), redirect_field_name='')
def delete_item(req, type='', item=''):
    if type == 'issue':
        Item = Issue
    elif type == 'task':
        Item = Task
    else:
        return Http404()
    _item = get_object_or_404(Item, id=item)
    _item.delete()
    return redirect(reverse('tracker:general'))

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

@user_passes_test(lambda user: user.is_staff, login_url=reverse_lazy('tracker:general'), redirect_field_name='')
def users(req):
    users = User.objects.all().reverse()
    return render(req, 'users/index.html', {'users': users})


@user_passes_test(lambda user: user.is_staff, login_url=reverse_lazy('tracker:general'), redirect_field_name='')
def create_user(req):
    args = dict()
    if req.method == 'POST':
        form = UserCreateForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('tracker:users'))
        else:
            args['form'] = form
    else:
        args['form'] = UserCreateForm()

    return render(req, 'user_form/index.html', args)














