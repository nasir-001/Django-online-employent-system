from django.urls import path
from jobapp import views
from django.views.static import serve
from django.conf import settings
from django.conf.urls import url

app_name = "jobapp"


urlpatterns = [

    path('', views.home_view, name='home'),
    path('jobs/', views.job_list_View, name='job-list'),
    path('job/create/', views.create_job_View, name='create-job'),
    path('job/<int:id>/', views.single_job_view, name='single-job'),
    path('apply-job/<int:id>/', views.apply_job_view, name='apply-job'),
    path('bookmark-job/<int:id>/', views.job_bookmark_view, name='bookmark-job'),
    path('about/', views.single_job_view, name='about'),
    path('contact/', views.single_job_view, name='contact'),
    path('result/', views.search_result_view, name='search_result'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/employer/job/<int:id>/applicants/', views.all_applicants_view, name='applicants'),
    path('dashboard/employer/job/edit/<int:id>', views.job_edit_view, name='edit-job'),
    path('dashboard/employer/applicant/<int:id>/', views.applicant_details_view, name='applicant-details'),
    path('dashboard/employer/delete/<int:id>/', views.delete_job_view, name='delete'),
    path('dashboard/employee/delete-bookmark/<int:id>/', views.delete_bookmark_view, name='delete-bookmark'),
    url(r'^download/(?P<path>.*)$', serve, {'document_roo': settings.MEDIA_ROOT}),


]
