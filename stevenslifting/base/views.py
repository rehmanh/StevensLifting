from django.shortcuts import render

from .models import Announcement

# Create your views here.
def home(request):
    announcements = Announcement.objects.all()
    context = {'announcements': announcements}
    return render(request, 'base/home.html', context)
