from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, RedirectView, UpdateView, DeleteView

from tasks.forms import AddTaskForm, EditTaskForm
from tasks.models import Task
from tasks.utils import DataMixin


class TaskListView(DataMixin, ListView):
    model = Task
    context_object_name = 'new_tasks'
    template_name = 'tasks/task_list.html'
    title_page = "Задачи"

    def get_queryset(self):
        return Task.objects.filter(status=Task.Status.NEW)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks_inprogress'] = Task.objects.filter(status=Task.Status.IN_PROGRESS)
        context['tasks_completed'] = Task.objects.filter(status=Task.Status.COMPLETED)
        context['selected_item'] = "all"
        return context

class TaskListViewByStatus(DataMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list_by_status.html'
    title_page = "Задачи"

    def get_queryset(self):
        return Task.objects.filter(status=self.kwargs['status'])

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['selected_item'] = self.kwargs['status']
        return context

class AddTaskView(LoginRequiredMixin, DataMixin, CreateView):
    model = Task
    form_class = AddTaskForm
    template_name = 'tasks/add_task.html'
    title_page = "Добавить задачу"
    success_url = reverse_lazy('tasks:index')

    def form_valid(self, form):
        form.instance.status = Task.Status.NEW
        form.save()
        return super().form_valid(form)

class TaskDetailView(DataMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'tasks/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context

class MakeTaskInProgressView(LoginRequiredMixin,DataMixin, RedirectView):
    permanent = False
    query_string = False
    pattern_name = 'make_task_in_progress'
    def get_redirect_url(self, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        task.status = Task.Status.IN_PROGRESS
        task.user = self.request.user
        task.save()
        return reverse_lazy('tasks:index')

class MakeTaskCompletedView(LoginRequiredMixin, DataMixin, RedirectView):
    permanent = False
    query_string = False
    pattern_name = 'make_task_completed'
    def get_redirect_url(self, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs['pk'])
        task.status = Task.Status.COMPLETED
        task.save()
        return reverse_lazy('tasks:index')

class EditTaskView(LoginRequiredMixin,DataMixin, UpdateView):
    model = Task
    form_class = EditTaskForm
    title_page = "Редактировать задачу"
    template_name = 'tasks/edit_task.html'

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('tasks:task_detail', kwargs={'pk': self.object.pk})

class DeleteTaskView(LoginRequiredMixin, DataMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete_task.html'
    success_url = reverse_lazy('tasks:index')
    title_page = "Удалить задачу"