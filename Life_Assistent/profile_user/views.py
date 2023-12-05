from django.shortcuts import render, get_object_or_404
from .models import TodoList
from django.contrib.auth.decorators import login_required
from datetime import date

# Create your views here.

def profile(request):
    pass