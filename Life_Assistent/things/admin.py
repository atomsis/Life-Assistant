from django.contrib import admin
from .models import TodoList,Comment

# Register your models here.

@admin.register(TodoList)
class TodoListAdmin(admin.ModelAdmin):
    list_display = ['user','date','status']
    list_filter = ['user','date']
    search_fields = ['date','tasks']
    raw_id_fields = ['user',]
    date_hierarchy = 'date'
    ordering = ['status', 'date']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','email','created','active']
    list_filter = ['active','created']
    search_fields = ['text','email','name']