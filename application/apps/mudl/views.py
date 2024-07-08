from django.shortcuts import render, get_object_or_404
from django import views
from .models import Course, CoursesModule


class MudlMainPage(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'mudl/main_page.html')
    

class CoursePages(views.View):
    def get(self, request, *args, **kwargs):
        modules = CoursesModule.objects.all()
        context = {
            'modules': modules,
        }
        return render(request, 'mudl/course_page.html', context=context)
    

class DetailCoursePage(views.View):
    def get(self, request, course_slug, *args, **kwargs):
        course = get_object_or_404(Course, slug=course_slug)
        context = {
            'course': course
        }
        return render(request, 'mudl/detail_course_page.html', context=context)