from datetime import datetime, timedelta

from users.models import CustomUser, PrizeHistory
from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserForm, TaskTemplateForm, TaskForm
from users.views import CustomUser
from django.contrib import messages
from users.models import PromotionRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from manager2.models import Task, Photo
from .models import TaskTemplate  # Добавляем импорт TaskTemplate
import os
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from manager2.models import Photo, PhotoFile
from .forms import UploadFileForm

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from manager2.models import Photo
from .forms import PhotoDescriptionForm
from django.db.models import Q
from .forms import AddDescriptionForm

from django.shortcuts import render, get_object_or_404, redirect
from .forms import PhotoForm  # Создайте форму для редактирования

from django.http import JsonResponse

def edit_maket(request, id):
    photo = get_object_or_404(Photo, id=id)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            return redirect('task_list_director')  # Перенаправление после успешного редактирования
    else:
        form = PhotoForm(instance=photo)

    return render(request, 'director/edit_maket.html', {'form': form, 'photo': photo})


def maket_info_director(request, photo_id):
    # Получаем объект макета по его ID
    photo = get_object_or_404(Photo, id=photo_id)

    context = {
        'photo': photo,
    }
    return render(request, 'director/maket_info_director.html', context)


def add_description(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)  # Найти макет по ID

    if request.method == 'POST':
        form = AddDescriptionForm(request.POST)
        if form.is_valid():
            photo.description = form.cleaned_data['description']  # Обновить описание
            photo.save()
            return redirect('task_list_director')  # Перенаправьте на страницу макета или другой URL

    else:
        form = AddDescriptionForm()

    return render(request, 'director/add_description.html', {'form': form, 'photo': photo})


def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    if request.method == 'POST':
        form = PhotoDescriptionForm(request.POST, instance=photo)
        if form.is_valid():
            form.save()
            return redirect('task_list_director')  # Или обратно на ту же страницу
    else:
        form = PhotoDescriptionForm(instance=photo)

    return render(request, 'director/photo_detail.html', {'photo': photo, 'form': form})



def maket_director(request, photo_id):
    # Получаем объект макета по его ID
    photo = get_object_or_404(Photo, id=photo_id)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "complete":
            # Проверяем, завершены ли все задачи, связанные с этим макетом
            tasks = Task.objects.filter(photo=photo)
            if not all(task.completed for task in tasks):
                # Если не все задачи завершены, показываем сообщение об ошибке
                messages.error(
                    request,
                    f"Невозможно завершить макет. Сначала завершите все задачи для макета {photo.image_name}."
                )
                return redirect("maket_director", photo_id=photo_id)

            # Если все задачи завершены, можно завершить макет
            if not photo.is_completed:
                photo.is_completed = True
                photo.save()
                messages.success(request, f"Макет '{photo.image_name}' успешно завершен!")
                return redirect("task_list_director")

    context = {
        'photo': photo,
    }
    return render(request, 'director/maket_director.html', context)


def upload_file_to_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            photo_file = form.save(commit=False)
            photo_file.photo = photo
            photo_file.save()
            return redirect('task_list_director')  # Замените на правильный путь после сохранения

    else:
        form = UploadFileForm()

    return render(request, 'upload_file.html', {'form': form, 'photo': photo})


def upload_photo(request):
    if request.method == 'POST':
        photos = request.FILES.getlist('photo')  # Загружаем все загруженные фотографии
        for photo in photos:
            new_photo = Photo(image=photo)
            new_photo.save()
        return redirect('task_list_director')  # Перенаправляем на страницу с изображениями

    return render(request, 'director/upload_photo_director.html')


def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    if request.method == 'POST':
        # Проверка прав доступа
        if not request.user.is_superuser:
            messages.error(request, 'Недостаточно прав для удаления')
            return redirect('task_list_director')

        # Удаление связанных задач
        Task.objects.filter(photo=photo).delete()

        # Удаление файла изображения
        if photo.image:
            photo.image.delete(save=False)

        photo.delete()
        messages.success(request, 'Макет удален')
        return redirect('task_list_director')

    return redirect('task_list_director')

def upload_photo_director(request):
    if request.method == 'POST':
        photos = request.FILES.getlist('photo')  # Загружаем все загруженные фотографии
        form = AddDescriptionForm(request.POST)  # Используем форму для получения данных
        if form.is_valid():
            for photo in photos:
                new_photo = Photo(
                    image=photo,
                    image_name=form.cleaned_data['image_name'],  # Название
                    description=form.cleaned_data['description'],  # Описание
                    requirements=form.cleaned_data['requirements'],  # Требования
                    due_date=form.cleaned_data['due_date'],  # Срок сдачи
                    assigned_manager=form.cleaned_data['assigned_manager'],  # Назначенный менеджер
                )
                new_photo.save()
            return redirect('task_list_director')  # Перенаправляем на страницу с изображениями
        else:
            # Если форма невалидна, вернуть её обратно с ошибками
            return render(request, 'director/upload_photo_director.html', {'form': form})
    else:
        form = AddDescriptionForm()  # Создаем пустую форму для GET-запроса
    return render(request, 'director/upload_photo_director.html', {'form': form})


