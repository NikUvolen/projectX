from django.urls import path
from .views import *

urlpatterns = [
    path('', MudlMainPage.as_view(), name='main_page'),
    path('course/', CoursePages.as_view(), name='course-page'),
    path('course/<str:course_slug>/', DetailCoursePage.as_view(), name='view-course')
]