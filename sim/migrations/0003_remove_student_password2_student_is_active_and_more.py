# Generated by Django 5.0.6 on 2024-10-14 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sim', '0002_remove_student_user_student_password_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='password2',
        ),
        migrations.AddField(
            model_name='student',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='student',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
