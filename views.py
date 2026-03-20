from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.db.models.functions import TruncMonth
from django.db.models import Count
import csv
import pandas as pd
from datetime import timedelta
import requests
import random
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import OutbreakReport


# ---------------- API KEYS ----------------
NEWS_API_KEY = "c3fb1bd7e6354c5ba3c76eab423d6acb"

# WHO API endpoint
WHO_API_URL = "https://ghoapi.azureedge.net/api/IndicatorData?Indicator=RS_1845&$top=10"


# ---------------- LOCATIONS ----------------
locations = [
    "Delhi","Mumbai","Hyderabad","Bangalore",
    "London","New York","Tokyo","Bangkok",
    "Singapore","Sydney"
]


# ---------------- DISEASE DETECTOR ----------------
def detect_disease_keyword(text):

    diseases = {
        "covid": ["covid","coronavirus","sars-cov-2"],
        "dengue": ["dengue"],
        "malaria": ["malaria"],
        "flu": ["flu","influenza"],
        "cholera": ["cholera"],
        "measles": ["measles"],
        "ebola": ["ebola"],
        "zika": ["zika"],
        "nipah": ["nipah"],
        "monkeypox": ["monkeypox","mpox"],
        "tuberculosis": ["tuberculosis","tb"],
        "hepatitis": ["hepatitis"],
        "rabies": ["rabies"],
        "yellow fever": ["yellow fever"],
        "plague": ["plague"]
    }

    text = text.lower()

    for disease, keywords in diseases.items():
        for word in keywords:
            if word in text:
                return disease

    return "unknown"


# ---------------- NEWS API ----------------
def fetch_newsapi_articles():

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": "dengue OR malaria OR covid OR flu OR measles OR cholera OR tuberculosis outbreak",
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 50,
        "apiKey": NEWS_API_KEY
    }

    try:

        response = requests.get(url, params=params, timeout=10)

        if response.status_code != 200:
            print("NewsAPI error:", response.status_code)
            return []

        data = response.json()

        articles = data.get("articles", [])

        return [a.get("title") for a in articles if a.get("title")]

    except Exception as e:

        print("NewsAPI failure:", e)
        return []


# ---------------- WHO API ----------------
def fetch_who_data():

    try:

        response = requests.get(WHO_API_URL, timeout=10)

        if response.status_code != 200:
            print("WHO API error:", response.status_code)
            return []

        data = response.json()

        reports = []

        for item in data.get("value", [])[:10]:

            indicator = item.get("Indicator", "Disease")

            reports.append(f"{indicator} cases reported")

        return reports

    except Exception as e:

        print("WHO API failure:", e)
        return []


# ---------------- FETCH DATA ----------------
def fetch_tweets_and_news():

    # Clear old records
    OutbreakReport.objects.all().delete()

    reports = []

    news_articles = fetch_newsapi_articles()
    who_reports = fetch_who_data()

    all_texts = news_articles + who_reports

    for text in all_texts:

        disease = detect_disease_keyword(text)

        if disease != "unknown":
            prob = round(random.uniform(0.60, 0.95), 2)
        else:
            prob = round(random.uniform(0.05, 0.45), 2)

        location = random.choice(locations)

        label = "Outbreak" if prob >= 0.60 else "Normal"

        report = OutbreakReport.objects.create(
            source="API",
            location=location,
            detected_disease=disease,
            probability=prob,
            text=text,
            timestamp=timezone.now(),
            predicted_label=label
        )

        reports.append(report)

    return reports


# ---------------- DASHBOARD ----------------
@login_required(login_url='login')
def dashboard(request):

    if request.method == "POST":
        fetch_tweets_and_news()

    now = timezone.now()
    three_years_ago = now - timedelta(days=3 * 365)

    reports = OutbreakReport.objects.filter(
        timestamp__gte=three_years_ago
    ).order_by("-timestamp")

    monthly_data = (
        reports
        .annotate(month=TruncMonth("timestamp"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    df = pd.DataFrame(list(monthly_data))

    return render(request, "dashboard.html", {
        "reports": reports,
        "monthly_data": df.to_dict(orient='records'),
    })


# ---------------- EXPORT CSV ----------------
def export_data(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="outbreak_reports.csv"'

    writer = csv.writer(response)

    writer.writerow([
        'Source','Location','Disease',
        'Probability','Text','Timestamp','Prediction'
    ])

    for report in OutbreakReport.objects.all():

        writer.writerow([
            report.source,
            report.location,
            report.detected_disease,
            report.probability,
            report.text,
            report.timestamp,
            report.predicted_label
        ])

    return response


# ---------------- API DATA ----------------
def outbreak_data_api(request):

    disease = request.GET.get('disease')

    qs = OutbreakReport.objects.all()

    if disease:
        qs = qs.filter(detected_disease=disease)

    return JsonResponse(list(qs.values()), safe=False)


def monthly_outbreaks_api(request):

    now = timezone.now()
    three_years_ago = now - timedelta(days=3 * 365)

    qs = (
        OutbreakReport.objects.filter(timestamp__gte=three_years_ago)
        .annotate(month=TruncMonth("timestamp"))
        .values("month")
        .annotate(count=Count("id"))
        .order_by("month")
    )

    return JsonResponse(list(qs), safe=False)


# ---------------- AUTH ----------------
def signup_view(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'User already exists'})

        user = User.objects.create_user(username=username, password=password)

        login(request, user)

        return redirect('login')

    return render(request, 'signup.html')


@csrf_protect
def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    error = None

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid credentials"

    return render(request, 'login.html', {'error': error})


def logout_view(request):

    logout(request)
    return redirect('login')