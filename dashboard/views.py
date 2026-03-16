import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from quizzes.models import Quiz
from django.db.models import Avg, Max, Count
from django.contrib.auth.models import User

def home(request):
    return render(request, "dashboard/home.html")


@login_required
def dashboard_home(request):
    quizzes = Quiz.objects.filter(
        user=request.user,
        score__isnull=False
    )

    incomplete_quizzes = Quiz.objects.filter(
        user=request.user,
        status="in_progress"
        )

    # chronological order for charts
    chart_quizzes = quizzes.order_by("created_at")

    # latest attempts for table
    recent_quizzes = quizzes.order_by("-created_at")[:5]
    total_quizzes = quizzes.count()

    avg_score = quizzes.aggregate(
        Avg("percentage")
    )["percentage__avg"] or 0

    best_score = quizzes.aggregate(
        Max("percentage")
    )["percentage__max"] or 0

    avg_score = round(avg_score, 2)
    best_score = round(best_score, 2)

    # Chart data
    chart_labels = []
    chart_scores = []

    for i, quiz in enumerate(chart_quizzes):
        chart_labels.append(f"Attempt {i+1}")
        chart_scores.append(quiz.percentage)

    # Category distribution
    # Category distribution
    category_stats = (
        quizzes.values("topic")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    category_labels = []
    category_counts = []

    for item in category_stats:
        category_labels.append(item["topic"])
        category_counts.append(item["total"])


    

    context = {
        "total_quizzes": total_quizzes,
        "avg_score": avg_score,
        "best_score": best_score,
        "chart_labels": json.dumps(chart_labels),
        "chart_scores": json.dumps(chart_scores),
        "category_labels": json.dumps(category_labels),
        "category_counts": json.dumps(category_counts),
        "recent_quizzes": recent_quizzes,
        "incomplete_quizzes": incomplete_quizzes
    }

    return render(request, "dashboard/dashboard.html", context)


@login_required
def leaderboard(request):

    leaderboard_data = (
        Quiz.objects.filter(score__isnull=False)
        .values("user__username")
        .annotate(
            avg_score=Avg("percentage"),
            total_quizzes=Count("id")
        )
        .order_by("-avg_score")
    )

    context = {
        "leaderboard": leaderboard_data
    }

    return render(request, "dashboard/leaderboard.html", context)