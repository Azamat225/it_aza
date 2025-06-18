from django import forms
from django.contrib.auth import get_user_model

from .models import Task, Photo, ManagerTaskTemplate
from django import forms
from users.models import CustomUser
from director.models import TaskTemplate

class TaskForm(forms.ModelForm):
    template = forms.ModelChoiceField(
        queryset=ManagerTaskTemplate.objects.all(),
        required=False,
        empty_label="Выберите шаблон",
        label="Шаблон задачи"
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_user', 'max_assigned_users']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'assigned_user': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'max_assigned_users': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Название задачи',
            'description': 'Описание',
            'assigned_user': 'Исполнители',
            'max_assigned_users': 'Максимальное количество исполнителей',
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        if self.request and self.request.user.is_authenticated:
            # Фильтруем шаблоны только текущего пользователя
            self.fields['template'].queryset = ManagerTaskTemplate.objects.filter(created_by=self.request.user)
            # Исключаем пользователей с ролями 'manager' и 'unapproved'
            self.fields['assigned_user'].queryset = CustomUser.objects.exclude(
                post_user__in=['manager', 'unapproved'])

    def clean(self):
        cleaned_data = super().clean()
        assigned_users = cleaned_data.get('assigned_user')
        max_assigned_users = cleaned_data.get('max_assigned_users')

        if assigned_users and max_assigned_users:
            if len(assigned_users) > max_assigned_users:
                self.add_error('assigned_user', f'Превышено максимальное количество сотрудников ({max_assigned_users}).')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)




class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar']

class PhotoDescriptionForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'description': 'Описание фотографии',
        }

class ManagerTaskTemplateForm(forms.ModelForm):
    class Meta:
        model = ManagerTaskTemplate
        fields = ['title', 'description', 'max_assigned_users', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'max_assigned_users': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'max_assigned_users': 'Максимальное количество исполнителей',
            'is_public': 'Сделать шаблон доступным для всех'
        }