from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Job
from .forms import RegisterForm, ApplicationForm, LoginForm
 # Make sure LoginForm exists

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # or your desired page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})  # make sure template name matches



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('job_list')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def job_list(request):
    location = request.GET.get('location')
    title = request.GET.get('title')
    company = request.GET.get('company')
    jobs = Job.objects.all()
    if location:
        jobs = jobs.filter(location__icontains=location)
    if title:
        jobs = jobs.filter(title__icontains=title)
    if company:
        jobs = jobs.filter(company__icontains=company)
    return render(request, 'job_list.html', {'jobs': jobs})


@login_required
def job_detail(request, id):
    job = get_object_or_404(Job, id=id)
    return render(request, 'job_detail.html', {'job': job})


@login_required
def apply_job(request, id):
    job = get_object_or_404(Job, id=id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.applicant = request.user
            app.save()
            return redirect('job_list')
    else:
        form = ApplicationForm()
    return render(request, 'apply_job.html', {'form': form, 'job': job})


@login_required
def post_job(request):
    if not hasattr(request.user, 'profile') or request.user.profile.role != 'employer':
        return HttpResponse("Unauthorized", status=401)

    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('description')
        company = request.POST.get('company')
        salary = request.POST.get('salary')
        location = request.POST.get('location')
        Job.objects.create(
            title=title,
            description=desc,
            company=company,
            salary=salary,
            location=location,
            posted_by=request.user
        )
        return redirect('job_list')
    return render(request, 'post_job.html')
