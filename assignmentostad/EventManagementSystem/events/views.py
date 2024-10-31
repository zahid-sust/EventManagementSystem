from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, UserProfileForm, EventForm
from .models import Event, Booking, Category

# --- User Authentication and Profile Management ---

# Registration view
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # This will handle password hashing
            login(request, user)  # Log in the user automatically
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('event_list')  # Redirect to the event list after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'events/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request, username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('event_list')
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'events/login.html', {'form': form})

# Logout view
def custom_logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return render(request, 'events/logout_confirmation.html')

# Profile view
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'events/profile.html', {'form': form})

# --- Event Management ---

# Homepage view
def homepage(request):
    events = Event.objects.all()
    user_booked_events = (
        Booking.objects.filter(user=request.user).values_list('event_id', flat=True)
        if request.user.is_authenticated else []
    )
    categories = Category.objects.all()  # Fetch all categories for the dropdown
    
    return render(request, 'events/homepage.html', {
        'events': events,
        'user_booked_events': user_booked_events,
        'categories': categories,
    })

# Event list with search and filtering
def event_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    events = Event.objects.all()

    if query:
        events = events.filter(name__icontains=query)

    if category_id:
        events = events.filter(category_id=category_id)  # Filter events by category

    user_booked_events = (
        Booking.objects.filter(user=request.user).values_list('event_id', flat=True)
        if request.user.is_authenticated else []
    )

    categories = Category.objects.all()  # Fetch all categories for the filter

    return render(request, 'events/event_list.html', {
        'events': events,
        'user_booked_events': user_booked_events,
        'categories': categories,
    })

# Create event view
@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user  # Set the user creating the event
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect('event_list')  # Redirect to the event list after creation
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

# Update event view
@login_required
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user != event.created_by and not request.user.is_staff:
        messages.error(request, "You do not have permission to edit this event.")
        return redirect('event_list')

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/update_event.html', {'form': form, 'event': event})

# Delete event view
@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user != event.created_by and not request.user.is_staff:
        messages.error(request, "You do not have permission to delete this event.")
        return redirect('event_list')

    if request.method == 'POST':
        event.delete()
        messages.success(request, "Event deleted successfully!")
        return redirect('event_list')
    return render(request, 'events/confirm_delete.html', {'event': event})

# --- Booking Management ---

# Book event view
@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check if the event is fully booked
    if event.is_fully_booked():
        messages.error(request, "This event is fully booked.")
        return redirect('event_list')

    # Check if the user has already booked this event
    if Booking.objects.filter(user=request.user, event=event).exists():
        messages.error(request, "You cannot book this event; it has already been booked.")
        return redirect('event_list')

    # Proceed with booking
    Booking.objects.create(user=request.user, event=event)
    event.booked_count += 1
    event.save()

    messages.success(request, "Event booked successfully.")
    return redirect('event_list')

# View booked events
@login_required
def booked_events(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'events/booked_events.html', {'bookings': bookings})

# Search events view
def search_events(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    events = Event.objects.all()
    
    if query:
        events = events.filter(name__icontains=query)
    if category:
        events = events.filter(category=category)

    return render(request, 'events/search_results.html', {
        'events': events,
        'query': query,
        'category': category
    })
@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check if the event is fully booked
    if event.is_fully_booked():
        messages.error(request, "This event is fully booked.")
        return redirect('event_list')

    # Check if the user has already booked this event
    if Booking.objects.filter(user=request.user, event=event).exists():
        messages.error(request, "You cannot book this event; it has already been booked.")
        return redirect('event_list')

    # Proceed with booking if not fully booked
    Booking.objects.create(user=request.user, event=event)
    event.booked_count += 1
    event.save()  # Save the updated booked_count

    messages.success(request, "Event booked successfully.")
    return redirect('event_list')  # Redirects to the same page with a message
