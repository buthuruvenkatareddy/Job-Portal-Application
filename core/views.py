from django.shortcuts import render, redirect, get_object_or_404
from .models import Job
from .forms import RegisterForm, JobApplyForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('job_list')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

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
        form = JobApplyForm(request.POST, request.FILES)
        if form.is_valid():
            app = form.save(commit=False)
            app.job = job
            app.applicant = request.user
            app.save()
            return redirect('job_list')
    else:
        form = JobApplyForm()
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
