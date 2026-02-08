from django.shortcuts import render, get_object_or_404
from .models import Category
from django.shortcuts import render, redirect
from .models import SubCategory

def quiz_settings(request, subcategory_id):
    subcategory = SubCategory.objects.get(id=subcategory_id)

    if request.method == 'POST':
        # store settings in session
        request.session['subcategory_id'] = subcategory.id
        request.session['difficulty'] = request.POST.get('difficulty')
        request.session['question_count'] = request.POST.get('question_count')
        request.session['timer'] = request.POST.get('timer', 'off')

        return redirect('quiz_summary')  # temporary page

    return render(
        request,
        'quizzes/quiz_settings.html',
        {'subcategory': subcategory}
    )



def category_list(request):
    categories = Category.objects.all()
    return render(request, 'quizzes/categories.html', {'categories': categories})


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
