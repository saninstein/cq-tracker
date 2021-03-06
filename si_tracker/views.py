from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib import auth
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from si_tracker.models import *
from si_tracker.forms import *
from operator import itemgetter
from datetime import datetime
from si_tracker.utils import message_create, message_about_task


def log(item, action, type=None):
    if type == 'task':
        log = LogTask()
    else:
        log = LogIssue()
    log.what = action
    log.save()





def user_context(req):
    return {
        'user': req.user
    }

def bootstraped_form(form):
    for key in form.fields:
        if key == 'is_staff' or key == 'allow_mail_send':
            continue
        if key == 'issue':
            form.fields[key].widget.attrs['class'] = 'form-control selectpicker'
            continue
        form.fields[key].widget.attrs['class'] = 'form-control'

    if 'location' in form.fields:
        form.fields['location'].widget.attrs['class'] += " selectpicker"
        form.fields['location'].widget.attrs['data-live-search'] = "true"
    if 'raised_by' in form.fields:
        form.fields['raised_by'].widget.attrs['class'] += " selectpicker"
        form.fields['raised_by'].widget.attrs['data-live-search'] = "true"
    if 'assigned_to' in form.fields:
        form.fields['assigned_to'].widget.attrs['class'] += " selectpicker"
        form.fields['assigned_to'].widget.attrs['data-live-search'] = "true"

@user_passes_test(lambda user: user.is_authenticated, login_url=reverse_lazy('tracker:login'), redirect_field_name='')
def general(req):
    return render(req, 'items/index.html')

@user_passes_test(lambda user: user.is_authenticated, login_url=reverse_lazy('tracker:login'), redirect_field_name='')
def items(req):
    vals_tasks = ('id', 'type', 'title', 'date_raised', 'status', 'raised_by', 'date_due', 'assigned_to', 'location__name')
    vals_issues = ('id', 'title', 'date_raised', 'status', 'raised_by', 'date_due', 'assigned_to', 'location__name')
    if req.user.is_staff:
        issues = Issue.objects.all()
        tasks = Task.objects.all()
        _tasks = [list(x.task_set.all().values('id')) for x in issues]
        _issues = [list(x.issue.all().values('id')) for x in tasks]

    else:
        tasks = Task.objects.filter(Q(visible='Public') | Q(raised_by=req.user))
        issues = Issue.objects.filter(Q(visible='Public') | Q(raised_by=req.user))
        _tasks = [list(x.task_set.filter(Q(visible='Public') | Q(raised_by=req.user)).values('id')) for x in issues]
        _issues = [list(x.issue.filter(Q(visible='Public') | Q(raised_by=req.user)).values('id')) for x in tasks]


    _tasks = [list(x['id'] for x in task) for task in _tasks]
    _issues = [list(x['id'] for x in issue) for issue in _issues]



    issue_items = list(issues.values(*vals_issues))
    [
        x.update(type='Issue', url=reverse('tracker:item', args=['critical-question', x.get('id')]), tasks=y)
        for x, y in zip(issue_items, _tasks)
    ]


    task_items = list(tasks.values(*vals_tasks))
    [
        x.update(url=reverse('tracker:item', args=['task', x.get('id')]), issues=y)
        for x, y in zip(task_items, _issues)
    ]

    items = sorted(issue_items + task_items, key=itemgetter('date_raised'), reverse=True)

    update_user_info(items)
    statuses = {
        'open': [x[0] for x in Item.open_statuses],
        'close': [x[0] for x in Item.closed_statuses]
    }


    current_month = datetime.today().month
    return JsonResponse({
        'items': items,
        'user': req.user.id,
        'statuses': statuses,
        'open_items': sum(Item.objects.filter(date_raised__month=current_month, status__in=statuses['open']).count() for Item in [Issue, Task]),
        'close_items': sum(Item.objects.filter(date_raised__month=current_month, status__in=statuses['close']).count() for Item in [Issue, Task])
    })

def update_user_info(items):
    for item in items:
        assigned_user = get_user(item.get('assigned_to', None))
        raised_user = get_user(item.get('raised_by', None))
        assigned_user = assigned_user.username if assigned_user else None
        raised_user = raised_user.username if raised_user else None
        item.update(assigned_user=assigned_user, raised_user=raised_user)

def get_user(id):
    try:
        return User.objects.get(id=id)
    except User.DoesNotExist:
        return False


def get_issue(args, issue):
    args['tasks'] = issue.task_set.all()

def get_task(args, task):
    args['issues'] = task.issue.all()


