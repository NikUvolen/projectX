# Generated by Django 5.0.6 on 2024-07-08 08:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mudl', '0003_course_module'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='module',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses', to='mudl.coursesmodule'),
        ),
    ]
