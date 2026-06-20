import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import CarMake, CarModel, Dealer, DealerReview


POSITIVE_WORDS = {"fantastic", "great", "excellent", "friendly", "smooth", "professional", "love", "amazing"}
NEGATIVE_WORDS = {"terrible", "awful", "rude", "slow", "bad", "horrible", "worst", "disappointed"}


def analyze_sentiment(text):
    words = set(text.lower().replace(",", " ").replace(".", " ").split())
    if words & POSITIVE_WORDS:
        return "positive", 0.95
    if words & NEGATIVE_WORDS:
        return "negative", 0.90
    return "neutral", 0.55


def home(request):
    state = request.GET.get("state", "").upper()
    dealers = Dealer.objects.all()
    if state:
        dealers = dealers.filter(state=state)
    states = Dealer.objects.values_list("state", flat=True).distinct().order_by("state")
    return render(request, "home.html", {"dealers": dealers, "states": states, "selected_state": state})


def about(request):
    return render(request, "About.html")


def contact(request):
    return render(request, "Contact.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error": "Username already taken"})
        user = User.objects.create_user(
            username=username,
            password=request.POST.get("password"),
            first_name=request.POST.get("first_name", ""),
            last_name=request.POST.get("last_name", ""),
            email=request.POST.get("email", ""),
        )
        login(request, user)
        return redirect("home")
    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            return redirect("home")
        return render(request, "login.html", {"error": "Invalid credentials"}, status=401)
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


def dealer_detail(request, dealer_id):
    dealer = get_object_or_404(Dealer, id=dealer_id)
    return render(request, "dealer_detail.html", {"dealer": dealer, "reviews": dealer.reviews.all()})


@login_required
def review_dealer(request, dealer_id):
    dealer = get_object_or_404(Dealer, id=dealer_id)
    if request.method == "POST":
        text = request.POST.get("review")
        sentiment, _ = analyze_sentiment(text)
        DealerReview.objects.create(
            dealer=dealer,
            reviewer=request.user,
            review_text=text,
            car_make=request.POST.get("car_make"),
            car_model=request.POST.get("car_model"),
            car_year=request.POST.get("car_year"),
            purchased=request.POST.get("purchase") == "yes",
            sentiment=sentiment,
        )
        return redirect("dealer_detail", dealer_id=dealer.id)
    return render(request, "review_form.html", {"dealer": dealer})


# ---------------- JSON API (djangoapp/...) ----------------

def api_get_dealers(request):
    state = request.GET.get("state", "").upper()
    qs = Dealer.objects.all()
    if state:
        qs = qs.filter(state=state)
    data = [
        {
            "id": d.id, "full_name": d.full_name, "city": d.city, "state": d.state,
            "address": d.address, "zip": d.zip_code, "phone": d.phone, "rating": float(d.rating),
        }
        for d in qs
    ]
    return JsonResponse(data, safe=False)


def api_get_dealer(request, dealer_id):
    d = get_object_or_404(Dealer, id=dealer_id)
    return JsonResponse({
        "id": d.id, "full_name": d.full_name, "city": d.city, "state": d.state,
        "address": d.address, "zip": d.zip_code, "phone": d.phone, "rating": float(d.rating),
    })


def api_get_dealer_reviews(request, dealer_id):
    reviews = DealerReview.objects.filter(dealer_id=dealer_id)
    data = [
        {
            "id": r.id, "dealership": r.dealer_id, "name": r.reviewer.get_full_name() or r.reviewer.username,
            "purchase": r.purchased, "car_make": r.car_make, "car_model": r.car_model,
            "car_year": r.car_year, "review": r.review_text, "sentiment": r.sentiment,
        }
        for r in reviews
    ]
    return JsonResponse(data, safe=False)


def api_get_cars(request):
    data = [{"CarMake": m.name, "CarModel": [cm.name for cm in m.models.all()]} for m in CarMake.objects.all()]
    return JsonResponse(data, safe=False)


def api_analyze(request, text):
    sentiment, score = analyze_sentiment(text)
    return JsonResponse({"text": text, "sentiment": sentiment, "score": score})


@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        payload = {}
    username = payload.get("username") or request.POST.get("username")
    password = payload.get("password") or request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({"status": "Failed", "detail": "Invalid credentials"}, status=401)
    login(request, user)
    return JsonResponse({"userName": user.username, "status": "Authenticated"})


@csrf_exempt
def api_logout(request):
    username = request.user.username if request.user.is_authenticated else ""
    logout(request)
    return JsonResponse({"userName": ""})


@csrf_exempt
@require_http_methods(["POST"])
def api_register(request):
    try:
        payload = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        payload = {}
    username = payload.get("username")
    if not username:
        return JsonResponse({"detail": "Username is required"}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({"detail": "Username already taken"}, status=409)
    user = User.objects.create_user(
        username=username,
        password=payload.get("password"),
        first_name=payload.get("first_name", ""),
        last_name=payload.get("last_name", ""),
        email=payload.get("email", ""),
    )
    login(request, user)
    return JsonResponse({"userName": user.username, "status": "Registered"})