def delete_task_director(request, task_id):
    # Получаем задачу по ID или возвращаем 404, если задача не найдена
    task = get_object_or_404(Task, id=task_id)

    # Сохраняем photo_id перед удалением задачи
    photo_id = task.photo.id

    # Удаляем задачу
    task.delete()

    # Перенаправляем пользователя на страницу деталей макета
    return redirect('maket_director', photo_id=photo_id)



def task_list_director(request):
    if request.method == "POST":
        action = request.POST.get("action")
        photo_id = request.POST.get("photo_id")

        if action == "complete":
            # Получаем макет по photo_id
            photo = get_object_or_404(Photo, id=photo_id)

            # Проверяем, завершены ли все задачи, связанные с этим макетом
            tasks = Task.objects.filter(photo=photo)
            if not all(task.completed for task in tasks):
                # Если не все задачи завершены, показываем сообщение об ошибке
                return render(request, "director/task_list_director.html", {
                    "tasks": Task.objects.all(),
                    "photos": Photo.objects.all(),
                    "error_message": f"Невозможно завершить макет. Сначала завершите все задачи для макета {photo.image_name}."
                })

            # Если все задачи завершены, можно завершить макет
            if not photo.is_completed:
                photo.is_completed = True
                photo.save()

            return redirect('task_list_director')

    # Получаем все фотографии из базы данных
    photos = Photo.objects.all()

    # Добавляем информацию о процентах завершения для каждого макета
    for photo in photos:
        total_tasks = Task.objects.filter(photo=photo).count()
        completed_tasks_count = Task.objects.filter(photo=photo, completed=True).count()

        if total_tasks > 0:
            photo.completion_percentage = (completed_tasks_count / total_tasks) * 100
        else:
            photo.completion_percentage = 0

    # Получаем все задачи и фотографии из базы данных
    tasks = Task.objects.all()

    # Передаем задачи и фотографии в шаблон
    return render(request, "director/task_list_director.html", {"tasks": tasks, "photos": photos})


def employee_director(request):
    # Получаем параметр сортировки из GET-запроса
    sort_by = request.GET.get('sort_by', 'name')  # По умолчанию сортировка по имени
    
    # Получаем всех пользователей, исключая менеджеров и непринятых
    users = CustomUser.objects.exclude(Q(post_user='manager') | Q(post_user='unapproved'))
    
    # Применяем сортировку
    if sort_by == 'name':
        # Сортируем по имени от А до Я
        users = users.order_by('full_name')
    elif sort_by == 'position':
        # Сортируем по должности
        users = users.order_by('post_user')
    
    context = {
        'users': users,
        'current_sort': sort_by,
    }
    return render(request, 'director/employee.html', context)


def employee_manager(request):
    users = CustomUser.objects.filter(post_user='manager')
    return render(request, 'director/employee_manager.html', {'users': users})

def profile_employee(request, user_id):
    print(f"Received user_id: {user_id}")  # Временное сообщение для отладки
    user = get_object_or_404(CustomUser, id=user_id)  # Получаем одного пользователя
    return render(request, 'director/profile_employee.html',
{'user': user})  # Передаем единственного пользователя в контекст


def promotion_requests(request):
    requests = PromotionRequest.objects.all()

    return render(request, 'director/promotion_requests.html', {'requests': requests})


from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserForm

def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            # Получаем новую должность пользователя
            post_user = form.cleaned_data.get('post_user')

            # Устанавливаем значение big_stavka на основе новой должности
            if post_user != user.post_user:  # Если должность изменилась
                user.big_stavka = user.calculate_default_stavka()  # Устанавливаем новую ставку
            else:
                # Если должность не изменилась, сохраняем текущее значение
                user.big_stavka = form.cleaned_data.get('big_stavka', user.big_stavka)

            form.save()  # Сохраняем изменения в базе данных
            return redirect('/director/employee_director/')
    else:
        form = UserForm(instance=user)
    return render(request, 'director/edit_user.html', {'form': form, 'user': user})


def director_promotions(request):
    promotion_requests = PromotionRequest.objects.all()  # Получение всех запросов на повышение

    if request.method == 'POST':
        promotion_request_id = request.POST.get('promotion_request_id')
        approve = request.POST.get('approve')  # Получаем информацию о подтверждении

        # Проверка и обработка запроса
        try:
            promotion_request = PromotionRequest.objects.get(id=promotion_request_id)
            if approve:  # Если запрос подтверждается
                user = promotion_request.user
                user.post_user = promotion_request.requested_post  # Обновляем пост пользователя
                user.save()
                messages.success(request, 'Запрос на повышение подтвержден и должность обновлена.')
            else:
                promotion_request.delete()  # Возможно, удалить отклоненный запрос
                messages.info(request, 'Запрос на повышение отклонен.')

            # Удаляем запрос после обработки
            promotion_request.delete()

        except PromotionRequest.DoesNotExist:
            messages.error(request, 'Запрос на повышение не найден.')
        except Exception as e:
            messages.error(request, f'Ошибка: {str(e)}')

    context = {
        'promotion_requests': promotion_requests,
    }
    return render(request, 'director/director_promotions.html', context)


