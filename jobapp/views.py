from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from account.models import User
from jobapp.forms import *
from jobapp.models import *
from jobapp.permission import *
User = get_user_model()


def home_view(request):

    jobs = Job.objects.order_by('-timestamp')
    total_candidates = User.objects.filter(role='employee').count()
    total_companies = User.objects.filter(role='employer').count()

    paginator = Paginator(jobs, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {

        'total_candidates': total_candidates,
        'total_companies': total_companies,
        'total_jobs': len(jobs),
        'page_obj': page_obj
    }
    return render(request, 'jobapp/index.html', context)
 

def job_list_View(request):
    """

    """
    job_list = Job.objects.order_by('-timestamp')
    paginator = Paginator(job_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {

        'page_obj': page_obj,

    }
    return render(request, 'jobapp/job-list.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def create_job_View(request):
    """
    Provide the ability to create job post
    """
    form = JobForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    categories = Category.objects.all()

    if request.method == 'POST':

        if form.is_valid():

            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            # for save tags
            form.save_m2m()

            return redirect(reverse("jobapp:single-job", kwargs={
                                    'id': instance.id
                                    }))

    context = {
        'form': form,
        'categories': categories
    }
    return render(request, 'jobapp/post-job.html', context)


def single_job_view(request, id):
    """
    Provide the ability to view job details
    """

    job = get_object_or_404(Job, id=id)
    related_job_list = job.tags.similar_objects()

    paginator = Paginator(related_job_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'job': job,
        'page_obj': page_obj,
        'total': len(related_job_list)

    }
    return render(request, 'jobapp/job-single.html', context)


def search_result_view(request):
    """
        User can search job with multiple fields

    """

    job_list = Job.objects.order_by('-timestamp')

    # Keywords
    if 'job_title_or_company_name' in request.GET:
        job_title_or_company_name = request.GET['job_title_or_company_name']

        if job_title_or_company_name:
            job_list = job_list.filter(title__icontains=job_title_or_company_name) | job_list.filter(
                company_name__icontains=job_title_or_company_name)

    # location
    if 'location' in request.GET:
        location = request.GET['location']
        if location:
            job_list = job_list.filter(location__icontains=location)

    # Job Type
    if 'job_type' in request.GET:
        job_type = request.GET['job_type']
        if job_type:
            job_list = job_list.filter(job_type__iexact=job_type)

    paginator = Paginator(job_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {

        'page_obj': page_obj,

    }
    return render(request, 'jobapp/result.html', context)


@login_required(login_url=reverse_lazy('account:login'))
def apply_job_view(request, id):

    form = JobApplyForm(request.POST, request.FILES or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = Applicant.objects.filter(user=user, job=id)

    if not applicant:
        if request.method == 'POST':
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully applied for this job!')
                return redirect(reverse("jobapp:file"))

        else:
            return redirect(reverse("jobapp:single-job", kwargs={
                'id': id
            }))

    else:

        messages.error(request, 'You already applied for the Job!')

        return redirect(reverse("jobapp:single-job", kwargs={
            'id': id
        }))


@login_required(login_url=reverse_lazy('account:login'))
# @user_is_employer
# @user_is_employee
def dashboard_view(request):
    """


    """
    jobs = []
    savedjobs = []
    total_applicants = {}
    if request.user.role == 'employer':

        jobs = Job.objects.filter(user=request.user.id)
        for job in jobs:
            count = Applicant.objects.filter(job=job.id).count()
            total_applicants[job.id] = count

    if request.user.role == 'employee':
        savedjobs = BookmarkJob.objects.filter(user=request.user.id)
    context = {

        'jobs': jobs,
        'savedjobs': savedjobs,
        'total_applicants': total_applicants
    }

    print(context)
    return render(request, 'jobapp/dashboard.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def delete_job_view(request, id):

    job = get_object_or_404(Job, id=id, user=request.user.id)

    if job:

        job.delete()
        messages.success(request, 'Your Job Post was successfully deleted!')

    return redirect('jobapp:dashboard')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def all_applicants_view(request, id):

    all_applicants = Applicant.objects.filter(job=id)

    context = {

        'all_applicants': all_applicants
    }

    return render(request, 'jobapp/all-applicants.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def delete_bookmark_view(request, id):

    job = get_object_or_404(BookmarkJob, id=id, user=request.user.id)

    if job:

        job.delete()
        messages.success(request, 'Saved Job was successfully deleted!')

    return redirect('jobapp:dashboard')


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employer
def applicant_details_view(request, id):

    applicant = get_object_or_404(User, id=id)

    context = {

        'applicant': applicant
    }

    return render(request, 'jobapp/applicant-details.html', context)


@login_required(login_url=reverse_lazy('account:login'))
@user_is_employee
def job_bookmark_view(request, id):

    form = JobBookmarkForm(request.POST or None)

    user = get_object_or_404(User, id=request.user.id)
    applicant = BookmarkJob.objects.filter(user=request.user.id, job=id)

    if not applicant:
        if request.method == 'POST':

            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = user
                instance.save()

                messages.success(
                    request, 'You have successfully save this job!')
                return redirect(reverse("jobapp:single-job", kwargs={
                    'id': id
                }))

        else:
            return redirect(reverse("jobapp:single-job", kwargs={
                'id': id
            }))

    else:
        messages.error(request, 'You already saved this Job!')

        return redirect(reverse("jobapp:single-job", kwargs={
            'id': id
        }))


@login_required(login_url=reverse_lazy('accounts:login'))
@user_is_employer
def job_edit_view(request, id=id):
    """
    Handle Employee Profile Update

    """

    job = get_object_or_404(Job, id=id)
    categories = Category.objects.all()
    form = JobEditForm(request.POST or None, instance=job)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        # for save tags
        # form.save_m2m()
        messages.success(request, 'Your Job Post Was Successfully Updated!')
        return redirect(reverse("jobapp:single-job", kwargs={
            'id': instance.id
        }))
    context = {

        'form': form,
        'categories': categories
    }

    return render(request, 'jobapp/job-edit.html', context)
