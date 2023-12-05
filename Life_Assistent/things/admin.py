from django.contrib import admin
from .models import TodoList

# Register your models here.

@admin.register(TodoList)
class TodoListAdmin(admin.ModelAdmin):
    list_display = ['user','date','status']
    list_filter = ['user','date']
    search_fields = ['date','tasks']
    raw_id_fields = ['user',]
    date_hierarchy = 'date'
    ordering = ['status', 'date']
