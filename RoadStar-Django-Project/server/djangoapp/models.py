from django.db import models


class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.car_make.name} {self.name}"


class Dealer(models.Model):
    full_name = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    address = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=30)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)

    def __str__(self):
        return self.full_name


class DealerReview(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    review_text = models.TextField()
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_year = models.PositiveIntegerField()
    purchased = models.BooleanField(default=False)
    sentiment = models.CharField(max_length=10, default="neutral")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer.username} -> {self.dealer.full_name}"
