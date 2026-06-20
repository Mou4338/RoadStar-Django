import django, os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carsdealership.settings")
django.setup()
from django.contrib.auth.models import User
from djangoapp.models import CarMake, CarModel, Dealer

if not User.objects.filter(username="root").exists():
    User.objects.create_superuser("root", "admin@roadstar.example", "root123")
if not User.objects.filter(username="demo").exists():
    User.objects.create_user("demo", "demo@roadstar.example", "Demo123!", first_name="Alex", last_name="Morgan")

makes = {
    "Audi": ["A4", "Q5", "e-tron"], "BMW": ["3 Series", "X3", "i4"],
    "Ford": ["F-150", "Mustang", "Escape"], "Honda": ["Accord", "Civic", "CR-V"],
    "Tesla": ["Model 3", "Model Y", "Model S"], "Toyota": ["Camry", "Corolla", "RAV4"],
}
for make, models_ in makes.items():
    m, _ = CarMake.objects.get_or_create(name=make)
    for model_name in models_:
        CarModel.objects.get_or_create(car_make=m, name=model_name)

dealers = [
    ("RoadStar Kansas City", "Kansas City", "KS", "1550 Main Street", "66101", "(913) 555-0142", 4.9),
    ("RoadStar Wichita", "Wichita", "KS", "8200 East Kellogg Dr", "67207", "(316) 555-0194", 4.7),
    ("RoadStar Austin", "Austin", "TX", "410 Congress Avenue", "78701", "(512) 555-0118", 4.8),
    ("RoadStar San Francisco", "San Francisco", "CA", "275 Van Ness Avenue", "94102", "(415) 555-0163", 4.6),
    ("RoadStar New York", "New York", "NY", "630 11th Avenue", "10036", "(212) 555-0177", 4.9),
    ("RoadStar Chicago", "Chicago", "IL", "220 North Michigan Ave", "60601", "(312) 555-0129", 4.5),
]
for full_name, city, state, address, zip_code, phone, rating in dealers:
    Dealer.objects.get_or_create(full_name=full_name, defaults=dict(
        city=city, state=state, address=address, zip_code=zip_code, phone=phone, rating=rating))

print("Seed complete.")
print("Users:", list(User.objects.values_list("username", flat=True)))
print("Dealers:", Dealer.objects.count(), "CarMakes:", CarMake.objects.count())
