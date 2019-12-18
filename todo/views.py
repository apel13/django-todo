from __future__ import unicode_literals
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.urls import reverse
from django.views import View

from .models import Mark, Task, TaskStatus
from .forms import TaskUpdateForm, TaskCreateForm

import datetime


@require_http_methods(["GET", "POST"])
def get_todo_list_t(request):
    tasks = Task.objects.all()
    categories = Task.objects.all()
    if request.method == "POST":
        if "taskAdd" in request.POST:
            title = request.POST["description"]
            date = str(request.POST["date"])
            category = request.POST["category_select"]
            content = title + " -- " + date + " " + category
            Todo = Task(title=title, content=content, due_date=date, category=Category.objects.get(name=category))
            Todo.save()
            return redirect("/")

        if "taskDelete" in request.POST:
            checkedlist = request.POST["checkedbox"]
            for todo_id in checkedlist:
                todo = Task.objects.get(id=int(todo_id))
                todo.delete()

    return render(request, "index.html", {"todos": todos, "categories": categories})


@require_http_methods(["GET"])
def get_todo_list(request):
    todo_list = Task.objects.all()
    return render(request, "todo_list.html", {"todo_list": todo_list})


class TodoCreateView(View):
    template_name = 'todo_create.html'

    def get(self, request):
        form = TaskCreateForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created = timezone.now()
            task.status = TaskStatus.PROGRESS.value
            task.save()
            return redirect(reverse('todo_list'))
        else:
            return HttpResponseServerError("Error form isn't valid: %s" % form.errors)


class TodoDetailView(View):
    http_method_names = ['get', 'post', 'put', 'delete']
    template_name = 'todo_detail.html'
    todo_id = None

    def dispatch(self, *args, **kwargs):
        method = self.request.POST.get('_method', '').lower()
        if method == 'put':
            return self.put(*args, **kwargs)
        if method == 'delete':
            return self.delete(*args, **kwargs)
        return super(TodoDetailView, self).dispatch(*args, **kwargs)

    def get(self, request, todo_id: int):
        todo = get_object_or_404(Task, pk=todo_id)
        form = TaskUpdateForm(initial=todo.to_dict())
        return render(request, self.template_name, {"todo": todo, "form": form})

    @staticmethod
    def put(request, todo_id: int):
        instance = get_object_or_404(Task, id=todo_id)
        form = TaskUpdateForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse('todo_list'))
        else:
            return HttpResponseServerError("Error form isn't valid: %s" % form.errors)

    @staticmethod
    def delete(request, todo_id: int):
        Task.objects.filter(pk=todo_id).delete()
        return redirect(reverse('todo_list'))
