
from django.contrib import admin
from .models import Hotel, MenuItem


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'phone', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
    search_fields = ('name', 'owner__username', 'phone')
    actions = ['approve_hotels']

    def approve_hotels(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} hotels approved.")
    approve_hotels.short_description = "Approve selected hotels"


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'price', 'category', 'available')
    list_filter = ('category', 'available', 'hotel')
    search_fields = ('name', 'hotel__name')
