from __future__ import unicode_literals
from django.http import HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.urls import reverse
from django.views import View

from .models import Mark, Task, TaskStatus
from .forms import TaskUpdateForm, TaskCreateForm


@require_http_methods(["GET"])
def get_todo_list(request):
    todo_list = Task.objects.all()
    return render_list_from_queryset(request, todo_list)


@require_http_methods(["GET"])
def get_progress_todo_list(request):
    todo_list = Task.objects.filter(status=TaskStatus.PROGRESS.name)
    return render_list_from_queryset(request, todo_list)


@require_http_methods(["GET"])
def get_completed_todo_list(request):
    todo_list = Task.objects.filter(status=TaskStatus.COMPLETED.name)
    return render_list_from_queryset(request, todo_list)


def render_list_from_queryset(request, todo_queryset):
    return render(request, "todo_list.html", {"todo_list": todo_queryset})


def complete_todo(request, todo_id: int):
    task = Task.objects.get(pk=todo_id)
    task.complete()
    task.save()
    return redirect(reverse('todo_list'))


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


def init_db(request):
    Mark.objects.all().delete()
    Task.objects.all().delete()

    mark_home = Mark.objects.create(name="Дом")
    mark_work = Mark.objects.create(name="Работа")
    mark_uni = Mark.objects.create(name="Вуз")
    mark_product = Mark.objects.create(name="Продукты")

    task_arch = Task.objects.create(title="Сделать лабораторную по проектированию",
                                    description="Сделать лабораторную работу №7 и показать во вторник",
                                    mark=mark_uni)
    Task.objects.create(title="Купить молоко",
                        description="Купить в пятерочке пискоревское молоко",
                        mark=mark_product)
    Task.objects.create(title="Здать курсовую работу по вебу",
                        description="Доделать проект django-todo, составить отчет и сдать",
                        mark=mark_uni)
    Task.objects.create(title="Получить зарплату",
                        description="Не забыть получить зарплату во вторник с:",
                        mark=mark_work)
    task_table = Task.objects.create(title="Починить стол",
                                     description="-",
                                     mark=mark_home)
    task_arch.complete().save()
    task_table.complete().save()
    return redirect(reverse('todo_list'))
