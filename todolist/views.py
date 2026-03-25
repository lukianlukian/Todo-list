from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic, View

from .models import Task, Tag


# Task views --------------------------------------------------------
class TaskListView(generic.ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "todolist/index.html"
    paginate_by = 10

    def get_queryset(self):
        return Task.objects.prefetch_related("tags").order_by("done_or_no", "-date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_tasks"] = Task.objects.count()
        return context


class TaskCreateView(generic.CreateView):
    model = Task
    fields = ["content", "deadline", "done_or_no", "tags"]
    success_url = reverse_lazy("todolist:index")


class TaskUpdateView(generic.UpdateView):
    model = Task
    fields = ["content", "deadline", "done_or_no", "tags"]
    success_url = reverse_lazy("todolist:index")


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("todolist:index")


class ToggleTaskStatusView(View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.done_or_no = not task.done_or_no
        task.save()
        return redirect("todolist:index")


# Tag views --------------------------------------------------------
class TagListView(generic.ListView):
    model = Tag
    context_object_name = "tags"
    template_name = "todolist/tags.html"


class TagCreateView(generic.CreateView):
    model = Tag
    fields = ["name"]
    success_url = reverse_lazy("todolist:tags")


class TagUpdateView(generic.UpdateView):
    model = Tag
    fields = ["name"]
    success_url = reverse_lazy("todolist:tags")


class TagDeleteView(generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("todolist:tags")