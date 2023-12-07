from django.urls import path
from . import views

app_name = 'todo'

urlpatterns = [
    path('',views.TaskListView.as_view(), name='task_list'),
    path('tag/<slug:tag_slug>/',views.TaskListView.as_view(), name='task_list_by_tag'),
    path('add', views.add_task, name='add_task'),
    # path('task/<str:date>/', views.task_detail, name='task_detail'),
    path('task/<int:year>-<int:month>-<int:day>/', views.task_detail, name='task_detail'),
    path('<str:date>/share/',views.tasks_share,name='tasks_share'),
    path('<str:date>/edit/',views.TaskUpdateView.as_view(), name='edit_task'),
    path('<str:date>/comment/',views.task_comment,name='task_comment'),
]
