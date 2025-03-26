from django.urls import path
from . import views


urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('task-list/', views.task_list, name='task_list'),
    path('create-task/', views.create_task, name='create_task'),
    path("edit-task/<int:task_id>/", views.edit_task, name="edit_task"),
    path("delete-task/<int:task_id>/", views.delete_task, name="delete_task"),
    path('update-status/<int:task_id>/', views.update_status, name='update_status'),
    path('archive/', views.archive_view, name='archive'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('api/tasks/', views.task_api, name='task_api'),
    path('api/quote/', views.get_quote, name='get_quote'),   # API for tasks
    path('settings/', views.settings_view, name='settings'),
]





