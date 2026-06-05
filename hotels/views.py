from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.db.models import Q
from math import radians, sin, cos, sqrt, atan2
from .models import Hotel, MenuItem
from .forms import OwnerRegistrationForm, MenuItemForm


def is_hotel_owner(user):
    return hasattr(user, 'hotel') and user.hotel.is_approved


def is_admin_user(user):
    return user.is_superuser


def register(request):
    if request.method == 'POST':
        form = OwnerRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('pending_approval')
    else:
        form = OwnerRegistrationForm()
    return render(request, 'hotels/register.html', {'form': form})


def pending_approval(request):
    return render(request, 'hotels/pending_approval.html')


@login_required
@user_passes_test(is_hotel_owner)
def dashboard(request):
    hotel = request.user.hotel
    menu_items = hotel.menu_items.all()
    return render(request, 'hotels/dashboard.html', {'hotel': hotel, 'menu_items': menu_items})


@login_required
@user_passes_test(is_hotel_owner)
def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.hotel = request.user.hotel
            item.save()
            return redirect('dashboard')
    else:
        form = MenuItemForm()
    return render(request, 'hotels/menu_form.html', {'form': form, 'title': 'Add Item'})


@login_required
@user_passes_test(is_hotel_owner)
def edit_menu_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk, hotel=request.user.hotel)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'hotels/menu_form.html', {'form': form, 'title': 'Edit Item'})


@login_required
@user_passes_test(is_hotel_owner)
def delete_menu_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk, hotel=request.user.hotel)
    item.delete()
    return redirect('dashboard')

# Public views


def home(request):
    hotels = Hotel.objects.filter(is_approved=True)
    query = request.GET.get('q')
    if query:
        hotels = hotels.filter(Q(name__icontains=query)
                               | Q(address__icontains=query))
    # Nearby logic (if lat/lng provided)
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    if lat and lng:
        lat = float(lat)
        lng = float(lng)
        hotels_with_distance = []
        for hotel in hotels:
            if hotel.latitude and hotel.longitude:
                dist = haversine(lat, lng, hotel.latitude, hotel.longitude)
                hotels_with_distance.append((hotel, dist))
            else:
                hotels_with_distance.append((hotel, None))
        hotels_with_distance.sort(
            key=lambda x: x[1] if x[1] is not None else 9999)
        hotels = [h for h, _ in hotels_with_distance]
    return render(request, 'hotels/home.html', {'hotels': hotels, 'query': query})


def hotel_detail(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id, is_approved=True)
    menu_items = hotel.menu_items.filter(available=True)
    return render(request, 'hotels/hotel_detail.html', {'hotel': hotel, 'menu_items': menu_items})


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c