from django.shortcuts import render
from django.db.models import Count, Sum, Avg, Q
from users.models import CustomUser, TimeEntry
from manager2.models import Task  # Пример, если модели пользователей и задач называются так


def home_director(request):
    # Общее число пользователей
    total_users = CustomUser.objects.count()

    # Кол-во активных пользователей
    active_users = CustomUser.objects.filter(is_active=True).count()

    # Выполненные задачи
    completed_tasks = Task.objects.filter(completed=True).count()

    completed_maket = Photo.objects.filter(is_completed=True).count()

    # Среднее время выполнения задач
    average_task_time = Task.objects.aggregate(Avg('time_spent'))['time_spent__avg'] or 0

    # Общая зарплата (сумма всех salary из TimeEntry)
    total_salary = TimeEntry.total_salary_users()
    total_salary_manager = TimeManger.total_salary_users_money()
    full_zarplata = total_salary + total_salary_manager

    # Общая сумма премий
    total_prizes = PrizeHistory.objects.aggregate(total=Sum('amount'))['total'] or 0

    # Передаем данные в шаблон
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'completed_tasks': completed_tasks,
        'completed_maket': completed_maket,
        'average_task_time': average_task_time,
        'total_salary': total_salary,
        'full_zarplata': full_zarplata,
        'total_salary_manager': total_salary_manager,
        'total_prizes': total_prizes,
    }
    return render(request, 'director/home.html', context)


def director_dashboard(request):
    unapproved_users = CustomUser.objects.filter(post_user='unapproved', is_active = True)
    user_type_choices = CustomUser.USER_TYPE_CHOICES  # Получаем доступные роли

    return render(request, 'director/director_dashboard.html', {
        'unapproved_users': unapproved_users,
        'user_type_choices': user_type_choices,
    })


def approve_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    # Получаем роль из формы
    user_role = request.POST.get('user_role')
    if user_role:
        user.post_user = user_role
        user.save()
        messages.success(request, f'Пользователь {user.email} был подтверждён как {user_role}.')

    return redirect('director_dashboard')


User = get_user_model()

