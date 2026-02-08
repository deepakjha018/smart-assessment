from django.urls import path
from .views import category_list, subcategory_list, quiz_settings, quiz_summary

urlpatterns = [
    path('categories/', category_list, name='categories'),
    path('categories/<int:category_id>/', subcategory_list, name='subcategories'),
    path('quiz-settings/<int:subcategory_id>/', quiz_settings, name='quiz_settings'),
    path('quiz-summary/', quiz_summary, name='quiz_summary'),
]
