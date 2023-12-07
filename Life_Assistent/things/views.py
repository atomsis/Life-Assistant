from django.core.mail import send_mail
from django.http import Http404
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import TodoList, Comment
from django.contrib.auth.decorators import login_required
from .forms import TodoListForm, TodoListSendForm, CommentForm
from datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, View
from django.views.generic.edit import UpdateView
from taggit.models import Tag

###---------------------Не актуально переделал в класс ---------------------------------
# @login_required
# def task_list(request):
#     user = request.user
#     events = TodoList.objects.filter(user=user)
#     paginator = Paginator(events,30)
#     page_number = request.GET.get('page',1)
#     try:
#         tasks = paginator.page(page_number)
#     except EmptyPage:
#         tasks = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         tasks = paginator.page(1)
#     return render(request, 'things/calendar.html', {'events': tasks})
###------------------------------------------------------------------------------------

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TodoListForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('calendar_view')
    else:
        form = TodoListForm()
    return render(request, 'things/add_event.html', {'form': form})


def tasks_share(request, date):
    tasks = get_object_or_404(TodoList,
                              date=date,
                              # status=TodoList.Status.PUBLISHED
                              )
    sent = False

    if request.method == 'POST':
        form = TodoListSendForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            task_url = request.build_absolute_uri(
                tasks.get_absolute_url())
            subject = f"{cd['name_author']} поделился(ась) своим Списком дел с тобой.'{tasks.description}"
            message = f"Перейди по ссылке {task_url} - там ПОЛНЫЙ список дел"
            send_mail(subject, message, 'your_account@gmail.com', [cd['to']])

            sent = True
    else:
        form = TodoListSendForm()
    return render(request, 'tasks/share_task.html',
                  {'tasks': tasks,
                   'form': form,
                   'sent': sent})


def task_detail(request, year, month, day):
    task = get_object_or_404(TodoList,
                             date__year=year,
                             date__month=month,
                             date__day=day,
                             # status=TodoList.Status.PUBLISHED
                             )
    task_split = task.tasks.split('\n')
    comments = task.comments.filter(active=True)
    form = CommentForm
    return render(request,
                  'tasks/detail.html',
                  {'task': task,
                   'task_split': task_split,
                   'comments': comments,
                   'form': form, })


class TaskListView(ListView):
    queryset = TodoList.objects.filter(status=TodoList.Status.PUBLISHED)
    context_object_name = 'tasks'
    paginate_by = 30
    template_name = 'things/calendar.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['drafts'] = TodoList.objects.filter(status=TodoList.Status.DRAFT)

        tag_slug = self.request.GET.get('tag')

        if tag_slug:
            tag = get_object_or_404(Tag,slug=tag_slug)
            context['tasks']= context['tasks'].filter(tags__in=[tag])
        return context


def edit_task(request, date):
    return render(request,
                  'tasks/edit_task.html',
                  {'date': date})


class TaskUpdateView(UpdateView):
    model = TodoList
    form_class = TodoListForm
    template_name = 'tasks/edit_task.html'
    success_url = reverse_lazy('todo:task_list')

    def get_object(self, queryset=None):
        date = self.kwargs.get('date')
        return get_object_or_404(TodoList, date=date)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date'] = self.kwargs.get('date')
        return context

    def form_valid(self, form):
        date = self.kwargs.get('date')
        existing_task = TodoList.objects.filter(date=date).exclude(pk=self.get_object().pk).first()

        if existing_task:
            existing_task.tasks = form.cleaned_data['tasks']
            existing_task.save()
            return redirect('todo:task_list')

        return super().form_valid(form)


@require_POST
def task_comment(request, date):
    task = get_object_or_404(TodoList,
                             date=date,
                             status=TodoList.Status.PUBLISHED)
    comment = None

    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.task = task
        comment.save()
    return render(request,
                  'tasks/comment.html',
                  {'task': task,
                   'form': form,
                   'comment': comment})
