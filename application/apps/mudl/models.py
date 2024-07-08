from django.db import models
from autoslug import AutoSlugField


class CoursesModule(models.Model):
    title = models.CharField(max_length=64, verbose_name='Название раздела')
    slug = AutoSlugField(populate_from='title', verbose_name='url раздела курсов', unique=True)

    def __str__(self) -> str:
        return f'{self.title}'
    
    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название курса')
    slug = AutoSlugField(populate_from='title', verbose_name='url курса', unique=True)
    description = models.TextField(max_length=1024, null=True, blank=True, verbose_name='Описание курса')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    module = models.ForeignKey(CoursesModule, on_delete=models.SET_NULL, related_name='courses', null=True)

    def __str__(self) -> str:
        return f'{self.title}'
    
    # def get_absolute_url(self):
    #     return reverse('view_course', kwargs={'course_slug': self.slug})

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-created_at']

