from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from .models import Task
from .forms import TaskForm
from django.http import JsonResponse
from django.core.cache import cache

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard_view(request):
    total_tasks = Task.objects.count()  # Count all tasks
    completed_tasks = Task.objects.filter(status="completed").count()  # Count completed tasks
    pending_tasks = Task.objects.filter(status="pending").count()  # Count pending tasks

    

    context = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        
    }

    return render(request, "dashboard.html", context)  # Ensure this template is correct

@login_required
def update_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == "POST":
        new_status = request.POST.get("status")
        task.status = new_status
        task.save()  # This will automatically archive it if completed
    
    return redirect('task_list')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user, is_archived=False).order_by('-id')
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Redirect back to the list after saving
        
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'create_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    if task.status == "completed":
        return redirect('archive')
    else:
        return redirect('task_list')


@login_required
def update_status(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == "POST":
        new_status = request.POST.get("status")
        task.status = new_status
        task.save()
    
    return redirect('task_list')

@login_required
def archive_view(request):
    archived_tasks = Task.objects.filter(user=request.user, is_archived=True).order_by('-due_date')
    return render(request, 'archive.html', {'archived_tasks': archived_tasks})

@login_required
def archive_page(request):
    archived_tasks = Task.objects.filter(is_archived=True)  # Show completed tasks
    return render(request, 'archive_page.html', {'tasks': archived_tasks})

@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    
    return render(request, 'create_task.html', {'form': form})

@login_required
def calendar_view(request):
    return render(request, 'calendar.html')

@login_required
def task_api(request):
    tasks = Task.objects.filter(user=request.user)
    task_list = []
    
    for task in tasks:
        task_list.append({
            "title": task.title,
            "start": task.due_date.strftime("%Y-%m-%d"),  
            "status": task.status,
            "description": task.description,
            "color": "#28a745" if task.status == "completed" else "#dc3545"
        })

    return JsonResponse(task_list, safe=False)

@login_required
def get_quote(request):
    # Check if a quote is cached to reduce API calls
    cached_quote = cache.get("daily_quote")
    
    if cached_quote:
        return JsonResponse(cached_quote, safe=False)

    # Fetch a new quote if not cached
    try:
        response = requests.get("https://zenquotes.io/api/today")
        if response.status_code == 200:
            data = response.json()

            # Check if response contains a valid quote
            if isinstance(data, list) and "q" in data[0]:
                quote = {"quote": data[0]["q"], "author": data[0]["a"]}

                # Cache the quote for 24 hours
                cache.set("daily_quote", quote, timeout=86400)  # 1 day
                return JsonResponse(quote, safe=False)

        return JsonResponse({"error": "Invalid API response"}, status=500)

    except requests.RequestException as e:
        print(f"Error fetching quote: {e}")
        return JsonResponse({"error": "Failed to fetch quote"}, status=500)

@login_required   
def settings_view(request):
    return render(request, 'settings.html')