# views.py
def add_task_director(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    template_id = request.GET.get('template_id')
    
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.photo = photo
            task.save()
            form.save_m2m()  # Сохраняем связи many-to-many
            return redirect('maket_director', photo_id=photo.id)
    else:
        initial_data = {}
        if template_id:
            try:
                template = TaskTemplate.objects.get(id=template_id)
                initial_data = {
                    'title': template.title,
                    'description': template.description,
                    'max_assigned_users': template.max_assigned_users
                }
            except TaskTemplate.DoesNotExist:
                pass
        form = TaskForm(initial=initial_data)
    
    return render(request, 'director/add_task_director.html', {
        'form': form,
        'photo': photo,
        'templates': TaskTemplate.objects.all()  # Добавляем список шаблонов в контекст
    })





def task_list_director_completed(request):
    photos = Photo.objects.all()
    return render(request, "director/task_list_director_completed.html", { "photos": photos})


def completed_maket(request, photo_id):

    photo = get_object_or_404(Photo, id=photo_id)

    completed_maket = Task.objects.filter(photo=photo, completed=True)

    context = {
        'photo': photo,
        'completed_maket': completed_maket,
    }
    return render(request, 'director/completed_maket.html', context)


def director_prize(request):
    users = CustomUser.objects.exclude(post_user='unapproved')
    return render(request, "director/director_prize.html", {'users': users})


def set_prize(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        try:
            # Получаем значение премии из POST-запроса
            prize_amount = float(request.POST.get('prize', 0))

            # Проверяем, что премия находится в допустимом диапазоне
            if prize_amount < 100 or prize_amount > 50000:
                messages.error(request, "Премия должна быть в диапазоне от 100 до 50000 рублей.")
                return redirect('director_prize')

            # Сохраняем текущую премию в истории
            PrizeHistory.objects.create(user=user, amount=prize_amount)

            # Обновляем текущую премию пользователя
            user.prize = prize_amount
            user.save()

            messages.success(request, f"Премия для {user.full_name} успешно обновлена.")
        except ValueError:
            messages.error(request, "Некорректное значение премии.")

    return redirect('director_prize')



from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum
from datetime import datetime
from users.models import PrizeHistory  # Импортируем вашу модель PrizeHistory

def prize_history(request):
    selected_month_str = request.GET.get('month')

    if selected_month_str:
        try:
            selected_month = datetime.strptime(selected_month_str, '%Y-%m').date()
        except (ValueError, TypeError):
            selected_month = timezone.now().date()
    else:
        selected_month = timezone.now().date()

    first_day_of_month = selected_month.replace(day=1)
    if selected_month.month == 12:
        last_day_of_month = selected_month.replace(year=selected_month.year + 1, month=1, day=1)
    else:
        last_day_of_month = selected_month.replace(month=selected_month.month + 1, day=1)

    # Получаем историю премий, включая объекты пользователей
    history = (
        PrizeHistory.objects
        .filter(date__gte=first_day_of_month, date__lt=last_day_of_month)
        .select_related('user')  # Загрузка связанного пользователя
    )

    # Группируем и суммируем премии
    aggregated_history = {}
    for entry in history:
        if entry.user.full_name in aggregated_history:
            aggregated_history[entry.user.full_name] += entry.amount
        else:
            aggregated_history[entry.user.full_name] = entry.amount

    context = {
        'history': [(name, total) for name, total in aggregated_history.items()],  # Преобразуем в список для шаблона
        'selected_month': selected_month.strftime('%Y-%m'),
    }

    return render(request, 'director/prize_history.html', context)



from django.db.models import Sum, F, ExpressionWrapper, FloatField, fields
from datetime import datetime, timedelta
from django.shortcuts import render
from users.models import TimeEntry, CustomUser
from django.db import models
from manager2.models import TaskReview
from django.db.models import Prefetch
from django.db.models import Count,Subquery, Avg, Q, OuterRef, IntegerField
from django.utils import timezone
from django.db.models.functions import Coalesce
from django.db.models import Value, FloatField

def salary_report(request):
    # Получаем параметры из GET-запроса
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    post_user = request.GET.get('post_user')  # Фильтр по роли
    sort_by = request.GET.get('sort_by', 'desc')  # Сортировка (по умолчанию убывание)

    # Преобразуем строки в объекты datetime
    try:
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            # Включаем сегодняшний день в диапазон
            end_date_plus_one = end_date + timedelta(days=1)
        else:
            start_date = None
            end_date_plus_one = None
    except ValueError:
        start_date = None
        end_date_plus_one = None

    # Подсчитываем количество завершенных задач для каждого пользователя через Subquery
    completed_tasks_subquery = TaskReview.objects.filter(
        user=OuterRef('pk'),  # Связываем с внешним запросом
        task__completed=True  # Учитываем только завершенные задачи
    )

    # Добавляем фильтрацию по датам, если они указаны
    if start_date and end_date_plus_one:
        completed_tasks_subquery = completed_tasks_subquery.filter(
            task__created_at__gte=start_date,
            task__created_at__lt=end_date_plus_one
        )
    completed_tasks_subquery = completed_tasks_subquery.values('user').annotate(
        count=Count('task')
    ).values('count')

    # Аннотируем средний рейтинг и количество завершенных задач
    users = CustomUser.objects.filter(is_active=True).annotate(
        average_ratings=Avg('reviews_user__rating', filter=Q(reviews_user__rating__isnull=False)),
        completed_tasks_count=Subquery(completed_tasks_subquery, output_field=models.IntegerField())
    )

    users = CustomUser.objects.filter(is_active=True).annotate(
        average_ratings=Avg('reviews_user__rating', filter=Q(reviews_user__rating__isnull=False)),
        completed_tasks_count=Subquery(completed_tasks_subquery, output_field=models.IntegerField())
    )

    # Аннотируем список макетов, над которыми работал сотрудник
    if start_date and end_date_plus_one:
        users = users.prefetch_related(
            Prefetch(
                'submitted_reviews',  # Используем related_name='submitted_reviews'
                queryset=Task.objects.filter(
                    completed=True,  # Только завершенные задачи
                    created_at__gte=start_date,  # Фильтр по дате начала
                    created_at__lt=end_date_plus_one  # Фильтр по дате окончания
                ).select_related('photo'),  # Предварительно загружаем связанные макеты
                to_attr='completed_tasks'  # Сохраняем результат в атрибуте completed_tasks
            )
        )
    else:
        # Если даты не заданы, используем все завершенные задачи без фильтрации по датам
        users = users.prefetch_related(
            Prefetch(
                'submitted_reviews',  # Используем related_name='submitted_reviews'
                queryset=Task.objects.filter(
                    completed=True  # Только завершенные задачи
                ).select_related('photo'),  # Предварительно загружаем связанные макеты
                to_attr='completed_tasks'  # Сохраняем результат в атрибуте completed_tasks
            )
        )

    # Создаем словарь для хранения макетов, над которыми работал каждый сотрудник
    user_worked_photos = {}

    for user in users:
        # Получаем список завершенных задач
        completed_tasks = getattr(user, 'completed_tasks', [])

        if not isinstance(completed_tasks, list):
            # Если 'completed_tasks' является ManyRelatedManager, преобразуем его в список
            completed_tasks = list(completed_tasks.all())

        # Собираем названия макетов
        photo_names = [
            task.photo.image_name for task in completed_tasks
            if task.photo and hasattr(task.photo, 'image_name')
        ]
        user_worked_photos[user.id] = ', '.join(set(photo_names)) if photo_names else 'Нет макетов'


    if start_date and end_date_plus_one:
        try:
            # Аннотируем общую зарплату за период для сотрудников
            users = users.annotate(
                total_salary=Sum(ExpressionWrapper(
                    ((F('timeentry__end_time') - F('timeentry__start_time')) / timedelta(hours=1)) * F('big_stavka'),
                    output_field=FloatField()
                ), filter=models.Q(timeentry__start_time__gte=start_date, timeentry__end_time__lt=end_date_plus_one))
            )
            # Рассчитываем общую зарплату за период через метод модели
            total_salary = TimeEntry.total_salary_users_money_user(start_date=start_date, end_date=end_date_plus_one)
            # Рассчитываем индивидуальную зарплату для каждого сотрудника
            individual_salaries = TimeEntry.total_salary_for_each_user_user(start_date=start_date, end_date=end_date_plus_one)
        except ValueError:
            # Если дата указана некорректно
            users = CustomUser.objects.filter(is_active=True).annotate(
                average_ratings=Avg('reviews_user__rating', filter=models.Q(reviews_user__rating__isnull=False))
            )
            total_salary = 0
            individual_salaries = {}
    else:
        # Если период не выбран, показываем только сотрудников без зарплаты
        total_salary = None
        individual_salaries = {}

    # Исключаем менеджеров из списка сотрудников
    users = users.exclude(post_user='manager')

    # Применяем фильтр по роли
    if post_user:
        users = users.filter(post_user=post_user)

    # Применяем сортировку
    if sort_by == 'asc':
        users = users.order_by('big_stavka')  # По возрастанию ставки
    elif sort_by == 'desc':
        users = users.order_by('-big_stavka')  # По убыванию ставки
    elif sort_by == 'wasc' and 'average_ratings' in users.query.annotations:
        users = users.order_by('average_ratings')  # По возрастанию рейтинга
    elif sort_by == 'wdesc' and 'average_ratings' in users.query.annotations:
        users = users.order_by('-average_ratings')  # По убыванию рейтинга
    elif sort_by == 'task' and 'completed_tasks_count' in users.query.annotations:
        users = users.order_by('completed_tasks_count')  # По возрастанию количества завершенных задач
    elif sort_by == 'anti_task' and 'completed_tasks_count' in users.query.annotations:
        users = users.order_by('-completed_tasks_count')  # По убыванию количества завершенных задач

    # Передаем данные в шаблон
    context = {
        'users': users,  # Список сотрудников
        'total_salary': total_salary,  # Общая зарплата за период
        'individual_salaries': individual_salaries,  # Зарплата для каждого сотрудника
        'post_user_choices': CustomUser.USER_TYPE_CHOICES,  # Выпадающий список ролей
        'selected_post_user': post_user,  # Выбранная роль
        'sort_by': sort_by,  # Текущий порядок сортировки
        'start_date': start_date.strftime('%Y-%m-%d') if start_date else '',
        'end_date': end_date.strftime('%Y-%m-%d') if end_date else '',
        'user_worked_photos': user_worked_photos
    }
    return render(request, 'director/salary_report.html', context)


from manager2.models import TimeManger

def salary_manager(request):
    # Получаем параметры из GET-запроса
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    post_user = request.GET.get('post_user')  # Фильтр по роли
    sort_by = request.GET.get('sort_by', 'desc')  # Сортировка (по умолчанию убывание)

    try:
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            end_date_plus_one = end_date + timedelta(days=1)  # Включаем последний день в диапазон
        else:
            start_date = None
            end_date_plus_one = None
    except ValueError:
        start_date = None
        end_date_plus_one = None

    # Подсчитываем количество завершенных задач для каждого менеджера через Subquery
    completed_tasks_subquery = Task.objects.filter(
        created_by=OuterRef('pk'),  # Связываем с внешним запросом
        completed=True  # Учитываем только завершенные задачи
    )

    if start_date and end_date_plus_one:
        completed_tasks_subquery = completed_tasks_subquery.filter(
            created_at__gte=start_date,
            created_at__lt=end_date_plus_one
        )

    completed_tasks_subquery = completed_tasks_subquery.values('created_by').annotate(
        count=Count('id')
    ).values('count')

    # Аннотируем средний рейтинг, количество завершенных задач и зарплату
    users = CustomUser.objects.filter(is_active=True, post_user='manager').annotate(
        completed_tasks_count=Subquery(completed_tasks_subquery, output_field=models.IntegerField())
    )

    # Аннотируем общую зарплату за период для менеджеров
    if start_date and end_date_plus_one:
        try:
            users = users.annotate(
                total_salary=Coalesce(
                    Sum(
                        ExpressionWrapper(
                            ((F('timemanger_set__end_time') - F('timemanger_set__start_time')) / timedelta(
                                hours=1)) * F('big_stavka'),
                            output_field=FloatField()
                        ),
                        filter=Q(timemanger_set__start_time__gte=start_date,
                                 timemanger_set__end_time__lt=end_date_plus_one)
                    ),
                    Value(0.0),
                    output_field=FloatField()
                )
            )
            # Рассчитываем общую зарплату за период через метод модели
            total_salary = TimeManger.total_salary_users_money(start_date=start_date, end_date=end_date_plus_one)
            # Рассчитываем индивидуальную зарплату для каждого менеджера
            individual_salaries = TimeManger.total_salary_for_each_user(start_date=start_date,
                                                                        end_date=end_date_plus_one)
        except ValueError:
            total_salary = 0
            individual_salaries = {}
    else:
        total_salary = None
        individual_salaries = {}

    # Аннотируем список макетов, созданных менеджером
    if start_date and end_date_plus_one:
        users = users.prefetch_related(
            Prefetch(
                'user_muser',  # related_name для задач, созданных менеджером
                queryset=Task.objects.filter(
                    completed=True,  # Только завершенные задачи
                    created_at__gte=start_date,  # Фильтр по дате начала
                    created_at__lt=end_date_plus_one  # Фильтр по дате окончания
                ).select_related('photo'),  # Предварительно загружаем связанные макеты
                to_attr='published_tasks'  # Сохраняем результат в атрибуте published_tasks
            )
        )
    else:
        users = users.prefetch_related(
            Prefetch(
                'user_muser',  # related_name для задач, созданных менеджером
                queryset=Task.objects.filter(
                    completed=True  # Только завершенные задачи
                ).select_related('photo'),  # Предварительно загружаем связанные макеты
                to_attr='published_tasks'  # Сохраняем результат в атрибуте published_tasks
            )
        )

    # Создаем словарь для хранения названий макетов
    user_published_photos = {}
    for user in users:
        published_tasks = getattr(user, 'published_tasks', [])
        photo_names = [
            task.photo.image_name for task in published_tasks
            if task.photo and hasattr(task.photo, 'image_name')
        ]
        user_published_photos[user.id] = ', '.join(set(photo_names)) if photo_names else 'Нет макетов'

    # Применяем фильтр по роли (если указан)
    if post_user:
        users = users.filter(post_user=post_user)

    # Применяем сортировку
    if sort_by == 'asc':
        users = users.order_by('big_stavka')  # По возрастанию ставки
    elif sort_by == 'desc':
        users = users.order_by('-big_stavka')  # По убыванию ставки
    elif sort_by == 'wasc' and 'average_ratings' in users.query.annotations:
        users = users.order_by('average_ratings')  # По возрастанию рейтинга
    elif sort_by == 'wdesc' and 'average_ratings' in users.query.annotations:
        users = users.order_by('-average_ratings')  # По убыванию рейтинга
    elif sort_by == 'task' and 'completed_tasks_count' in users.query.annotations:
        users = users.order_by('completed_tasks_count')  # По возрастанию количества завершенных задач
    elif sort_by == 'anti_task' and 'completed_tasks_count' in users.query.annotations:
        users = users.order_by('-completed_tasks_count')  # По убыванию количества завершенных задач

    # Передаем данные в шаблон
    context = {
        'users': users,  # Список менеджеров
        'total_salary': total_salary,  # Общая зарплата за период
        'individual_salaries': individual_salaries,  # Зарплата для каждого менеджера
        'post_user_choices': CustomUser.USER_TYPE_CHOICES,  # Выпадающий список ролей
        'selected_post_user': post_user,  # Выбранная роль
        'sort_by': sort_by,  # Текущий порядок сортировки
        'start_date': start_date.strftime('%Y-%m-%d') if start_date else '',
        'end_date': end_date.strftime('%Y-%m-%d') if end_date else '',
        'user_published_photos': user_published_photos  # Словарь с макетами, созданными менеджером
    }

    return render(request, 'director/salary_manager.html', context)



def director_user_statistic(request, user_id):
    current_user = get_object_or_404(CustomUser, id=user_id)

    # Обработка выбора месяца
    selected_month = timezone.now().date()
    if 'month' in request.GET:
        try:
            selected_month = datetime.strptime(request.GET['month'], '%Y-%m').date()
        except ValueError:
            pass

    # Определение границ месяца
    first_day = selected_month.replace(day=1)
    if selected_month.month == 12:
        last_day = selected_month.replace(year=selected_month.year + 1, month=1, day=1)
    else:
        last_day = selected_month.replace(month=selected_month.month + 1, day=1)

    # Расчет зарплаты
    try:
        salary_data = TimeEntry.boss_total_salary_for_each_user(
            start_date=first_day,
            end_date=last_day,
            user_id=current_user.id
        )
        total_salary = salary_data.get(current_user.id, 0)
    except Exception:
        total_salary = 0

    # Подзапрос для подсчета задач
    completed_tasks_subquery = Task.objects.filter(
        submitted_by=OuterRef('pk'),
        completed=True,
        created_at__range=(first_day, last_day)
    ).values('submitted_by').annotate(
        count=Count('id')
    ).values('count')

    # Аннотация данных пользователя
    user_data = CustomUser.objects.filter(id=current_user.id).annotate(
        avg_rating_annotation=Avg('reviews_user__rating'),
        completed_tasks_count=Subquery(completed_tasks_subquery, output_field=models.IntegerField()) or 0
    ).first()

    # Отдельный запрос для макетов
    completed_tasks_with_photos = Task.objects.filter(
        submitted_by=current_user,
        completed=True,
        created_at__range=(first_day, last_day)
    ).select_related('photo')

    worked_photos = Task.objects.filter(
        submitted_by=current_user,
        completed=True,
        created_at__range=(first_day, last_day)
    ).distinct().count()

    context = {
        'user': current_user,
        'user_data': user_data,
        'total_salary': total_salary,
        'worked_photos': worked_photos,
        'selected_month': selected_month,
        'current_year': timezone.now().year,
        'current_month': timezone.now().month,
        'start_date': first_day,
        'end_date': last_day,
    }

    return render(request, 'director/director_user_statistic.html', context)

def director_manager_statistic(request, user_id):
    current_user = get_object_or_404(CustomUser, id=user_id)

    # Обработка выбора месяца
    selected_month_str = request.GET.get('month')
    selected_month = timezone.now().date()
    if selected_month_str:
        try:
            selected_month = datetime.strptime(selected_month_str, '%Y-%m').date()
        except ValueError:
            pass

    # Определение границ месяца
    first_day = selected_month.replace(day=1)
    if selected_month.month == 12:
        last_day = selected_month.replace(year=selected_month.year + 1, month=1, day=1)
    else:
        last_day = selected_month.replace(month=selected_month.month + 1, day=1)

    # Подсчет созданных задач
    created_tasks_subquery = Task.objects.filter(
        created_by=current_user,
        completed=True,
        created_at__range=(first_day, last_day)
    ).values('created_by').annotate(
        count=Count('id')
    ).values('count')[:1]

    # Подсчет проверенных задач через TaskReview
    reviewed_tasks_subquery = TaskReview.objects.filter(
        manager=current_user,
        task__completed=True,
        reviewed_at__range=(first_day, last_day)
    ).values('manager').annotate(
        count=Count('id')
    ).values('count')[:1]

    total_shift_hours = TimeManger.objects.filter(
        manager=current_user,
        start_time__gte=first_day,  # Заменено на first_day
        start_time__lt=last_day,  # Заменено на last_day
        end_time__isnull=False
    ).aggregate(
        total_hours=Sum(
            (F('end_time') - F('start_time')),
            output_field=fields.DurationField()
        )
    )['total_hours']

    total_shift_hours = total_shift_hours.total_seconds() / 3600 if total_shift_hours else 0

    # Аннотация данных пользователя
    user_data = CustomUser.objects.filter(id=current_user.id).annotate(
        created_tasks=Coalesce(
            Subquery(created_tasks_subquery, output_field=IntegerField()),
            0
        ),
        reviewed_tasks=Coalesce(
            Subquery(reviewed_tasks_subquery, output_field=IntegerField()),
            0
        )
    ).first()

    # Расчет зарплаты
    try:
        salary_data = TimeManger.boss_total_salary_for_each_user(
            start_date=first_day,
            end_date=last_day,
            manager_id=current_user.id  # Передаем manager_id
        )
        total_salary = salary_data.get(current_user.id, 0)
    except Exception as e:
        print(f"Ошибка расчета зарплаты: {str(e)}")  # Для отладки
        total_salary = 0

    # Получение макетов созданных задач
    created_tasks = Task.objects.filter(
        created_by=current_user,
        completed=True,
        created_at__range=(first_day, last_day)
    ).select_related('photo')

    worked_photos = Task.objects.filter(
        created_by=current_user,
        completed=True,
        created_at__range=(first_day, last_day)
    ).distinct().count()

    context = {
        'user_data': user_data,
        'total_salary': total_salary,
        'worked_photos': worked_photos,
        'selected_month': selected_month,
        'current_year': timezone.now().year,
        'current_month': timezone.now().month,
        'start_date': first_day,
        'end_date': last_day,
        'total_shift_hours': total_shift_hours,
    }

    return render(request, 'director/director_manager_statistic.html', context)

def is_director(user):
    return user.email == 'albygroup@bk.ru'


def employee_shiftsdir(request, user_id):
    employee = get_object_or_404(CustomUser, id=user_id)

    active_task = Task.objects.filter(
        submitted_by=employee,
        is_rated=False,
        is_submitted_for_review=False  # или False — зависит от твоей логики
    ).first()

    # Получаем выбранный месяц из параметров GET-запроса
    selected_month_str = request.GET.get('month')

    # Если месяц не выбран, используем текущий месяц
    if selected_month_str:
        try:
            selected_month = datetime.strptime(selected_month_str, '%Y-%m').date()
        except (ValueError, TypeError):
            selected_month = timezone.now().date()
    else:
        selected_month = timezone.now().date()

    # Определяем первый и последний день выбранного месяца
    first_day_of_month = selected_month.replace(day=1)
    if selected_month.month == 12:
        last_day_of_month = selected_month.replace(year=selected_month.year + 1, month=1, day=1)
    else:
        last_day_of_month = selected_month.replace(month=selected_month.month + 1, day=1)

    # Получаем записи времени для сотрудника за выбранный период
    time_entries = TimeEntry.objects.filter(
        user=employee,
        timer_type='shift',
        start_time__gte=first_day_of_month,
        start_time__lt=last_day_of_month,
        end_time__isnull=False
    ).order_by('-start_time')

    # Рассчитываем общее время и зарплату
    total_duration = timezone.timedelta()
    for entry in time_entries:
        if entry.end_time and entry.start_time:
            total_duration += entry.end_time - entry.start_time

    total_salary = sum(entry.salary() for entry in time_entries)

    context = {
        'employee': employee,
        'time_entries': time_entries,
        'selected_month': selected_month,
        'total_duration': total_duration,
        'total_salary': total_salary,
        'active_task': active_task,
    }

    return render(request, 'director/employee_shifts.html', context)

def manager_shifts(request, user_id):
    manager = get_object_or_404(CustomUser, id=user_id)
    
    # Получаем выбранный месяц из параметров GET-запроса
    selected_month_str = request.GET.get('month')
    
    # Если месяц не выбран, используем текущий месяц
    if selected_month_str:
        try:
            selected_month = datetime.strptime(selected_month_str, '%Y-%m').date()
        except (ValueError, TypeError):
            selected_month = timezone.now().date()
    else:
        selected_month = timezone.now().date()
    
    # Определяем первый и последний день выбранного месяца
    first_day_of_month = selected_month.replace(day=1)
    if selected_month.month == 12:
        last_day_of_month = selected_month.replace(year=selected_month.year + 1, month=1, day=1)
    else:
        last_day_of_month = selected_month.replace(month=selected_month.month + 1, day=1)
    
    # Получаем записи времени для менеджера за выбранный период
    time_entries = TimeManger.objects.filter(
        manager=manager,
        start_time__gte=first_day_of_month,
        start_time__lt=last_day_of_month,
        end_time__isnull=False
    ).order_by('-start_time')
    
    # Рассчитываем общее время и зарплату
    total_duration = timezone.timedelta()
    for entry in time_entries:
        if entry.end_time and entry.start_time:
            total_duration += entry.end_time - entry.start_time
    
    total_salary = sum(entry.salary for entry in time_entries)
    
    context = {
        'manager': manager,
        'time_entries': time_entries,
        'selected_month': selected_month,
        'total_duration': total_duration,
        'total_salary': total_salary,
    }
    
    return render(request, 'director/manager_shifts.html', context)

def create_task_template(request):
    photo_id = request.GET.get('photo_id')
    if request.method == 'POST':
        form = TaskTemplateForm(request.POST)
        if form.is_valid():
            template = form.save()
            messages.success(request, 'Шаблон задачи успешно создан!')
            if photo_id:
                return redirect('add_task_director', photo_id=photo_id)
            return redirect('task_templates_list')
    else:
        form = TaskTemplateForm()
    
    return render(request, 'director/create_task_template.html', {
        'form': form,
        'photo': {'id': photo_id} if photo_id else None
    })

def get_template_data(request, template_id):
    template = get_object_or_404(TaskTemplate, id=template_id)
    data = {
        'title': template.title,
        'description': template.description,
        'max_assigned_users': template.max_assigned_users
    }
    return JsonResponse(data)

def task_templates_list(request):
    templates = TaskTemplate.objects.all().order_by('-id')
    return render(request, 'director/task_templates_list.html', {
        'templates': templates
    })

def delete_task_template(request, template_id):
    template = get_object_or_404(TaskTemplate, id=template_id)
    template.delete()
    messages.success(request, 'Шаблон задачи успешно удален')
    return redirect('task_templates_list')

def edit_task_template(request, template_id):
    template = get_object_or_404(TaskTemplate, id=template_id)
    
    if request.method == 'POST':
        form = TaskTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            messages.success(request, 'Шаблон задачи успешно обновлен')
            return redirect('task_templates_list')
    else:
        form = TaskTemplateForm(instance=template)
    
    return render(request, 'director/edit_task_template.html', {
        'form': form,
        'template': template
    })