@user_passes_test(lambda user: user.is_authenticated, login_url=reverse_lazy('tracker:login'), redirect_field_name='')
def item(req, type='', item=''):
    args = dict()
    if type.lower() == 'critical-question':
        template = 'issue/index.html'
        Item = Issue
        get_item = get_issue
    elif type.lower() == 'task' or type.lower() == 'idea':
        template = 'task/index.html'
        Item = Task
        get_item = get_task

    _item = get_object_or_404(Item, id=item)

    if _item.visible == 'Private':
        if req.user.is_staff or req.user.id == _item.raised_by.id:
            args['item'] = _item
            get_item(args, _item)
            return render(req, template, args)
    else:
        args['item'] = _item
        get_item(args, _item)
        return render(req, template, args)
    return redirect(reverse('tracker:general'))

@user_passes_test(lambda user: user.is_authenticated, login_url=reverse_lazy('tracker:login'), redirect_field_name='')
def item_create_update(req, type='', item=''):
    args = dict()
    args['type'] = type
    if type == 'critical-question':
        Item = Issue
        Form = IssueForm
    elif type == 'task':
        Item = Task
        Form = TaskForm
    else:
        return redirect(reverse('tracker:general'))

    if item:
        _item = get_object_or_404(Item, id=item)
        if _item.status in [s[0] for s in Item.closed_statuses ] and not req.user.is_staff:
            return redirect(_item.get_absolute_url())
        args['item'] = _item.id
    else:
        _item = None
        args['item'] = None

    if req.method == 'POST':
        inst = _item
        form = Form(req.POST, instance=_item)
        if form.is_valid():
            item = form.save(user=req.user, item=inst, commit=False)
            form.save()
            if _item is None:
                message_create("Item created", item, item.location.owner)
                if item.type != Issue.type:
                    message_about_task("Associated tasks create", item)
            return redirect(item.get_absolute_url())
        else:
            args['form'] = form

    else:
        inital = {'raised_by': req.user.id, 'assigned_to': req.user.id} if _item is None else None
        form = Form(instance=_item, initial=inital)

        if not req.user.is_staff:
            if _item is not None:
                if req.user.id != _item.raised_by.id:
                    form.fields['visible'].disabled = True
            if isinstance(form, TaskForm):
                form.fields['issue'].queryset = Issue.objects.filter(Q(visible='Public') | Q(raised_by=req.user.id))

        args['form'] = form
    bootstraped_form(args.get('form'))
    return render(req, 'item_form/index.html', args)

@user_passes_test(lambda user: user.is_staff, login_url=reverse_lazy('tracker:general'), redirect_field_name='')
def delete_item(req, type='', item=''):
    if type == 'critical-question':
        Item = Issue
    elif type == 'task':
        Item = Task
    else:
        return redirect(reverse('tracker:general'))
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
        form = AuthenticationForm()
        args['form'] = form
    bootstraped_form(form)
    return render(req, 'login/index.html', args)

@user_passes_test(lambda user: user.is_authenticated, login_url=reverse_lazy('tracker:login'), redirect_field_name='')
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
        form = UserCreateForm()
        args['form'] = form
    args['type'] = 'create'
    bootstraped_form(form)
    return render(req, 'user_form/index.html', args)

@user_passes_test(lambda user: user.is_staff, login_url=reverse_lazy('tracker:general'), redirect_field_name='')
def update_user(req, user=''):
    args = dict()
    if user:
        _user = get_object_or_404(User, id=user)
        if req.method == 'POST':
            form = UpdateUserForm(req.POST, instance=_user)
            if form.is_valid():
                form.save()
                return redirect(reverse('tracker:users'))
            else:
                args['form'] = form
        else:
            form = UpdateUserForm(instance=_user)
            args['form'] = form

        bootstraped_form(form)
        args['type'] = 'update'
        args['user_id'] = user
        return render(req, 'user_form/index.html', args)
    return redirect(reverse('tracker:users'))

def change_password(req, user=''):
    args = dict()
    if user:
        _user = get_object_or_404(User, id=user)
        if req.user.is_staff or req.user.id == _user.id:
            if req.method == 'POST':
                form = SetPasswordForm(_user, req.POST)
                if form.is_valid():
                    form.save()
                    return redirect(reverse('tracker:general'))
                else:
                    args['form'] = form
            else:
                form = SetPasswordForm(_user)
                args['form'] = form
            args['user_id'] = user
            bootstraped_form(form)
            return render(req, 'change_password/index.html', args)
    return redirect(reverse('tracker:general'))



















