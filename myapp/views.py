from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import NameForm, TaskForm
from .models import Task

def home(request):
    name = "Pranavi"
    course = "Django"

    return render(request, 'home.html', {
        'name': name,
        'course': course
    })


def about(request):
    return render(request, 'about.html')


def home_view(request):
    if request.method == "POST":
        form = NameForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect("/thanks/")
    else:
        form = NameForm()

    return render(request, "name.html", {"form": form})

def thanks(request):
    return HttpResponse("Thank you! Your form has been submitted successfully.")

def task_list(request):
    tasks = Task.objects.all().order_by('-created_at')

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = tasks.filter(completed=False).count()

    if total_tasks > 0:
        completion_percentage = int((completed_tasks / total_tasks) * 100)
    else:
        completion_percentage = 0

    return render(request, 'task_list.html', {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'completion_percentage': completion_percentage
    })

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()

    return render(request, 'task_form.html', {
        'form': form
    })


def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    task.completed = not task.completed
    task.save()

    return redirect('task_list')


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    task.delete()

    return redirect('task_list')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'task_form.html', {
        'form': form,
        'edit_mode': True
    })