from django.contrib import admin
from .models import CarMake, CarModel, Dealer, DealerReview


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("name", "car_make")
    list_filter = ("car_make",)


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "city", "state", "rating")
    list_filter = ("state",)
    search_fields = ("full_name", "city")


@admin.register(DealerReview)
class DealerReviewAdmin(admin.ModelAdmin):
    list_display = ("dealer", "reviewer", "sentiment", "purchased", "created_at")
    list_filter = ("sentiment", "purchased")
