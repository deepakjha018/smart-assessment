from django.shortcuts import render, get_object_or_404
from .models import Category
from django.shortcuts import render, redirect
from .models import SubCategory
from django.contrib.auth.decorators import login_required
from .utils import generate_quiz_questions
from .models import Quiz, Question
from django.shortcuts import get_object_or_404
from .models import UserAnswer
from django.http import HttpResponse
import time

@login_required
def generate_quiz(request):

    subcategory_id = request.session.get('subcategory_id')
    difficulty = request.session.get('difficulty')
    num_questions = request.session.get('question_count')

    if not subcategory_id:
        return HttpResponse("Subcategory missing from session.")

    subcategory = SubCategory.objects.get(id=subcategory_id)
    topic = subcategory.name

    questions_data = generate_quiz_questions(topic, difficulty, num_questions)

    if not questions_data:
        return render(request, "quizzes/error.html")


    # Create Quiz object
    quiz = Quiz.objects.create(
        user=request.user,
        topic=topic,
        difficulty=difficulty,
        total_questions=num_questions
    )
    
    # Save questions
    for q in questions_data:
        Question.objects.create(
            quiz=quiz,
            question_text=q["question"],
            option_a=q["options"]["A"],
            option_b=q["options"]["B"],
            option_c=q["options"]["C"],
            option_d=q["options"]["D"],
            correct_answer=q["correct_answer"]
        )

    request.session['quiz_id'] = quiz.id
    request.session['quiz_start_time'] = time.time()
    return redirect('quiz_page', question_number=1)

@login_required
def quiz_page(request, question_number):
    quiz_id = request.session.get('quiz_id')
    if not quiz_id:
        return redirect('categories')  # send back safely

    quiz = get_object_or_404(Quiz, id=quiz_id)

    questions = quiz.questions.all()
    total = questions.count()

    if question_number > total:
        return redirect('submit_quiz')

    question = questions[question_number - 1]

    if request.method == "POST":
        selected = request.POST.get("option")

        UserAnswer.objects.update_or_create(
            quiz=quiz,
            question=question,
            defaults={"selected_answer": selected}
        )

    if "next" in request.POST:
        return redirect('quiz_page', question_number=question_number + 1)

    elif "previous" in request.POST:
        return redirect('quiz_page', question_number=question_number - 1)

    elif "submit" in request.POST:
        return redirect('submit_quiz')


    try:
        user_answer = UserAnswer.objects.get(quiz=quiz, question=question)
        selected_answer = user_answer.selected_answer
    except:
        selected_answer = None

    timer_enabled = request.session.get('timer') == 'on'
    timer_duration = request.session.get('timer_duration', 0)

    context = {
        "quiz": quiz,
        "question": question,
        "question_number": question_number,
        "total": total,
        "timer_enabled": timer_enabled,
        "timer_duration": timer_duration,
        "selected_answer": selected_answer
    }

    return render(request, "quizzes/quiz_page.html", context)

@login_required
def quiz_settings(request, subcategory_id):
    subcategory = SubCategory.objects.get(id=subcategory_id)

    if request.method == 'POST':
        # store settings in session
        request.session['subcategory_id'] = subcategory.id
        request.session['difficulty'] = request.POST.get('difficulty')
        request.session['question_count'] = request.POST.get('question_count')
        request.session['timer_duration'] = int(request.POST.get('timer_duration', 0))

        return redirect('quiz_summary')  # temporary page

    return render(
        request,
        'quizzes/quiz_settings.html',
        {'subcategory': subcategory}
    )


@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'quizzes/categories.html', {'categories': categories})

@login_required
def subcategory_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = category.subcategories.all()
    return render(
        request,
        'quizzes/subcategories.html',
        {
            'category': category,
            'subcategories': subcategories
        }
    )

def quiz_summary(request):
    context = {
        'subcategory_id': request.session.get('subcategory_id'),
        'difficulty': request.session.get('difficulty'),
        'question_count': request.session.get('question_count'),
        'timer': request.session.get('timer'),
    }
    return render(request, 'quizzes/quiz_summary.html', context)

@login_required
def submit_quiz(request):
    import time
    start_time = request.session.get('quiz_start_time')
    end_time = time.time()

    time_taken = 0
    if start_time:
        time_taken = int(end_time - start_time)

    if not request.session.get('quiz_id'):
        return redirect('categories')

    quiz_id = request.session.get('quiz_id')

    if not quiz_id:
        return HttpResponse("Quiz session expired.")

    quiz = get_object_or_404(Quiz, id=quiz_id)

    questions = quiz.questions.all()
    user_answers = UserAnswer.objects.filter(quiz=quiz)

    answer_map = {ua.question.id: ua.selected_answer for ua in user_answers}

    result_data = []
    score = 0

    for question in questions:
        user_answer = answer_map.get(question.id)
        correct_answer = question.correct_answer

        is_correct = user_answer == correct_answer
        if is_correct:
            score += 1

        result_data.append({
            "question": question,
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        })

    total_questions = questions.count()

    percentage = round((score / total_questions) * 100, 2) if total_questions > 0 else 0

    if percentage >= 80:
        performance = "Excellent 🎯"
        performance_class = "success"
    elif percentage >= 50:
        performance = "Good Job 👍"
        performance_class = "warning"
    else:
        performance = "Needs Improvement 💪"
        performance_class = "danger"

    context = {
        "quiz": quiz,
        "score": score,
        "total": total_questions,
        "results": result_data,
        "percentage": percentage,
        "performance": performance,
        "time_taken": time_taken,
        "performance_class": performance_class,
    }
    if 'quiz_id' in request.session:
        del request.session['quiz_id']

    return render(request, "quizzes/quiz_result.html", context)
