from django.urls import path, include
from . import views
from .views import upload_photo, display_photos, delete_photo
from django.urls import path
from .views import  upload_avatar
from .views import delete_avatar

urlpatterns = [
    path('', views.home_man, name='home_man'),
    path('upload/', upload_photo, name='upload_photo'),
    path('photos/', display_photos, name='display_photos'),
    path('delete/<int:photo_id>/', delete_photo, name='delete_photo'),
    path('task_list/', views.task_list, name='task_list'),  # URL для отображения списка задач
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),  # Удаление задачи
    path('photo_list', views.photo_list, name='photo_list'),
    path('photo/<int:photo_id>/add_task/', views.add_task, name='add_task'),
    path('photo/<int:photo_id>/completed_tasks/', views.completed_tasks, name='completed_tasks'),
    path('profile_manager', views.profile_manager, name='profile_manager'),
    path('confirm_task/<int:task_id>/', views.confirm_task, name='confirm_task'),
    path('task/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('upload-avatar/', upload_avatar, name='upload_avatar'),
    path('delete_avatar/', delete_avatar, name='delete_avatar'),# URL для удаления аватарки
    path('start_timer_manager/', views.start_timer_manager, name='start_timer_manager'),
    path('stop_timer_manager/', views.stop_timer_manager, name='stop_timer_manager'),
    path('history/', views.history, name='history'),
    path('photo/<int:photo_id>/rated_tasks/', views.rated_tasks, name='rated_tasks'),
    path('photo/<int:photo_id>/task_completed/', views.task_completed, name='task_completed'),
    path('employee/',views.employee, name='employee'),
    path('refactor_profile_manager/', views.refactor_profile_manager, name='refactor_profile_manager'),
    path('toggle_timer_manager/', views.toggle_timer_manager, name='toggle_timer_manager'),
    path('profile_employee_manager/<int:user_id>/', views.profile_employee_manager, name='profile_employee_manager'),
    path('edit_user_manager/<int:user_id>/', views.edit_user_manager, name='edit_user_manager'),
    path('manager_user_statistic/<int:user_id>/', views.manager_user_statistic, name='manager_user_statistic'),
    path('my_statistic/', views.my_statistic, name='my_statistic'),
    path('manager_maket/<int:photo_id>/', views.manager_maket, name='manager_maket'),
    path('photo_detail/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('my_maket_manager', views.my_maket_manager, name='my_maket_manager'),
    path('maket_info_manager/<int:photo_id>/', views.maket_info_manager, name='maket_info_manager'),
    path('employee_shifts/<int:user_id>/', views.employee_shifts, name='employee_shifts'),
    path('templates/', views.manager_task_templates_list, name='manager_task_templates_list'),
    path('templates/create/', views.create_manager_task_template, name='create_manager_task_template'),
    path('templates/<int:template_id>/edit/', views.edit_manager_task_template, name='edit_manager_task_template'),
    path('templates/<int:template_id>/delete/', views.delete_manager_task_template, name='delete_manager_task_template'),
    path('get_template_data/<int:template_id>/', views.get_template_data, name='get_template_data'),
]
