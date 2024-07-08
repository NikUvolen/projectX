from django.contrib import admin
from .models import CoursesModule, Course


class MudlAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'module', 'created_at', 'slug')
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title')


admin.site.register(CoursesModule)
admin.site.register(Course, MudlAdmin)
