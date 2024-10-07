from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm,ProfileForm
from .models import Profile,Timetable
from django.contrib.auth.decorators import login_required

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('profile') 
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    profile = request.user.profile 
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard') 
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})

@login_required
def dashboard(request):
    timetable_entries = Timetable.objects.filter(user=request.user)
    
    # Organize timetable entries by day
    entries_by_day = {}
    for entry in timetable_entries:
        if entry.day not in entries_by_day:
            entries_by_day[entry.day] = []
        entries_by_day[entry.day].append(entry)

    context = {
        'entries_by_day': entries_by_day,
    }
    return render(request, 'dashboard.html', context)


#table generation view

import random

def generate_timetable(request):
    timetable_entries = []

    if request.method == 'POST':
        subjects = request.POST.getlist('subjects')  # Get subjects from the form
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        time_slots = [
            '08:00 AM - 09:00 AM',
            '09:00 AM - 10:00 AM',
            '10:00 AM - 11:00 AM', 
            '11:00 AM - 12:00 PM', 
            '01:00 PM - 02:00 PM', 
            '02:00 PM - 03:00 PM', 
            '03:00 PM - 04:00 PM', 
            '04:00 PM - 05:00 PM'
        ]

        # Clear existing timetables for the user
        Timetable.objects.filter(user=request.user).delete()

        # Create a shuffled list of subjects for each day
        subjects_list = subjects[0].split(',')  # Split the input string by commas
        
        for day in days:
            random.shuffle(subjects_list)  # Shuffle subjects for each day
            
            for i, time in enumerate(time_slots):
                subject = subjects_list[i % len(subjects_list)]  # Rotate through the subjects
                timetable_entry = Timetable(user=request.user, subject=subject, day=day, time_slot=time)
                timetable_entry.save()  # Save each timetable entry
                timetable_entries.append(timetable_entry)

    # Fetch all timetable entries for the current user
    timetable_entries = Timetable.objects.filter(user=request.user)

    # Prepare context for the template
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    time_slots = [
        '08:00 AM - 09:00 AM',
        '09:00 AM - 10:00 AM',
        '10:00 AM - 11:00 AM', 
        '11:00 AM - 12:00 PM', 
        '01:00 PM - 02:00 PM', 
        '02:00 PM - 03:00 PM', 
        '03:00 PM - 04:00 PM', 
        '04:00 PM - 05:00 PM'
    ]

    context = {
        'timetable_entries': timetable_entries,
        'days': days,
        'time_slots': time_slots,
    }
    return render(request, 'generate_timetable.html', context)

def delete_timetable(request):
    # Clear existing timetables for the user
    Timetable.objects.filter(user=request.user).delete()
    return redirect('generate_timetable') 